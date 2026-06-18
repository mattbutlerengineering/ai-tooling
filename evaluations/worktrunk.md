# Evaluation: worktrunk

**Repo:** [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk)
**Stars:** 5,495 | **Last updated:** 2026-06-17 | **License:** proprietary
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

CLI for managing git worktrees, designed specifically for parallel AI agent workflows. Creates, lists, switches between, and cleans up worktrees. Wraps `git worktree` commands into a streamlined workflow so you can run multiple agents on different branches simultaneously without git conflicts.

## How we tested it

Used worktrunk to manage 3 parallel agent sessions, each working on a different feature branch in its own worktree. Tested the create, list, switch, and cleanup lifecycle.

```
worktrunk new feat/auth         # creates worktree + branch in one step
worktrunk new feat/api-routes
worktrunk new feat/tests
worktrunk list                  # shows all active worktrees with status
worktrunk clean                 # removes merged/stale worktrees
```

## What worked

- `worktrunk new` combines worktree creation and branch setup in one step — cleaner than raw `git worktree add -b`
- `worktrunk list` shows meaningful status (branch, last commit, dirty state) vs. `git worktree list`'s bare paths
- Automatic cleanup of stale worktrees after branches are merged — no manual `git worktree remove`
- Handles the edge cases that trip up raw git worktree usage (nested worktrees, locked worktrees, orphaned paths)
- Fast — all operations complete in under a second

## What didn't work or surprised us

- Proprietary license — cannot fork if the project is abandoned (5.5K stars is solid but not guaranteed longevity)
- The real value only appears at 3+ parallel agents — with 1-2, raw `git worktree` commands are manageable
- No integration with claude-squad or other multi-agent managers (you manage worktrees and agents separately)
- `worktrunk clean` is aggressive by default — it removed a worktree for a branch that was merged upstream but had local uncommitted changes

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't affect code quality directly |
| Speed | + | Reduces friction of parallel agent workflows |
| Maintainability | neutral | No impact on code structure |
| Safety | - | Aggressive cleanup can discard uncommitted work if you're not careful |
| Cost Efficiency | neutral | Doesn't affect token usage |

## Verdict

**CONDITIONAL**

Adopt if running 3+ parallel agent sessions regularly — the worktree lifecycle management saves meaningful time and prevents the git state tangles that plague raw `git worktree` usage. Skip for solo sequential work where `git worktree add/remove` suffices. The proprietary license is a risk factor; if an open-source alternative emerges with similar UX, prefer that.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | CLI for git worktree management, designed for parallel AI agent workflows | Raw git worktree commands are error-prone when running multiple agents | — |
