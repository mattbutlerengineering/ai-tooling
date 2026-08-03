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

  ./refresh-metadata.py           # refresh every catalogued repo (slow: ~460 calls)
  ./refresh-metadata.py --stale   # only fetch slugs missing from the cache
"""
import os, sys, json, datetime, subprocess

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


def fetch(slug, today=None):
    """Repo metadata for one slug, or an UNREACHABLE record. Never raises: an
    unreachable repo is a fact to record, not a reason to abort a 460-repo run."""
    try:
        out = subprocess.run(
            ["gh", "api", f"repos/{slug}", "--jq", JQ],
            capture_output=True, text=True, check=True,
        ).stdout.strip()
        return stamp(json.loads(out), today)
    except (subprocess.CalledProcessError, FileNotFoundError, json.JSONDecodeError):
        return stamp({"license_spdx": UNREACHABLE, "archived": None,
                      "stars": None, "pushed_at": None, "resolved_name": None}, today)


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
    catalog = open(CATALOG, encoding="utf-8").read()
    slugs = catalog_slugs(catalog)
    cache = load_cache()

    todo = [s for s in sorted(slugs) if not (stale_only and s in cache)]
    print(f"refresh-metadata: {len(slugs)} catalogued repos, fetching {len(todo)}")

    for i, slug in enumerate(todo, 1):
        cache[slug] = fetch(slug)
        if i % 50 == 0:
            print(f"  {i}/{len(todo)}")

    # Drop slugs no longer catalogued so the cache can't outlive its source.
    for gone in set(cache) - set(slugs):
        del cache[gone]

    write_cache(cache)
    unreachable = [s for s, m in cache.items() if m["license_spdx"] == UNREACHABLE]
    archived = [s for s, m in cache.items() if m["archived"]]
    undated = [s for s, m in cache.items() if not m.get("fetched_at")]
    print(f"refresh-metadata: wrote {len(cache)} records "
          f"({len(archived)} archived, {len(unreachable)} unreachable)")
    if undated:
        # --stale skips slugs already present, so records written before fetched_at
        # existed keep no date until a FULL refresh re-fetches them. Say so rather
        # than stamping them here, which would date a fetch that never happened.
        print(f"  {len(undated)} record(s) still carry no fetched_at — run without "
              "--stale to re-fetch and stamp them")


if __name__ == "__main__":
    main()
