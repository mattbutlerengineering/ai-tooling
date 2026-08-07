#!/usr/bin/env python3
"""What maintenance this catalog needs — the SessionStart hook's two questions, answered
by the implementations that already own them.

    gh api user/starred --paginate --jq '.[].full_name' | python3 freshness.py
    python3 freshness.py --uncatalogued < slugs.txt   # just the slugs, for /sync-stars

Prints nothing when there is nothing to say, so the hook can stay quiet.

`plugin/hooks/check-freshness.sh` used to answer both questions itself, in bash, and got
both wrong (#445). This is #443's remedy one hook over: delegate, because CLAUDE.md's
rule for every other hook here is that the opencode plugins, the .claude/hooks scripts
and CI call the *same* scripts — one implementation.

**Staleness.** The hook compared each file's **mtime** against a flat 30 days. The repo
already answers this with `**Last verified:**` (a mandatory, gated field) and
`STALENESS_DAYS` keyed by Type — ~120 days for harnesses/MCP servers/frameworks, ~180
for tools/skills/plugins, ~365 for references, "tune in one place". The two did not
merely differ: on the tree that filed #445 the hook named 96 files, the sweep named 0,
and they shared **no** findings. mtime cannot do better, because it is a checkout
artifact — in a fresh `git clone` every eval is zero minutes old, so the check was
loudest where nothing was stale and silent on a fresh install however stale the corpus
truly was. It also read `plugin/docs/evaluations/`, the *synced copy*, making its dates
a fact about `sync-plugin-docs.sh` rather than about any evaluation.

So the sweep runs here via `ae.audit_staleness`, called directly on a `DetectorContext`
— `watchlist.py`'s rule, never re-implemented and never shelled out to and never
grep-parsed out of another script's prose, which is the exact failure #443 fixed.

**Stars.** The hook threw away the owner of each `full_name` and asked whether the bare
repo name appeared *anywhere* in CATALOG.md, case-insensitively, as a substring. That
hid 52 of 277 real leads: `dotnet/skills` matched the word "skills" in the column
legend, `Netflix/conductor` matched a bare `conductor` in an *Overlaps with* cell,
`apple/container` matched the prose "containerized", and `docling-project/docling`
matched `Docling (ext.)` — a token whose entire purpose is to assert the tool is *not*
catalogued. That is the identity-by-name error #343 found in the catalog, #366 on the
filesystem and #374 in triage.py's shield, surviving in the one place that feeds the
pipeline: scan intake. Key on what the row *is*, which in slug-space is its link.

Two rules carry the star half:

- **The network stays out of this file.** `refresh-metadata.py` is documented as the
  only script that calls `gh`; taking the slug list on stdin keeps that true and makes
  the comparison offline, deterministic and unit-testable. The caller fetches.
- **Resolution is deliberately generous** — *any* `github.com/owner/repo` link anywhere
  in CATALOG.md counts, not only a row's Name cell. A repo *linked* from a redirect note
  or an overlaps cell is one a human has already looked at, and re-offering it as a new
  lead costs more than missing it (detector V's rule). A repo merely *named* in prose is
  a different thing and stays a gap — that is precisely the case the basename grep got
  wrong, so the generosity is about links and never about text. On the tree that filed
  #445 the two readings agree exactly (265 of 542 starred repos), so the generosity is
  bought at no measured cost. A subpath link resolves to its `owner/repo`, so starring the
  container of a catalogued subpath is not a gap — the bug latent in `/sync-stars`' own
  `github\\.com/[^)]+` extraction.
"""
import importlib.util
import os
import sys

import catalog_lib

ROOT = os.path.dirname(os.path.abspath(__file__))

_spec = importlib.util.spec_from_file_location("audit_evals", os.path.join(ROOT, "audit-evals.py"))
if _spec is None or _spec.loader is None:  # a sibling in this repo — absent means a broken checkout
    raise ImportError("cannot load audit-evals.py from " + ROOT)
ae = importlib.util.module_from_spec(_spec); _spec.loader.exec_module(ae)


def read_slugs(text):
    """Ordered, de-duplicated `owner/repo` slugs from a `full_name`-per-line list.

    Anything that is not `owner/repo` is dropped rather than compared: a stray URL or a
    `gh` error line on stdin must never become a lead."""
    seen, out = set(), []
    for line in text.splitlines():
        s = line.strip()
        if not s or s.startswith("#"):
            continue
        if s.count("/") != 1 or not all(s.split("/")):
            continue
        if s.lower() not in seen:
            seen.add(s.lower())
            out.append(s)
    return out


def uncatalogued(slug_text, catalog_text):
    """The slugs with no `github.com/owner/repo` link in the catalog, in input order."""
    known = {s.lower() for s in catalog_lib.github_repos(catalog_text)}
    return [s for s in read_slugs(slug_text) if s.lower() not in known]


def stale_evals(root=None):
    """(stale, undated) from the repo's own staleness sweep — never a second reading."""
    return ae.audit_staleness(ae.DetectorContext(root or ROOT))


def report(slug_text, catalog_text, root=None, limit=10):
    """The hook's lines, or [] when there is nothing to say.

    `limit` caps the per-eval detail, and the cap is *disclosed* in the line that
    follows rather than silently truncating (the no-silent-caps rule)."""
    lines = []
    stale, _undated = stale_evals(root)
    for name, _type, date, age, threshold in stale[:limit]:
        lines.append(f"  - {name} last verified {date} ({age}d, threshold {threshold}d)")
    if len(stale) > limit:
        lines.append(f"  - …and {len(stale) - limit} more past their staleness threshold")
    missing = uncatalogued(slug_text, catalog_text)
    if missing:
        lines.append(f"  - {len(missing)} starred repo(s) with no catalog row")
    return lines


def main():
    args = sys.argv[1:]
    catalog = os.path.join(ROOT, "CATALOG.md")
    if not os.path.exists(catalog):
        print(f"freshness: no CATALOG.md at {ROOT}", file=sys.stderr)
        return 2
    with open(catalog, encoding="utf-8") as fh:
        catalog_text = fh.read()
    slug_text = "" if sys.stdin.isatty() else sys.stdin.read()
    if "--uncatalogued" in args:
        print("\n".join(uncatalogued(slug_text, catalog_text)))
        return 0
    lines = report(slug_text, catalog_text)
    if lines:
        print("⚡ ai-tooling: workflow maintenance needed")
        print("\n".join(lines))
        print("  Run /update-catalog to sync")
    return 0


if __name__ == "__main__":
    sys.exit(main())
