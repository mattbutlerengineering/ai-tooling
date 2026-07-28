# Evaluation: vibe-kanban

**Repo:** [BloopAI/vibe-kanban](https://github.com/BloopAI/vibe-kanban)
**Stars:** ~27,322 | **Last updated:** 2026-04-24 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A kanban board to plan, dispatch, and review multiple coding agents (Claude Code, Codex, any) in parallel — turns ad-hoc multi-agent dispatch into a trackable visual board.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: `repo-metadata.json` (27.3K stars, Apache-2.0, pushed 2026-04-24) plus the CATALOG "Overlaps with" cell against claude-squad/agent-orchestrator/orca.

## Triage note

P2 challenger band (overlaps claude-squad, a STACK pick), but vibe-kanban's kanban-board UX for dispatching/tracking agents is a materially different paradigm from claude-squad's TUI session manager, and at 27K stars it's a major, well-adopted project in its own right — not plainly dominated. Left at discovery-log for a future hands-on eval.
