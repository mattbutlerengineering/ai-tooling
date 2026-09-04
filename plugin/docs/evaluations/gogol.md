# Evaluation: gogol

**Repo:** [tcmug/_gogol](https://github.com/tcmug/_gogol)
**Stars:** 0 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Semantic search and knowledge store using local llama.cpp embeddings. Indexes code and files so agents can query, explore definitions, trace call graphs, and manage memory notes via CLI or MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog). Sits near `semble`/`lean-ctx`/`heimdall` (local, CPU-friendly semantic code search + memory), but is brand new and unstarred; no basis yet for a redundancy call. Leaving for a real eval to check whether the local-embeddings approach differentiates it from the incumbents.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gogol](https://github.com/tcmug/_gogol) | tool | Semantic search and knowledge store (MIT) using local llama.cpp embeddings — indexes code and files so agents can query, explore definitions, trace call graphs, and manage memory notes via CLI or MCP | Grep-based code search misses semantic matches and agents have no durable memory notes; want one local embeddings store for both | semble, lean-ctx, heimdall, mex |
