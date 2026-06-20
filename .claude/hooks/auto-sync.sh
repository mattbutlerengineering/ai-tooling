#!/bin/bash
# PostToolUse(Edit|Write) auto-sync: when a root doc that sync-plugin-docs.sh mirrors
# is edited, re-run the sync so plugin/docs/ never drifts. Fail-open and silent.
input=$(cat)
fp=$(printf '%s' "$input" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tool_input',{}).get('file_path',''))" 2>/dev/null)
case "$fp" in
  */CATALOG.md|*/WORKFLOW.md|*/STACK.md|*/evaluations/*.md)
    # ignore edits already inside plugin/docs (would be a no-op loop anyway)
    case "$fp" in */plugin/docs/*) exit 0 ;; esac
    cd "${CLAUDE_PROJECT_DIR:-.}" && ./sync-plugin-docs.sh >/dev/null 2>&1
    ;;
esac
exit 0
