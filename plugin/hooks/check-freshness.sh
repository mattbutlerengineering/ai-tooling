#!/bin/bash
# Check if evaluations are stale (>30 days) or if new stars exist
# Outputs nothing if everything is current (suppressed)

PLUGIN_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
EVAL_DIR="$PLUGIN_ROOT/docs/evaluations"
STALE_DAYS=30
ISSUES=""

# Check evaluation file freshness
if [ -d "$EVAL_DIR" ]; then
  for f in "$EVAL_DIR"/*.md; do
    [ -f "$f" ] || continue
    if [ "$(uname)" = "Darwin" ]; then
      file_age=$(( ( $(date +%s) - $(stat -f %m "$f") ) / 86400 ))
    else
      file_age=$(( ( $(date +%s) - $(stat -c %Y "$f") ) / 86400 ))
    fi
    if [ "$file_age" -gt "$STALE_DAYS" ]; then
      basename_f=$(basename "$f")
      ISSUES="${ISSUES}  - ${basename_f} is ${file_age} days old\n"
    fi
  done
fi

# Check for new GitHub stars not in catalog
if command -v gh &>/dev/null; then
  CATALOG="$PLUGIN_ROOT/docs/CATALOG.md"
  if [ -f "$CATALOG" ]; then
    new_stars=$(gh api user/starred --paginate --jq '.[].full_name' 2>/dev/null | while read -r repo; do
      name=$(echo "$repo" | cut -d/ -f2)
      if ! grep -qi "$name" "$CATALOG" 2>/dev/null; then
        echo "$repo"
      fi
    done)
    if [ -n "$new_stars" ]; then
      count=$(echo "$new_stars" | wc -l | tr -d ' ')
      ISSUES="${ISSUES}  - ${count} new starred repos not in catalog\n"
    fi
  fi
fi

# Output only if there are issues
if [ -n "$ISSUES" ]; then
  echo '{"continue":true,"suppressOutput":false}'
  echo ""
  echo "⚡ ai-tooling: workflow maintenance needed"
  printf "$ISSUES"
  echo "  Run /update-catalog to sync"
else
  echo '{"continue":true,"suppressOutput":true}'
fi
