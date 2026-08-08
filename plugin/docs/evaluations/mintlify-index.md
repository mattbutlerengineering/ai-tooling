# Evaluation: Mintlify Index

**Repo:** [mintlify/index](https://github.com/mintlify/index)
**Stars:** 31 | **Last updated:** 2026-08-06 (pushed) | **License:** MIT
**Last verified:** 2026-08-08
**Last triaged:** 2026-08-08  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Infrastructure (MCP server)

---

## What it does

A retrieval engine and MCP server from Mintlify for searching documentation, installed via
`npx mint index`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: a dedicated retrieval engine from a documentation-platform vendor
(Mintlify) is a different bet than the existing docs-lookup MCP servers (context7 = live
library docs, ref-tools-mcp = token-efficient search) — worth a first-time eval on retrieval
quality rather than a mechanical redundancy SKIP.

_Triaged 2026-08-08 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Mintlify Index](https://github.com/mintlify/index) | MCP server | Retrieval engine and MCP server (MIT) from Mintlify for searching documentation — install via `npx mint index` | Agents need fast, accurate retrieval over docs without hand-rolling RAG or embeddings | context7, ref-tools-mcp, docmd |
