#!/bin/bash
# Validate that CLAUDE.md, README.md, CATALOG.md (and plugin/CLAUDE.md) counts agree.
# Runs after edits to catch drift before commit.
#
# NOTE: extractions are BSD/GNU portable. The real /usr/bin/grep on macOS has no
# -P (PCRE) flag, so `grep -oP '...\K...'` silently returns empty there and every
# count check it guarded was a dead no-op. Use `grep -oE` + a number pull instead.

REPO_ROOT="$(git rev-parse --show-toplevel 2>/dev/null)"
[ -z "$REPO_ROOT" ] && exit 0

CATALOG="$REPO_ROOT/CATALOG.md"
CLAUDEMD="$REPO_ROOT/CLAUDE.md"
README="$REPO_ROOT/README.md"
PLUGIN_CLAUDEMD="$REPO_ROOT/plugin/CLAUDE.md"

[ -f "$CATALOG" ] && [ -f "$CLAUDEMD" ] && [ -f "$README" ] || exit 0

# Pull the integer that follows a phrase, e.g. num_after "inventory of" file -> 477
num_after()  { grep -oE "$1 [0-9]+" "$2" 2>/dev/null | grep -oE '[0-9]+' | head -1; }
# Pull the integer that precedes a phrase, e.g. num_before "evidence" file -> 466
num_before() { grep -oE "[0-9]+ $1" "$2" 2>/dev/null | grep -oE '[0-9]+' | head -1; }

issues=""

# Count actual catalog entries (table rows excluding headers and separators)
actual_entries=$(grep '^| ' "$CATALOG" | grep -v '^| Name' | grep -v '^|---' | wc -l | tr -d ' ')

# Check CLAUDE.md entry count
claude_count=$(num_after "inventory of" "$CLAUDEMD")
if [ -n "$claude_count" ] && [ "$claude_count" != "$actual_entries" ]; then
  issues="${issues}CLAUDE.md says $claude_count entries but CATALOG.md has $actual_entries\n"
fi

# Check plugin/CLAUDE.md entry count (hand-maintained, not synced — drifts silently)
if [ -f "$PLUGIN_CLAUDEMD" ]; then
  plugin_claude_count=$(num_after "inventory of" "$PLUGIN_CLAUDEMD")
  if [ -n "$plugin_claude_count" ] && [ "$plugin_claude_count" != "$actual_entries" ]; then
    issues="${issues}plugin/CLAUDE.md says $plugin_claude_count entries but CATALOG.md has $actual_entries\n"
  fi
fi

# Count actual evaluation files
actual_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')

# Check README.md eval count
readme_evals=$(num_before "evidence" "$README")
if [ -n "$readme_evals" ] && [ "$readme_evals" != "$actual_evals" ]; then
  issues="${issues}README.md says $readme_evals eval files but evaluations/ has $actual_evals\n"
fi

# Check CLAUDE.md eval count
claude_evals=$(num_before "evidence" "$CLAUDEMD")
if [ -n "$claude_evals" ] && [ "$claude_evals" != "$actual_evals" ]; then
  issues="${issues}CLAUDE.md says $claude_evals eval files but evaluations/ has $actual_evals\n"
fi

# Check plugin/docs sync
PLUGIN_CATALOG="$REPO_ROOT/plugin/docs/CATALOG.md"
if [ -f "$PLUGIN_CATALOG" ]; then
  plugin_entries=$(grep '^| ' "$PLUGIN_CATALOG" | grep -v '^| Name' | grep -v '^|---' | wc -l | tr -d ' ')
  if [ "$plugin_entries" != "$actual_entries" ]; then
    issues="${issues}plugin/docs/CATALOG.md has $plugin_entries entries but root has $actual_entries — run ./sync-plugin-docs.sh\n"
  fi
fi

if [ -n "$issues" ]; then
  echo ""
  echo "⚠️  ai-tooling: count drift detected"
  printf "$issues"
  echo "Actual: $actual_entries catalog entries, $actual_evals evaluation files"
fi
