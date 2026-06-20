# Evaluation: LightRAG

**Repo:** [HKUDS/LightRAG](https://github.com/HKUDS/LightRAG)
**Stars:** ~36,800 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement (retrieval / Memory & Context)
**Layer:** Infrastructure

---

## What it does

A simple, fast graph-based RAG framework (EMNLP 2025). Instead of flat vector chunks, LightRAG extracts a knowledge graph (entities + relationships) from your documents and performs **dual-level retrieval** — low-level (specific entities) and high-level (broader themes/relationships) — so retrieval captures how facts connect, not just surface similarity.

Per the changelog, it now includes: **multimodal content parsing** (MinerU/Docling services, with RAG-Anything merged in), four selectable text-chunking strategies (Fix/Recursive/Vector/Paragraph), **role-specific LLM configuration** (independent models for EXTRACT/QUERY/KEYWORDS/VLM roles), OpenSearch as a unified storage backend, and a Docker setup wizard for local embedding/reranking/storage. You ingest documents, LightRAG builds and incrementally updates the graph, and queries traverse both the graph and vector layers.

## How we tested it

Architecture review against the README/changelog and the documented dual-level graph-retrieval design. Confirmed the knowledge-graph + vector hybrid, the multimodal parsing (post RAG-Anything merge), the role-specific LLM config, the chunking strategies, and the pluggable storage backends. The EMNLP/benchmark claims are the project's own. Not run on a live corpus, so condition-gated.

```bash
gh api repos/HKUDS/LightRAG --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/HKUDS/LightRAG/readme --jq '.content' | base64 -d
```

## What worked

- **Graph structure captures relationships.** Entity/relationship extraction + dual-level retrieval surfaces connected context that flat vector RAG misses — strong for multi-hop questions over connected documents.
- **Incremental and configurable.** Incremental graph updates plus role-specific LLM config (cheap model for extraction, strong model for query) is a sensible cost/quality split.
- **Multimodal + storage flexibility.** Absorbing RAG-Anything (MinerU/Docling) and supporting OpenSearch/Docker makes it a fuller pipeline than a toy RAG.

## What didn't work or surprised us

- **Graph construction cost.** Extracting entities/relationships across a corpus is LLM-heavy up front — more expensive to index than plain embedding.
- **Operational surface.** Multiple storage backends, chunking strategies, and role configs mean real setup/tuning; it's a framework, not a one-liner.
- **Overlaps PageIndex/cognee.** All three move beyond flat vector RAG; LightRAG's edge is the entity-relationship graph + dual-level retrieval (vs. PageIndex's reasoning-over-tree, cognee's memory platform).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Graph + dual-level retrieval improves multi-hop/connected-context answers |
| Speed | neutral | Fast queries; graph indexing is the up-front cost |
| Maintainability | + | Incremental updates; pluggable storage and chunking |
| Safety | neutral | Retrieval layer; no direct safety effect |
| Cost Efficiency | neutral | Role-specific LLMs help, but graph extraction is token-heavy |

## Verdict

**CONDITIONAL**

Adopt for RAG over connected document corpora where relationships and multi-hop reasoning matter and you can absorb the up-front graph-extraction cost. For long single documents needing explainable retrieval, PageIndex is the reasoning-over-structure alternative; for plain Q&A, flat vector RAG is cheaper. Pilot on a representative corpus and tune the role-specific LLM config to control indexing spend.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [LightRAG](https://github.com/HKUDS/LightRAG) | tool | Simple, fast graph-based RAG (MIT, ★37K, EMNLP 2025) — knowledge graph + dual-level (local/global) retrieval instead of flat vector chunks; multimodal parsing (MinerU/Docling), role-specific LLM config, pluggable storage | Flat vector RAG misses entity relationships and global context; want graph-structured, incremental retrieval | PageIndex, cognee, memU, ragas |
