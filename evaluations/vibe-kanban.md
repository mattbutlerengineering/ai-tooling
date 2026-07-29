# Evaluation: vibe-kanban

**Repo:** [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban)
**Stars:** 27,000 | **License:** Apache-2.0
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling (kanban board UI)

---

## What it does

A kanban board to plan, dispatch, and review multiple coding agents (Claude Code, Codex, any) in
parallel. Picked up from the P2 challenger band of the daily discovery-and-triage pass.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`claude-squad`, `agent-orchestrator`, `orca`). `claude-squad`
is KEEP in STACK.md, but it's a lean TUI session manager, not a kanban-style plan/dispatch/review
board — a genuinely different interaction model for coordinating multiple agents, so a mechanical
SKIP isn't defensible from metadata alone.

## Triage note

Left at `discovery-log`: 27K stars and backed by BloopAI (a known dev-tools shop); large and
differentiated enough (visual board vs. TUI) to deserve a real eval rather than a redundancy SKIP.

_Triaged 2026-07-29 by the daily discovery scan's P2-band triage pass._
