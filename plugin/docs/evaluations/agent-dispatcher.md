# Evaluation: agent-dispatcher

**Repo:** [nahid-sparktales/agent-dispatcher](https://github.com/nahid-sparktales/agent-dispatcher)
**Stars:** 30 | **Last updated:** 2026-09-20 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A capability-aware Claude Code dispatcher routing tasks to 27 specialist roles, with
composable skills, MCP/tool routing, verification workflows, and direct role commands.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (crucible, claude-octopus, hubo). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: no overlap cell names a STACK incumbent, so it lands in P3
backlog rather than P2. A 27-role dispatcher with built-in verification workflows is
significant enough on its face to deserve a first-time look rather than a mechanical
disposition. Left for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-dispatcher](https://github.com/nahid-sparktales/agent-dispatcher) | tool | Capability-aware Claude Code dispatcher routing tasks to 27 specialist roles with composable skills and verification workflows | A single agent handles every task the same way, with no role-specific routing, tool/MCP scoping, or verification step | crucible, claude-octopus, hubo |
