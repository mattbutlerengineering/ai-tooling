#!/bin/bash
# Validate that CLAUDE.md, README.md, and CATALOG.md counts are consistent
# Runs after edits to catch drift before commit

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -z "$REPO_ROOT" ] && exit 0

CATALOG="$REPO_ROOT/CATALOG.md"
CLAUDEMD="$REPO_ROOT/CLAUDE.md"
README="$REPO_ROOT/README.md"

[ -f "$CATALOG" ] && [ -f "$CLAUDEMD" ] && [ -f "$README" ] || exit 0

issues=""

# Count actual catalog entries (table rows excluding headers and separators)
actual_entries=$(grep '^| ' "$CATALOG" | grep -v '^| Name' | grep -v '^|---' | wc -l | tr -d ' ')

# Check CLAUDE.md entry count
claude_count=$(grep -oP 'inventory of \K\d+' "$CLAUDEMD" 2>/dev/null)
if [ -n "$claude_count" ] && [ "$claude_count" != "$actual_entries" ]; then
  issues="${issues}CLAUDE.md says $claude_count entries but CATALOG.md has $actual_entries\n"
fi

# Count actual evaluation files
actual_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')

# Check README.md eval count
readme_evals=$(grep -oP '— \K\d+(?= evidence)' "$README" 2>/dev/null)
if [ -n "$readme_evals" ] && [ "$readme_evals" != "$actual_evals" ]; then
  issues="${issues}README.md says $readme_evals eval files but evaluations/ has $actual_evals\n"
fi

# Check CLAUDE.md eval count
claude_evals=$(grep -oP '— \K\d+(?= evidence)' "$CLAUDEMD" 2>/dev/null)
if [ -n "$claude_evals" ] && [ "$claude_evals" != "$actual_evals" ]; then
  issues="${issues}CLAUDE.md says $claude_evals eval files but evaluations/ has $actual_evals\n"
fi

if [ -n "$issues" ]; then
  echo ""
  echo "⚠️  ai-tooling: count drift detected"
  printf "$issues"
  echo "Actual: $actual_entries catalog entries, $actual_evals evaluation files"
fi
