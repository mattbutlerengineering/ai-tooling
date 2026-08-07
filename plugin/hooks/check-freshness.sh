#!/bin/bash
# Surface catalog maintenance at session start, by running the repo's own implementations.
#
# This hook used to answer its two questions itself, in bash, and got both wrong (#445):
# it compared each eval's file **mtime** against a flat 30 days — a checkout artifact
# measured against a threshold the repo already keys by Type — and it decided whether a
# starred repo was catalogued by grepping the bare repo **basename** as a substring of
# the whole catalog, which hid 52 of 277 real leads behind matches in prose.
#
# So it delegates, exactly as validate-counts.sh does since #443. `freshness.py` calls
# audit-evals.py's own staleness detector and resolves stars by slug; there is one
# implementation of each fact, and no bash grep of another script's prose to rot.
#
# Scoped to this repo on purpose. The advice is "run /update-catalog" — a maintainer
# operation on *this* catalog — so a user who installed the plugin for its skills has no
# CATALOG.md to act on. Outside the repo the hook is a silent no-op rather than an
# answer computed from the bundled copy.

json_quiet='{"continue":true,"suppressOutput":true}'

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
if [ -z "$REPO_ROOT" ] || [ ! -f "$REPO_ROOT/freshness.py" ]; then
  echo "$json_quiet"
  exit 0
fi

# The network lives here, not in freshness.py: refresh-metadata.py is the only script
# that calls `gh`, so the slug list arrives on stdin. No `gh`, no star half — a missing
# fetch must not read as "nothing new".
stars=""
if command -v gh &>/dev/null; then
  stars=$(gh api user/starred --paginate --jq '.[].full_name' 2>/dev/null)
fi

report=$(cd "$REPO_ROOT" && printf '%s\n' "$stars" | python3 freshness.py 2>/dev/null)

# Output is either a JSON control payload or a message, never both concatenated: the old
# hook printed the control line and then 100 lines of text, so the payload did not parse
# as JSON and the control line was simply the first thing the user saw.
if [ -n "$report" ]; then
  echo "$report"
  echo "  (details: make check, or python3 audit-evals.py --staleness)"
else
  echo "$json_quiet"
fi
