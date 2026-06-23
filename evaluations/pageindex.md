# Evaluation: PageIndex

**Repo:** [VectifyAI/PageIndex](https://github.com/VectifyAI/PageIndex)
**Stars:** ~33,200 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement (retrieval / Memory & Context)
**Layer:** Infrastructure

---

## What it does

A vectorless, reasoning-based RAG system. Instead of embedding-and-chunking, PageIndex builds a hierarchical "table-of-contents" tree index from a long document, then has an LLM **reason over that tree via tree search** to find the relevant sections.

Mechanically it's two steps: (1) generate a tree-structure index (a ToC-like hierarchy of natural document sections, no artificial chunks); (2) perform reasoning-based retrieval by having the LLM navigate the tree — like a human expert flipping to the right chapter/section. Because retrieval is grounded in explicit page/section references, it's traceable and explainable ("no vibe retrieval"). The thesis: similarity ≠ relevance, and relevance on professional documents requires reasoning, not nearest-neighbor vectors. It reports SOTA 98.7% on FinanceBench. There's a self-host open-source repo (standard PDF parsing), a cloud service with enhanced OCR/tree-building, a chat platform, and MCP/API integration. A "PageIndex File System" extends the tree across an entire corpus, and an agentic vectorless RAG example uses the OpenAI Agents SDK.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the documented two-step retrieval pipeline, the deployment options, and the FinanceBench claim. Confirmed the no-vector/no-chunk design, the tree-search retrieval mechanism, the traceability story (page/section grounding), and the self-host vs. cloud split. The 98.7% benchmark is the project's own published result (vs. a separate Mafin2.5 repo) — not independently reproduced. Not run on a live corpus, so condition-gated.

```bash
gh api repos/VectifyAI/PageIndex --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/VectifyAI/PageIndex/readme --jq '.content' | base64 -d
```

## What worked

- **Traceable, explainable retrieval.** Every result is grounded in explicit page/section references, so you can audit *why* something was retrieved — a real correctness/debuggability win over opaque vector top-k.
- **No vector DB, no chunking.** Removes embedding infra, chunk-boundary tuning, and re-embedding migrations; documents stay in natural sections.
- **Strong fit for long professional documents.** The reasoning-over-structure approach targets exactly where similarity search fails (finance/legal/technical docs needing multi-step reasoning).

## What didn't work or surprised us

- **Reasoning retrieval costs LLM calls.** Tree search spends model tokens per query, so latency/cost can exceed a vector lookup — the tradeoff is accuracy/traceability for compute.
- **Best results need the cloud pipeline.** The self-host repo uses "standard PDF parsing"; enhanced OCR/tree-building (and the headline accuracy) lean on the cloud service.
- **Benchmark is self-reported.** Treat 98.7% as directional until validated on your documents.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reasoning-based, page-grounded retrieval targets relevance over similarity |
| Speed | - | Tree-search reasoning adds LLM calls vs. a vector lookup |
| Maintainability | + | No embeddings/chunking/vector DB to tune or migrate |
| Safety | + | Traceable retrieval makes results auditable, not opaque |
| Cost Efficiency | ✓/$ | Self-host is free; per-query reasoning and cloud OCR add cost |

## Verdict

**CONDITIONAL**

Adopt for retrieval over long, high-stakes professional documents where relevance and explainability matter more than per-query latency/cost. For high-volume, low-stakes retrieval, classic vector RAG is cheaper. Pilot the self-host repo first; reach for the cloud pipeline when OCR quality and peak accuracy justify it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [PageIndex](https://github.com/VectifyAI/PageIndex) | tool | Vectorless, reasoning-based RAG (MIT, ★33K) — hierarchical tree index + LLM tree search for traceable, context-aware retrieval, no vector DB or chunking; reports SOTA 98.7% on FinanceBench | Vector similarity ≠ relevance on long professional docs; want explainable retrieval without embeddings/chunks | cognee, memU, ref-tools-mcp, context7 |
