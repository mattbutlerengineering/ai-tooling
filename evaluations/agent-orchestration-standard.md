# Evaluation: agent-orchestration-standard

**Repo:** [tomtomsatnav/agent-orchestration-standard](https://github.com/tomtomsatnav/agent-orchestration-standard)
**Stars:** 71 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local-first dashboard (plugin + terminal UI + MCP server) graphing Claude Code
sessions — agent tree, tokens, tool feed, replay, alerts — and defining the AOS-1 agent
orchestration spec alongside it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-18). Differentiator over `bar-observatory`/`tracecrate` is the
project-graph/replay dashboard plus a named orchestration spec (AOS-1), rather than a pure
log-diffing workbench. No archived flag, no disqualifying license, no `Ships inside`
container, zero overlap pressure. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-orchestration-standard](https://github.com/tomtomsatnav/agent-orchestration-standard) | tool | Local-first dashboard (MIT) — plugin + terminal UI + MCP server — graphing Claude Code sessions' agent tree, tokens, tool feed, replay, and alerts; includes the AOS-1 spec | No single live view of what parallel Claude Code sessions are doing, costing, or replaying after the fact | bar-observatory, tracecrate, claude-super-sidebar |
