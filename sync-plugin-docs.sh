#!/usr/bin/env bash
# Sync root documentation to plugin/docs/ so the installable plugin stays current.
# Also syncs root skills/ from plugin/skills/ (plugin is authoritative for skills).
# Run before publishing or via pre-commit hook.
#
#   ./sync-plugin-docs.sh                # apply: write the synced tree in place
#   ./sync-plugin-docs.sh --check        # verify only: exit 1 if plugin/docs or skills
#                                          would change; mutate nothing (CI/pre-commit gate)
#   ./sync-plugin-docs.sh --list-watched # print the watch set (one entry per line,
#                                          dirs with a trailing /) and exit; the
#                                          harness auto-sync hooks derive their trigger
#                                          predicate from this instead of restating it (#194)
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")" && pwd)"
PLUGIN_DOCS="$REPO_ROOT/plugin/docs"
PLUGIN_SKILLS="$REPO_ROOT/plugin/skills"
ROOT_SKILLS="$REPO_ROOT/skills"

# The watch set — the one definition of what this script mirrors into plugin/docs/.
# The copy loop below iterates these arrays; adapters consume the same set via
# --list-watched (pinned by TestWatchListSeam). The apply-mode verify block at the
# bottom still spot-checks a hand-picked subset — it is a count sanity-check, not
# a second definition of the set.
WATCHED_FILES=(CATALOG.md WORKFLOW.md STACK.md STACK-LEDGER.md NEXT-EVALS.md WATCHLIST.md PLAYBOOK.md)
WATCHED_DIRS=(evaluations discovery methodologies)

CHECK=0
case "${1:-}" in
  --check) CHECK=1 ;;
  --list-watched)
    printf '%s\n' "${WATCHED_FILES[@]}"
    printf '%s/\n' "${WATCHED_DIRS[@]}"
    exit 0
    ;;
esac

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

# --- Docs: root → DEST_DOCS (driven by the watch set, never restated) ---
mkdir -p "$DEST_DOCS"
for f in "${WATCHED_FILES[@]}"; do
  cp "$REPO_ROOT/$f" "$DEST_DOCS/$f"
done
for dir in "${WATCHED_DIRS[@]}"; do
  mkdir -p "$DEST_DOCS/$dir"
  rsync -a --delete "$REPO_ROOT/$dir/" "$DEST_DOCS/$dir/"
done

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
# Entry counts come from catalog_lib.catalog_count — the one implementation of
# "what counts as a catalog row" (#195). A grep here had subtly different
# whitespace rules and could silently diverge.
# Runs from REPO_ROOT so the repo's catalog_lib.py resolves first, wherever the
# caller's cwd is (python3 -c puts cwd at the head of sys.path).
count_catalog_entries() {
  (cd "$REPO_ROOT" && python3 -c '
import sys, catalog_lib
with open(sys.argv[1], encoding="utf-8") as f:
    print(catalog_lib.catalog_count(f.read()))' "$1")
}
root_entries=$(count_catalog_entries "$REPO_ROOT/CATALOG.md")
plugin_entries=$(count_catalog_entries "$PLUGIN_DOCS/CATALOG.md")
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
