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
"""
import os, re, sys, json, base64, datetime, subprocess

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
    r"|will receive no further updates)", re.I)
README_HEAD = 3000  # the banner is at the top or it is not a banner


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


def readme_signal(slug):
    """The discontinuation phrase in `slug`'s README head, or None. Returns the matched
    text rather than a bool so a record says WHY it was flagged and a human can judge
    the phrase instead of trusting the regex."""
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}/readme", "--jq", ".content"],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        head = base64.b64decode(out).decode("utf-8", "replace")[:README_HEAD]
    except (subprocess.CalledProcessError, FileNotFoundError, ValueError):
        return None  # no README, or unreachable — absence of a banner, not a signal
    m = DISCONTINUED.search(head)
    return m.group(0).strip() if m else None


def fetch(slug, today=None, maintenance=False, previous=None):
    """Repo metadata for one slug, or an UNREACHABLE record. Never raises: an
    unreachable repo is a fact to record, not a reason to abort a 460-repo run.

    With `maintenance`, adds `discontinued` (the README banner phrase, or None) and
    `license_lost` (True when `previous` recorded a real license and this fetch does
    not). The license moves in BOTH directions — daytona went AGPL-3.0 → 404 while
    vercel-labs/skills went NONE → MIT — and `--metadata-staleness` cannot see either,
    because it ages the snapshot as a whole and both records were well inside the
    threshold. A per-record flag is the only thing that catches a single flip."""
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}", "--jq", JQ],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        rec = json.loads(out)
        if maintenance:
            rec["discontinued"] = readme_signal(slug)
            had = (previous or {}).get("license_spdx")
            rec["license_lost"] = bool(
                had and had not in (UNREACHABLE, NO_LICENSE)
                and rec["license_spdx"] in (UNREACHABLE, NO_LICENSE))
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
    catalog = open(CATALOG, encoding="utf-8").read()
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
    print(f"refresh-metadata: wrote {len(cache)} records "
          f"({len(archived)} archived, {len(unreachable)} unreachable, "
          f"{len(dead)} discontinued, {len(lost)} license-lost)")
    for s in sorted(dead):
        print(f"  DISCONTINUED {s}: \"{cache[s]['discontinued']}\"")
    for s in sorted(lost):
        print(f"  LICENSE-LOST {s}: now {cache[s]['license_spdx']}")
    if undated:
        # --stale skips slugs already present, so records written before fetched_at
        # existed keep no date until a FULL refresh re-fetches them. Say so rather
        # than stamping them here, which would date a fetch that never happened.
        print(f"  {len(undated)} record(s) still carry no fetched_at — run without "
              "--stale to re-fetch and stamp them")


if __name__ == "__main__":
    main()
