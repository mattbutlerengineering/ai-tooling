# Evaluation: CallBoard

**Repo:** [AsWali/CallBoard](https://github.com/AsWali/CallBoard)
**Stars:** 15 | **Last updated:** 2026-09-30 (pushed) | **License:** MIT
**Last verified:** 2026-10-03
**Last triaged:** 2026-10-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A shared to-do list for a human and their coding agents, exposed over MCP (Go, ★15,
created 2026-09-28) — a task board a human and several agents can read and write to
instead of relying on ad-hoc todo lists.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new today (created 2026-09-28, discovered in the daily scan). Its "Overlaps with"
cell names `succubus`, `tasktrooper`, and `agent-track` — none of which is a STACK pick,
so this does not band as a P2 challenger. No archived flag, no disqualifying license, no
`Ships inside` container. Left at `discovery-log` for a real hands-on eval rather than a
mechanical disposition on day one.

_Triaged 2026-10-03 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CallBoard](https://github.com/AsWali/CallBoard) | MCP server | Shared to-do list (MIT) exposed over MCP so you and your coding agents work off one task board | Coordinating tasks between a human and several coding agents has no shared, inspectable board, only ad-hoc todo lists | succubus, tasktrooper, agent-track |
