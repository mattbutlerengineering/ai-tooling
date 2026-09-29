# Evaluation: Recollect

**Repo:** [MikeK184/Recollect](https://github.com/MikeK184/Recollect)
**Stars:** 40 | **Last updated:** 2026-09-26 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-29
**Last triaged:** 2026-09-29  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

Self-hosted AI memory and MCP coordination for coding agents, built in Rust for Codex and Claude Code. Persistent context across repositories and sessions, backed by knowledge graphs (Neo4j) and hybrid search (pgvector), with a desktop web UI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

Cites claude-mem (STACK ADOPT) in Overlaps with, which bands this P2 challenger. Not SKIPped as redundant: claude-mem is a zero-friction npm plugin with no external dependencies, while Recollect's stated design is a self-hosted knowledge-graph store (Neo4j + pgvector hybrid search) coordinating memory across repositories via MCP — the same heavier-infrastructure differentiation that kept cognee at discovery-log rather than SKIPped. Newly catalogued (added 2026-09-29), 40 stars, 10 days old. Left at discovery-log for a future hands-on look rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Recollect](https://github.com/MikeK184/Recollect) | tool | Self-hosted AI memory + MCP coordination (Apache-2.0, Rust) — knowledge graphs, hybrid search, desktop UI | Coding-agent context/memory is siloed per repo and session with no persistent, queryable store | claude-mem, OMEGA, agentic-stack-desktop |
