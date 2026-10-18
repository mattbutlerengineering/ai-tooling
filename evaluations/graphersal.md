# Evaluation: graphersal

**Repo:** [graphersal/graphersal](https://github.com/graphersal/graphersal)
**Stars:** 15 | **Last updated:** 2026-10-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

An in-memory graph database and Gremlin traversal engine written in Rust, shipping a browser
playground, CLI, MCP server for AI agents, a durable store, and Python bindings — infrastructure
for standing up GraphRAG/knowledge-graph storage rather than a packaged memory product.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and GitHub repo metadata (stars, license, activity). No hands-on run was performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

P3 backlog, oldest-untriaged (no prior eval file). Not a P2 challenger: its cited peers
(`cognee`, `LightRAG`, `OMEGA`) are themselves `discovery-log` leads or MCP-server entries, not
a STACK pick this tool is redundant with — graphersal is a general-purpose graph-DB engine
(Gremlin/TinkerPop-compatible) rather than a packaged agent-memory product, a different layer
than the memory tools it's filed next to. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [graphersal](https://github.com/graphersal/graphersal) | tool | In-memory graph DB + Gremlin traversal engine in Rust (Apache-2.0) shipping an MCP server, browser playground, and Python bindings | Standing up GraphRAG/knowledge-graph storage for agents means assembling a DB plus an MCP layer from scratch | cognee, LightRAG, OMEGA |  |
