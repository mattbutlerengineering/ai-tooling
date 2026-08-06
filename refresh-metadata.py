#!/usr/bin/env python3
"""
refresh-metadata.py — fetch GitHub repo metadata for every catalogued tool into
`repo-metadata.json`, the offline cache the triage bands and the eval-header
backfills read.

This is the ONLY script that calls `gh`. Everything downstream (triage.py, the
`**Stars:**`/`**License:**` backfill) reads the committed JSON, so `make check`
stays offline and CI never depends on 460 API calls or a rate limit. That split
mirrors audit-evals.py, whose gating detectors are offline while `--installs`
and `--archived` are opt-in network passes.

Why the cache exists at all: banding a `discovery-log` lead needs facts about the
repo (is it archived? what license?) that live nowhere in the repo's own files.

Every record it writes carries a `fetched_at` stamp — OUR fetch date, which no other
field holds (`pushed_at` is the repo's). `audit-evals.py --metadata-staleness` reads it
to age the cache (#260). `--stale` skips slugs already cached, so records written before
the stamp existed stay undated until a full run re-fetches them; they are never
backfilled, since a floor date would assert a fetch that never happened.

  ./refresh-metadata.py                 # refresh every catalogued repo (slow: ~460 calls)
  ./refresh-metadata.py --stale         # only fetch slugs missing from the cache
  ./refresh-metadata.py --maintenance   # also read each README head for a discontinuation
                                        #   banner (#351) — DOUBLES the call count

A repo whose license comes back absent gets a few extra calls on EVERY path, not just
--maintenance: see LICENSE_HEADING below for why `NONE` cannot be trusted as an absence.
That is scoped to the handful of records it applies to, so it costs a few dozen calls in
a ~600-repo run rather than doubling it.
"""
import base64
import datetime
import json
import os
import re
import subprocess
import sys
from pathlib import Path

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))
CATALOG = os.path.join(ROOT, "CATALOG.md")
CACHE = os.path.join(ROOT, "repo-metadata.json")

# GitHub returns 404 for a repo that never existed, was renamed away, or was taken
# down (DMCA). All three mean "we cannot see it" — recorded distinctly from NONE,
# which means the repo is live and simply declares no license. Conflating them would
# turn a takedown into a licensing verdict.
UNREACHABLE = "404"
NO_LICENSE = "NONE"

JQ = (
    '{license_spdx: (.license.spdx_id // "NONE"), archived: .archived, '
    'stars: .stargazers_count, pushed_at: .pushed_at, resolved_name: .full_name}'
)

# `archived == true` is the clean structural death signal, and it only catches
# maintainers who took the extra step of flipping the flag. daytonaio/daytona — ★72K,
# the catalog's canonical sandbox answer — announced discontinuation in its README in
# June 2026, moved development to a private codebase, and sat in P3 backlog as ordinary
# un-examined work for two months because `archived` stayed false (#351).
#
# So: read the README head and look for the banner maintainers actually write. This is
# the HIGH-PRECISION signal. Deliberately NOT a `pushed_at` threshold — dormancy is not
# discontinuation, and the distinction is load-bearing: `plandex` was SKIPped at 13
# months because a *coding agent* rots when model APIs turn over, while `ralph` was left
# at ~6 because an autonomous *loop* is a pattern over whatever harness you point it at.
# Age informs a human; it does not dispose a lead.
DISCONTINUED = re.compile(
    r"(?:no longer (?:maintained|actively maintained|supported|under development)"
    r"|not (?:actively )?maintained"
    r"|this (?:repo|repository|project) (?:is|has been) (?:deprecated|archived|discontinued|unmaintained)"
    r"|(?:project|development) (?:is |has been )?(?:discontinued|sunset|abandoned)"
    r"|moved to a private (?:codebase|repo)"
    # Anchored to the REPO as the subject. A bare `(?:is|now) read-only` flagged
    # openai/codex-plugin-cc ("This command is read-only and will not perform any
    # changes") and danmcinerney/architect-loop ("The closing final-review is
    # read-only") — both live tools describing a COMMAND. A detector that flags a
    # healthy tool is worse than one that misses a dead one, because the miss costs
    # a stale row and the false positive costs trust in every other finding.
    r"|(?:repo|repository|project) is (?:now )?read-only"
    r"|will receive no further updates)", re.IGNORECASE)
README_HEAD = 3000  # the banner is at the top or it is not a banner

# GitHub's licensee detector reads exactly one thing: a root LICENSE file. A repo that
# states its terms in the README, or in package.json, or in both, records `NONE` — the
# same value as a repo that grants nothing. triage.py's P4 mechanical-skip band disposes
# vendored leads on that value, so the conflation is not academic: 8 of 28 NONE records
# were wrong, and two skill leads were SKIPped "text carrying no license grant cannot be
# copied in" against a README reading `## License` / `MIT` (#372).
#
# What this records is a CANDIDATE, not a license. A README line naming MIT without the
# license text or a copyright holder is a thinner record than a LICENSE file, and whether
# that is good enough is a human call. What it is NOT is an absence — and only an absence
# can carry a mechanical SKIP.
#
# Recorded ONLY when the API reports no license, which is the one state where it changes
# a disposition, and re-derived on every fetch rather than carried forward: a repo that
# later adds a real LICENSE file drops the field on its own.
LICENSE_HEADING = re.compile(r"^#{1,6}[ \t]*licen[cs]e\b.*$", re.IGNORECASE | re.MULTILINE)
LICENSE_SECTION = 400   # chars after the heading — the name is in the first line or two
MANIFESTS = ("package.json", "pyproject.toml", "Cargo.toml")

# Longest-first within a family so AGPL never matches as GPL and CC-BY-NC-SA never as
# CC-BY. The value is the FAMILY, not the version: nothing downstream keys on a version
# (triage.py's DISQUALIFYING_LICENSE matches on prefix, and a human reads the phrase),
# and inferring "GPL" -> "GPL-3.0" from prose that never said 3.0 would be a fabrication
# in a field whose entire purpose is to stop one.
SPDX_FAMILIES = (
    ("AGPL", "AGPL"), ("LGPL", "LGPL"), ("GPL", "GPL"),
    ("APACHE", "Apache-2.0"), ("BSD-3", "BSD-3-Clause"), ("BSD-2", "BSD-2-Clause"),
    ("BSD", "BSD"), ("MPL", "MPL-2.0"), ("CC0", "CC0-1.0"),
    ("CC-BY-NC-SA", "CC-BY-NC-SA"), ("CC-BY-SA", "CC-BY-SA"),
    ("CC-BY-NC", "CC-BY-NC"), ("CC-BY", "CC-BY"), ("EUPL", "EUPL"),
    ("MIT", "MIT"), ("ISC", "ISC"), ("UNLICENSE", "Unlicense"),
    ("ZLIB", "Zlib"), ("WTFPL", "WTFPL"), ("PROPRIETARY", "Proprietary"),
)
SPDX_TOKEN = re.compile(
    r"\b(AGPL[-\s]?[0-9.]*|LGPL[-\s]?[0-9.]*|GPL[-\s]?[0-9.]*"
    r"|Apache(?:[-\s]License)?[-\s]?[0-9.]*|BSD[-\s]?[0-9]?[-\s]?(?:Clause)?"
    r"|MPL[-\s]?[0-9.]*|CC0[-\s]?[0-9.]*|CC[-\s]BY(?:[-\s]NC)?(?:[-\s]SA)?[-\s]?[0-9.]*"
    r"|EUPL[-\s]?[0-9.]*|MIT|ISC|Unlicense|Zlib|WTFPL|proprietary)\b", re.IGNORECASE)


def normalize_spdx(token):
    """The SPDX family a license NAME in prose belongs to, or the token uppercased when
    it belongs to none. Sorted longest-family-first by SPDX_FAMILIES, not by regex luck."""
    t = re.sub(r"[\s_]+", "-", token.strip()).upper()
    for prefix, family in sorted(SPDX_FAMILIES, key=lambda p: -len(p[0])):
        if t.startswith(prefix):
            return family
    return t


def catalog_slugs(catalog_text):
    """Every `owner/repo` a CATALOG row links to in its Name cell, lowercased and
    de-duplicated. Only the Name cell — an "Overlaps with" cell can mention a repo
    we do not catalogue, and a row's identity is its own link."""
    slugs = {}
    for row in catalog_lib.parse_catalog_rows(catalog_text):
        if not row.url:
            continue
        found = catalog_lib.github_repos(row.url)
        if found:
            slugs[found[0].lower()] = row.name
    return slugs


def stamp(record, today=None):
    """`record` with today's date as `fetched_at`. This is OUR fetch date, which no
    other field carries: `pushed_at` is when the *repo* was last pushed, so a busy
    repo looks freshly-checked no matter how old our snapshot of it is. Detector R
    (audit-evals.py --metadata-staleness) reads this to age the cache; without it,
    a repo archived after our last refresh keeps its `archived: false` record and
    silently never reaches the P1 successor-check band. Stamped on the UNREACHABLE
    path too — "we looked and got a 404" is as much a dated observation as a hit.
    `today` is injectable for tests."""
    return dict(record, fetched_at=(today or datetime.date.today()).isoformat())


def _gh_file(slug, path):
    """A repo file's decoded text, or "" when absent/unreachable. Never raises: a
    missing file is a fact about the repo, not a reason to abort a 600-repo run."""
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}/{path}", "--jq", ".content"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return base64.b64decode(out).decode("utf-8", "replace")
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return ""


def readme_text(slug):
    return _gh_file(slug, "readme")


def discontinued_phrase(text):
    """The discontinuation phrase in a README HEAD, or None. Returns the matched text
    rather than a bool so a record says WHY it was flagged and a human can judge the
    phrase instead of trusting the regex. Scoped to the head: the banner is at the top
    or it is not a banner."""
    m = DISCONTINUED.search(text[:README_HEAD])
    return m.group(0).strip() if m else None


def readme_license(text):
    """(family, quoted phrase) for a license named under a README `## License` heading,
    or None. Searches the WHOLE README, not the head — a license section sits at the
    bottom (vercel-labs/agent-skills' is at line 226), which is exactly the opposite of
    where a discontinuation banner lives."""
    h = LICENSE_HEADING.search(text)
    if not h:
        return None
    section = text[h.end():h.end() + LICENSE_SECTION]
    m = SPDX_TOKEN.search(section)
    if not m:
        return None
    phrase = " ".join((h.group(0) + " " + section[:m.end()]).split())
    return normalize_spdx(m.group(1)), phrase


def manifest_license(slug):
    """(family, quoted phrase, filename) from the first root manifest that declares a
    license, or None. package.json first (the catalog skews JS), then the TOML pair —
    `license = "MIT"` parses the same in pyproject.toml and Cargo.toml."""
    for fn in MANIFESTS:
        text = _gh_file(slug, f"contents/{fn}")
        if not text:
            continue
        m = re.search(r'"license"\s*:\s*"([^"]+)"', text) if fn.endswith(".json") \
            else re.search(r'^\s*license\s*=\s*"([^"]+)"', text, re.MULTILINE)
        # npm's legacy object form: "license": { "type": "MIT" }
        if not m and fn.endswith(".json"):
            m = re.search(r'"license"\s*:\s*\{[^}]*"type"\s*:\s*"([^"]+)"', text, re.DOTALL)
        if m:
            return normalize_spdx(m.group(1)), f'{fn}: "{m.group(1)}"', fn
    return None


def declared_license(slug, readme=None):
    """`license_declared` for a repo GitHub reports no license for, or None.

    Records where the grant was found and quotes it, so a human judges the wording
    rather than trusting the regex (detector V's rule). When the README and the manifest
    disagree it records BOTH and says so: builderio/agent-native reads MIT in its README
    and ISC in package.json, and the standing "the LICENSE file governs" tiebreak (#26)
    has nothing to govern with when there is no LICENSE file."""
    text = readme if readme is not None else readme_text(slug)
    from_readme = readme_license(text) if text else None
    from_manifest = manifest_license(slug)
    if not from_readme and not from_manifest:
        return None
    if from_readme and from_manifest:
        spdx, phrase = from_readme
        mspdx, mphrase, _ = from_manifest
        rec = {"spdx": spdx, "where": "readme+manifest", "phrase": f"{phrase} | {mphrase}"}
        if mspdx != spdx:
            rec.update(conflict=mspdx, where="readme")
        return rec
    if from_readme:
        return {"spdx": from_readme[0], "where": "readme", "phrase": from_readme[1]}
    spdx, phrase, _fn = from_manifest
    return {"spdx": spdx, "where": "manifest", "phrase": phrase}


def fetch(slug, today=None, maintenance=False, previous=None):
    """Repo metadata for one slug, or an UNREACHABLE record. Never raises: an
    unreachable repo is a fact to record, not a reason to abort a 460-repo run.

    With `maintenance`, adds `discontinued` (the README banner phrase, or None) and
    `license_lost` (True when `previous` recorded a real license and this fetch does
    not). The license moves in BOTH directions — daytona went AGPL-3.0 → 404 while
    vercel-labs/skills went NONE → MIT — and `--metadata-staleness` cannot see either,
    because it ages the snapshot as a whole and both records were well inside the
    threshold. A per-record flag is the only thing that catches a single flip.

    `license_declared` is written on EVERY path, not just --maintenance, because it
    fires only on a `NONE` license and there are a few dozen of those — a rounding error
    against a ~600-repo run, and the field is what stops P4 disposing a lead on a license
    GitHub merely failed to look for (#372)."""
    readme = None
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}", "--jq", JQ],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        rec = json.loads(out)
        if maintenance:
            readme = readme_text(slug)
            rec["discontinued"] = discontinued_phrase(readme)
            had = (previous or {}).get("license_spdx")
            rec["license_lost"] = bool(
                had and had not in (UNREACHABLE, NO_LICENSE)
                and rec["license_spdx"] in (UNREACHABLE, NO_LICENSE))
        if rec.get("license_spdx") == NO_LICENSE:
            found = declared_license(slug, readme)
            if found:
                rec["license_declared"] = found
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        rec = {"license_spdx": UNREACHABLE, "archived": None,
               "stars": None, "pushed_at": None, "resolved_name": None}
    # A human's false-positive acknowledgment (#360) is the one field this script does
    # not own; carry it forward or a refresh silently erases the judgement call. Applied
    # on EVERY path — not just --maintenance runs, and notably including the unreachable
    # one, since a transient `gh` failure must not cost a human decision.
    ack = (previous or {}).get("discontinued_ack")
    if ack:
        rec["discontinued_ack"] = ack
    return stamp(rec, today)


def load_cache():
    if not os.path.exists(CACHE):
        return {}
    with open(CACHE, encoding="utf-8") as f:
        return json.load(f)


def write_cache(data):
    with open(CACHE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, sort_keys=True, ensure_ascii=False)
        f.write("\n")


def main():
    stale_only = "--stale" in sys.argv[1:]
    maintenance = "--maintenance" in sys.argv[1:]
    catalog = Path(CATALOG).read_text(encoding="utf-8")
    slugs = catalog_slugs(catalog)
    cache = load_cache()

    todo = [s for s in sorted(slugs) if not (stale_only and s in cache)]
    calls = len(todo) * (2 if maintenance else 1)
    print(f"refresh-metadata: {len(slugs)} catalogued repos, fetching {len(todo)} "
          f"(~{calls} API calls{'; --maintenance reads each README too' if maintenance else ''})")

    for i, slug in enumerate(todo, 1):
        cache[slug] = fetch(slug, maintenance=maintenance, previous=cache.get(slug))
        if i % 50 == 0:
            print(f"  {i}/{len(todo)}")

    # Drop slugs no longer catalogued so the cache can't outlive its source.
    for gone in set(cache) - set(slugs):
        del cache[gone]

    write_cache(cache)
    unreachable = [s for s, m in cache.items() if m["license_spdx"] == UNREACHABLE]
    archived = [s for s, m in cache.items() if m["archived"]]
    undated = [s for s, m in cache.items() if not m.get("fetched_at")]
    dead = [s for s, m in cache.items() if m.get("discontinued")]
    lost = [s for s, m in cache.items() if m.get("license_lost")]
    declared = [s for s, m in cache.items() if m.get("license_declared")]
    nolicense = [s for s, m in cache.items() if m["license_spdx"] == NO_LICENSE]
    print(f"refresh-metadata: wrote {len(cache)} records "
          f"({len(archived)} archived, {len(unreachable)} unreachable, "
          f"{len(dead)} discontinued, {len(lost)} license-lost, "
          f"{len(declared)} of {len(nolicense)} 'NONE' declared elsewhere)")
    for s in sorted(dead):
        print(f"  DISCONTINUED {s}: \"{cache[s]['discontinued']}\"")
    for s in sorted(lost):
        print(f"  LICENSE-LOST {s}: now {cache[s]['license_spdx']}")
    for s in sorted(declared):
        d = cache[s]["license_declared"]
        conflict = f" (manifest says {d['conflict']})" if d.get("conflict") else ""
        print(f"  DECLARED {s}: {d['spdx']} in {d['where']}{conflict} — \"{d['phrase']}\"")
    if undated:
        # --stale skips slugs already present, so records written before fetched_at
        # existed keep no date until a FULL refresh re-fetches them. Say so rather
        # than stamping them here, which would date a fetch that never happened.
        print(f"  {len(undated)} record(s) still carry no fetched_at — run without "
              "--stale to re-fetch and stamp them")


if __name__ == "__main__":
    main()
