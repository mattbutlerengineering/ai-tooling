#!/bin/bash
# PreToolUse(Bash) gate: block a `git commit` if the offline integrity audit fails.
# Uses --offline (gating detectors B/D/G/J/K/O) so it's fast and works
# with no network; detector A (install resolution, network) is left for CI.
# Fail-open: if the command can't be parsed or isn't a commit, do nothing (exit 0).
# The commit predicate below ("git commit", substring) is pinned in lockstep with
# the opencode commit-gate plugin by TestHookTriggerSeam in test_automation.py (#202).
input=$(cat)
cmd=$(printf '%s' "$input" | python3 "$(dirname "$0")/hook-field.py" command 2>/dev/null)
case "$cmd" in
  *"git commit"*)
    cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
    if ! out=$(python3 audit-evals.py --offline 2>&1); then
      printf 'BLOCKED: integrity audit failed — fix before committing.\n\n%s\n' "$out" >&2
      exit 2   # exit 2 = block the tool call, surface stderr to the agent
    fi
    ;;
esac
exit 0
