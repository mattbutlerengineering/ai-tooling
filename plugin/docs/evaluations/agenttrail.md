# Evaluation: agenttrail

**Repo:** [sodiumsun/agenttrail](https://github.com/sodiumsun/agenttrail)
**Stars:** 84 | **Last updated:** 2026-08-24 (pushed) | **License:** MIT
**Last verified:** 2026-08-24
**Last triaged:** 2026-08-24  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (Reflect/Observability)
**Layer:** Tooling

---

## What it does

A local observability dashboard (MIT) that watches Claude Code, Codex, and Cursor plans,
tool calls, file changes, and progress in real time, across all three tools rather than
one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`. It cites no STACK pick in "Overlaps with" (`zoetrope`,
`claude-devtools`, and `roundtable` are themselves `discovery-log` leads, not adopted
incumbents), so it doesn't clear the P2 challenger bar. Not archived, permissively
licensed, not a vendored skill/plugin Type, no `Ships inside` declared. Cross-tool
(Claude Code + Codex + Cursor in one dashboard) is a real point of differentiation from
the single-tool observability leads already in the catalog, worth a real look rather than
a mechanical disposition.

_Triaged 2026-08-24 by the P3 backlog band (daily discovery)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agenttrail](https://github.com/sodiumsun/agenttrail) | tool | Local observability dashboard (MIT) watching Claude Code, Codex, and Cursor plans, tool calls, file changes, and progress in real time | Agent session progress is a scrolling transcript with no local, cross-tool live view of what tool calls and file changes are actually happening | zoetrope, claude-devtools, roundtable |
