#!/usr/bin/env bash
# Sync root documentation to plugin/docs/ so the installable plugin stays current.
# Also syncs root skills/ from plugin/skills/ (plugin is authoritative for skills).
# Run before publishing or via pre-commit hook.
#
#   ./sync-plugin-docs.sh           # apply: write the synced tree in place
#   ./sync-plugin-docs.sh --check   # verify only: exit 1 if plugin/docs or skills
#                                     would change; mutate nothing (CI/pre-commit gate)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DOCS="$REPO_ROOT/plugin/docs"
PLUGIN_SKILLS="$REPO_ROOT/plugin/skills"
ROOT_SKILLS="$REPO_ROOT/skills"

CHECK=0
[ "${1:-}" = "--check" ] && CHECK=1

# In --check we build the would-be-synced tree in a scratch dir and diff it against
# the committed copies, mutating nothing. In apply mode we write straight to the
# real destinations, so apply behaviour is byte-for-byte unchanged.
if [ "$CHECK" = 1 ]; then
  SCRATCH="$(mktemp -d)"
  trap 'rm -rf "$SCRATCH"' EXIT
  DEST_DOCS="$SCRATCH/docs"
  DEST_SKILLS="$SCRATCH/skills"
else
  DEST_DOCS="$PLUGIN_DOCS"
  DEST_SKILLS="$ROOT_SKILLS"
fi

# --- Docs: root → DEST_DOCS ---
mkdir -p "$DEST_DOCS/evaluations" "$DEST_DOCS/discovery"

cp "$REPO_ROOT/CATALOG.md" "$DEST_DOCS/CATALOG.md"
cp "$REPO_ROOT/WORKFLOW.md" "$DEST_DOCS/WORKFLOW.md"
cp "$REPO_ROOT/STACK.md" "$DEST_DOCS/STACK.md"
cp "$REPO_ROOT/STACK-LEDGER.md" "$DEST_DOCS/STACK-LEDGER.md"
rsync -a --delete "$REPO_ROOT/evaluations/" "$DEST_DOCS/evaluations/"
rsync -a --delete "$REPO_ROOT/discovery/" "$DEST_DOCS/discovery/"

# --- Skills: plugin/skills/ → DEST_SKILLS (strip ${CLAUDE_PLUGIN_ROOT}/docs/ paths) ---
for skill_dir in "$PLUGIN_SKILLS"/*/; do
  skill_name=$(basename "$skill_dir")
  mkdir -p "$DEST_SKILLS/$skill_name"
  sed 's|\${CLAUDE_PLUGIN_ROOT}/docs/||g' "$skill_dir/SKILL.md" > "$DEST_SKILLS/$skill_name/SKILL.md"
done

# --- Check mode: diff the freshly-synced scratch tree against the committed copies ---
if [ "$CHECK" = 1 ]; then
  # diff returns non-zero on any difference or missing file; -r recurses, -q is terse.
  # The if-condition consumes the exit code, so set -e does not abort here.
  if diff -rq "$DEST_DOCS" "$PLUGIN_DOCS" && diff -rq "$DEST_SKILLS" "$ROOT_SKILLS"; then
    echo "sync check: OK — plugin/docs/ and skills/ are in sync with root"
    exit 0
  fi
  echo "sync check: DRIFT — plugin/docs/ or skills/ is stale; run ./sync-plugin-docs.sh and commit the result" >&2
  exit 1
fi

# --- Verify (apply mode) ---
root_entries=$(grep "^|" "$REPO_ROOT/CATALOG.md" | grep -v "^| Name " | grep -v "^|---" | wc -l | tr -d ' ')
plugin_entries=$(grep "^|" "$PLUGIN_DOCS/CATALOG.md" | grep -v "^| Name " | grep -v "^|---" | wc -l | tr -d ' ')
root_evals=$(ls "$REPO_ROOT/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')
plugin_evals=$(ls "$PLUGIN_DOCS/evaluations/"*.md 2>/dev/null | wc -l | tr -d ' ')
root_discovery=$(ls "$REPO_ROOT/discovery/"*.md 2>/dev/null | wc -l | tr -d ' ')
plugin_discovery=$(ls "$PLUGIN_DOCS/discovery/"*.md 2>/dev/null | wc -l | tr -d ' ')
skill_count=$(ls -d "$PLUGIN_SKILLS"/*/ 2>/dev/null | wc -l | tr -d ' ')

echo "Synced: CATALOG.md ($plugin_entries entries), WORKFLOW.md, evaluations/ ($plugin_evals files), discovery/ ($plugin_discovery files), skills/ ($skill_count skills)"

if [ "$root_entries" != "$plugin_entries" ] || [ "$root_evals" != "$plugin_evals" ] || [ "$root_discovery" != "$plugin_discovery" ]; then
  echo "WARNING: count mismatch after sync — root has $root_entries entries/$root_evals evals/$root_discovery discovery, plugin has $plugin_entries/$plugin_evals/$plugin_discovery"
  exit 1
fi
