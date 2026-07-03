#!/bin/bash
# PostToolUse(Edit|Write) auto-sync: when a root doc that sync-plugin-docs.sh mirrors
# is edited, re-run the sync so plugin/docs/ never drifts. Fail-open and silent.
#
# The trigger set is DERIVED from `sync-plugin-docs.sh --list-watched` — the one
# definition of the syncable set — never restated here (#194, pinned by
# TestWatchListSeam in test_automation.py).
input=$(cat)
fp=$(printf '%s' "$input" | python3 "$(dirname "$0")/hook-field.py" file_path 2>/dev/null)
[ -z "$fp" ] && exit 0
# ignore edits already inside plugin/docs (would be a no-op loop anyway)
case "$fp" in */plugin/docs/*) exit 0 ;; esac

root="${CLAUDE_PROJECT_DIR:-.}"
watched=$("$root/sync-plugin-docs.sh" --list-watched 2>/dev/null) || exit 0

while IFS= read -r entry; do
  [ -z "$entry" ] && continue
  case "$entry" in
    */) # watched directory: any file under it
        dir="${entry%/}"
        case "$fp" in "$dir"/*|*/"$dir"/*) ;; *) continue ;; esac ;;
    *)  # watched root file: match by basename
        case "$fp" in "$entry"|*/"$entry") ;; *) continue ;; esac ;;
  esac
  cd "$root" && ./sync-plugin-docs.sh >/dev/null 2>&1
  break
done <<EOF
$watched
EOF
exit 0
