#!/usr/bin/env bash
# Sync root documentation to plugin/docs/ so the installable plugin stays current.
# Also syncs root skills/ from plugin/skills/ (plugin is authoritative for skills).
# Run before publishing or via pre-commit hook.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DOCS="$REPO_ROOT/plugin/docs"
PLUGIN_SKILLS="$REPO_ROOT/plugin/skills"
ROOT_SKILLS="$REPO_ROOT/skills"

# --- Docs: root → plugin/docs/ ---
mkdir -p "$PLUGIN_DOCS/evaluations"

cp "$REPO_ROOT/CATALOG.md" "$PLUGIN_DOCS/CATALOG.md"
cp "$REPO_ROOT/WORKFLOW.md" "$PLUGIN_DOCS/WORKFLOW.md"
rsync -a --delete "$REPO_ROOT/evaluations/" "$PLUGIN_DOCS/evaluations/"

# --- Skills: plugin/skills/ → root/skills/ (strip ${CLAUDE_PLUGIN_ROOT}/docs/ paths) ---
for skill_dir in "$PLUGIN_SKILLS"/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$ROOT_SKILLS/$skill_name"
  sed 's|\${CLAUDE_PLUGIN_ROOT}/docs/||g' "$skill_dir/SKILL.md" > "$ROOT_SKILLS/$skill_name/SKILL.md"
done

# --- Verify ---
root_entries=$(grep "^|" "$REPO_ROOT/CATALOG.md" | grep -v "^| Name " | grep -v "^|---" | wc -l | tr -d ' ')
plugin_entries=$(grep "^|" "$PLUGIN_DOCS/CATALOG.md" | grep -v "^| Name " | grep -v "^|---" | wc -l | tr -d ' ')
root_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')
plugin_evals=$(ls "$PLUGIN_DOCS/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')
skill_count=$(ls -d "$PLUGIN_SKILLS"/*/ 2>/dev/null | wc -l | tr -d ' ')

echo "Synced: CATALOG.md ($plugin_entries entries), WORKFLOW.md, evaluations/ ($plugin_evals files), skills/ ($skill_count skills)"

if [ "$root_entries" != "$plugin_entries" ] || [ "$root_evals" != "$plugin_evals" ]; then
  echo "WARNING: count mismatch after sync — root has $root_entries entries/$root_evals evals, plugin has $plugin_entries/$plugin_evals"
  exit 1
fi
