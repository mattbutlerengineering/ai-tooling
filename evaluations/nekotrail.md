# Evaluation: nekotrail

**Repo:** [Harshil-Jani/nekotrail](https://github.com/Harshil-Jani/nekotrail)
**Stars:** 5 | **Last updated:** 2026-11-12 (pushed) | **License:** MIT
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Runs Claude Code, Codex, and 14 more coding agents at once, in parallel git worktrees on
the user's own logins, advertised as a free, open-source alternative to the commercial
"Conductor" app, per the repo's own description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`. The parallel-worktree-manager job is crowded (`claude-squad`,
`worktrunk`, `agent-of-empires`, `orca`, `gastown`, and more), but none of those is a
STACK ADOPT/KEEP incumbent — `claude-squad` is `CONDITIONAL`, the rest are
`discovery-log` themselves — so there is no single incumbent this lead is redundant
against. Breadth (16+ agents, no-account, free) is a plausible differentiator worth a
real eval rather than a crowded-category SKIP.
