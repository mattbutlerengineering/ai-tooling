# Evaluation: flow (Aixle)

**Repo:** [AixleHQ/flow](https://github.com/AixleHQ/flow)
**Stars:** 4 | **Last updated:** 2026-08-07 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-07
**Last triaged:** 2026-08-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure (self-hosted app)

---

## What it does

A self-hosted Rails app orchestrating coding agents (Claude Code, Codex, Gemini CLI, Cursor)
through durable, Temporal-backed, inspectable workflows with a kanban view.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (sandcastle, deer-workflow, cee, orca). That
is sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: sandcastle/deer-workflow/cee are TypeScript/Go orchestration
frameworks you embed in your own code, not self-hosted apps; orca is a fleet-of-agents IDE,
not a durable-execution engine. A Temporal-backed durable workflow engine purpose-built for
coding-agent tasks is a real differentiator worth a hands-on eval rather than a redundancy
SKIP, though the very low star count (4, one day old) argues for waiting to see if it gets
traction before spending eval time on it.

_Triaged 2026-08-07 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [flow (Aixle)](https://github.com/AixleHQ/flow) | platform | Self-hosted Rails app (Apache-2.0) orchestrating coding agents (Claude Code, Codex, Gemini CLI, Cursor) through durable, Temporal-backed, inspectable workflows with a kanban view | Coding-agent orchestration scripts aren't durable or inspectable across failures; want a self-hosted workflow engine purpose-built for agent tasks | sandcastle, deer-workflow, cee, orca |
