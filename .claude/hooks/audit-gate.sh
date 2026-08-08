#!/bin/bash
# PreToolUse(Bash) gate: block a `git commit` if the repo's offline data gates fail.
#
# It runs `make check-data` — the ONE definition of that set, shared with CI and with
# the opencode commit-gate plugin. It used to run `python3 audit-evals.py --offline`
# alone, which is 1 of the 13 gates `make check` enforces, while this comment claimed it
# ran "the offline subset" of them (#459). Every gate added since then widened the hole
# silently: a stale NEXT-EVALS.md, a desynced plugin/docs/, a missing **Stars:** line, a
# dead relative link and a stale WATCHLIST.md all passed here and failed CI. Delegating
# is the rule CLAUDE.md already states for every other hook: the opencode plugins, the
# .claude/hooks scripts and CI call the same scripts, so there is one implementation.
#
# Detector A (install resolution) stays out — it needs the network. So do ruff/mypy
# (they need the pinned dev venv) and the unit suite (15.9s, and it tests the scripts
# rather than the tree). `make check-data` runs in a median 4.0s against 0.55s for the
# one gate this used to run, which is what keeps it usable as a commit gate at all.
#
# **"Could not run" is not "failed."** The preconditions are checked explicitly — make,
# python3, the Makefile, the target — and any one of them missing exits 0 rather than
# blocking, so a contributor without the toolchain can still commit and the installed
# plugin firing in someone else's repo is a silent no-op. Exit codes cannot carry that
# distinction (make exits non-zero for a missing target and for a real finding alike),
# so it is decided BEFORE the run, never inferred from it. Once those hold, a non-zero
# exit is a genuine finding and blocks.
#
# The commit predicate below ("git commit", substring) is pinned in lockstep with
# the opencode commit-gate plugin by TestHookTriggerSeam in test_automation.py (#202).
input=$(cat)
cmd=$(printf '%s' "$input" | python3 "$(dirname "$0")/hook-field.py" command 2>/dev/null)
case "$cmd" in
  *"git commit"*)
    cd "${CLAUDE_PROJECT_DIR:-.}" || exit 0
    command -v make >/dev/null 2>&1 || exit 0
    command -v python3 >/dev/null 2>&1 || exit 0
    grep -q '^check-data:' Makefile 2>/dev/null || exit 0
    if ! out=$(make --no-print-directory check-data 2>&1); then
      printf 'BLOCKED: integrity audit failed — fix before committing.\n\n%s\n' "$out" >&2
      exit 2   # exit 2 = block the tool call, surface stderr to the agent
    fi
    ;;
esac
exit 0
