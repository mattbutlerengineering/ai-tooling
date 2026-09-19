# Evaluation: EvoOntology

**Repo:** [ruc-datalab/EvoOntology](https://github.com/ruc-datalab/EvoOntology)
**Stars:** 177 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A self-evolving ontology layer, shipped as a Claude Code/Codex plugin, that exposes versioned
semantic knowledge of heterogeneous tables, files, and databases to data agents via MCP tools —
continuously adapting the ontology based on observed execution behavior instead of a static schema.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (cognee, OMEGA, open-index). That is sufficient to place the
lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: overlaps `OMEGA` (KEEP/STACK) and `cognee` on the general "persistent,
queryable agent memory/knowledge graph" theme, but EvoOntology's specific job — a *versioned
ontology over heterogeneous tables/files/DBs for data agents*, adapting from execution behavior —
is a narrower, data-engineering-specific niche rather than general cross-session dev-agent memory.
Not clearly dominated by the general-purpose memory incumbent; worth a first-time look.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
