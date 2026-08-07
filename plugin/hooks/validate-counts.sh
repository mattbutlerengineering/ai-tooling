#!/bin/bash
# Surface count/sync drift after an edit, by running the repo's own canonical gates.
#
# This hook used to re-implement the count extraction in bash, grepping for the prose
# phrasing each number sits in ("inventory of N", "N evidence-based evaluations").
# `reconcile-counts.py` owns the canonical patterns for those same numbers, so one fact
# had two extractors in two languages with nothing coupling them — and when the prose was
# rewritten, the Python failed loudly while the bash silently stopped matching. Three of
# five checks had rotted to no-ops that way, two of them within three days (#443).
#
# So it delegates. That is the rule CLAUDE.md already states for every other hook here:
# the opencode plugins and the .claude/hooks scripts call the SAME scripts CI does, so
# there is one implementation. Delegating also picks up patterns the bash never knew
# about — COMPOSITION_PATTERNS arrived in #435 and no hook was taught it.
#
# In a repo that is not this one (the installed plugin fires on every Edit/Write), the
# scripts are absent and the hook stays a silent no-op.

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -z "$REPO_ROOT" ] && exit 0

issues=""

# reconcile-counts.py --check: the catalog total and the eval count/composition across
# README.md, CLAUDE.md, STACK.md and plugin/README.md, plus COMPARISON's summary rows.
if [ -f "$REPO_ROOT/reconcile-counts.py" ]; then
  if ! out=$(cd "$REPO_ROOT" && python3 reconcile-counts.py --check 2>&1); then
    issues="${issues}${out}\n"
  fi
fi

# sync-plugin-docs.sh --check: plugin/docs/ and skills/ against root.
if [ -x "$REPO_ROOT/sync-plugin-docs.sh" ]; then
  if ! out=$(cd "$REPO_ROOT" && ./sync-plugin-docs.sh --check 2>&1); then
    issues="${issues}${out}\n"
  fi
fi

if [ -n "$issues" ]; then
  echo ""
  echo "⚠️  ai-tooling: count or sync drift detected"
  printf '%b' "$issues"
  echo "Run \`make fix\` to reconcile."
fi
