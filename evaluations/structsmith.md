# Evaluation: StructSmith

**Repo:** [dziksu/StructSmith](https://github.com/dziksu/StructSmith)
**Stars:** 10 | **Last updated:** 2026-09-09 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Local-first, MCP-native tool for modelling software architecture — a C4-style semantic
model with a React Flow visual editor, SQLite storage, and a single-container deploy. Pitched
as a self-hosted Structurizr alternative an AI client can read and edit live over MCP, rather
than a static diagram file.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `codegraph`. codegraph auto-syncs a
code knowledge graph from the *existing* codebase for agent retrieval; StructSmith is for
*modelling* system architecture (C4-style diagrams an agent can edit live over MCP), a
design/planning artifact rather than an indexed-retrieval substrate. Different job, worth its
own look. Very early (10★, created this week) — a real eval should wait for more usage signal
or install it directly to confirm the MCP-editable-diagram claim.

_Triaged 2026-09-09 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [StructSmith](https://github.com/dziksu/StructSmith) | tool | Local-first, MCP-native architecture-modeling tool (MIT) — C4-style semantic model, React Flow editor, SQLite, single container | Architecture diagrams drift from the real system and agents can't edit them; want a self-hosted Structurizr alternative live over MCP | Understand-Anything, codegraph, graphify |
