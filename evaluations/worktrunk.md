# Evaluation: worktrunk

**Repo:** [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk)
**Stars:** 5,495 | **Last updated:** 2026-06-17 | **License:** proprietary
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

CLI for managing git worktrees, designed specifically for parallel AI agent workflows. Creates, lists, switches between, and cleans up worktrees. Wraps `git worktree` commands into a streamlined workflow so you can run multiple agents on different branches simultaneously without git conflicts.

## How we tested it

**Evidence:** REVIEW

**README/CLI-surface review — not run.** worktrunk wraps git worktrees to give each parallel agent session its own branch+worktree; a real test means driving multiple concurrent agent sessions, not done here. Documented lifecycle:

```
worktrunk new feat/auth         # creates worktree + branch in one step
worktrunk new feat/api-routes
worktrunk list                  # active worktrees with status
worktrunk clean                 # removes merged/stale worktrees
```

The create/list/switch/cleanup flow below is from the documented command surface, not an observed multi-session run.

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

**discovery-log — tentative read**

Adopt if running 3+ parallel agent sessions regularly — the worktree lifecycle management saves meaningful time and prevents the git state tangles that plague raw `git worktree` usage. Skip for solo sequential work where `git worktree add/remove` suffices. The proprietary license is a risk factor; if an open-source alternative emerges with similar UX, prefer that.

## Triage note

Left at `discovery-log`, examined and not disposed. The tentative read above already does the hard
part — parallel-agent worktree lifecycle management, worth it at 3+ concurrent sessions, `git worktree
add/remove` sufficient below that — so there is nothing this lane can add by way of elimination.

The one thing worth re-stating from the header rather than the prose: the licence is **proprietary**.
That is the single fact most likely to decide this row, and per the adoption bar it forecloses ADOPT
regardless of how well the tool works. The verdict names an open-source alternative as the preferred
outcome if one appears; nothing in this pass found one.

Not SKIPped, because the capability is real and there is no catalogued incumbent to be redundant with.
Promotion would need a hands-on run *and* a licence the bar accepts — the second is not ours to fix,
which makes this a watch rather than a queue item.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

**Re-triaged 2026-09-04 by the P3 backlog band (daily discovery pass):** no change — still proprietary-licensed with no catalogued incumbent to be redundant with; the watch-for-an-OSS-alternative posture from the prior pass still holds, and this pass found none.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | CLI for git worktree management, designed for parallel AI agent workflows | Raw git worktree commands are error-prone when running multiple agents | — |
