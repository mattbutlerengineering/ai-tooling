# Evaluation: friday

**Repo:** [friday-memory/friday](https://github.com/friday-memory/friday)
**Stars:** 36 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

An open-source persistent cognitive memory layer for AI coding agents (Cursor, Claude, Copilot) —
a Neo4j-backed knowledge graph exposed via a FastAPI service and an MCP server, aimed at giving
agents durable, queryable memory across sessions instead of "amnesia" on every restart.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (OMEGA, claude-mem, cognee). That is sufficient to place the
lead against its incumbents, not to support an ADOPT — this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (STACK, Tier 1, `MEASURED`). claude-mem already ships
persistent memory with semantic search, timeline views, and knowledge-graph management for Claude
Code, validated in real testing. friday is a two-day-old repo (36 stars) offering the same
knowledge-graph-backed persistent-memory pitch with no benchmark or differentiation claim beyond
being cross-tool (Cursor/Claude/Copilot). A second unvalidated entrant in an already-crowded
memory cluster (agentmemory, beads, OMEGA, cognee, MemOS, memind, supermemory all compete here)
earns nothing over the validated incumbent.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
