# Evaluation: llama_index

**Repo:** [run-llama/llama_index](https://github.com/run-llama/llama_index)
**Stars:** 51,375 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A framework for building document-centric LLM applications — indexing, retrieval, RAG and document agents. The repository describes itself as "the leading document agent and OCR platform".

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "the leading document **agent and OCR platform**" — product infrastructure for document applications. It is the canonical RAG-framework peer of `langchain`, which this catalog SKIPped as "app-building framework, not a dev-loop tool", and its `Overlaps with` cell names `langchain` first.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

The `haystack` eval, SKIPped in this same pass, tells its reader to "compare against LangChain/LlamaIndex for the orchestration slot" — all three are the same artifact, and it would be incoherent to dispose two and keep the third.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [llama_index](https://github.com/run-llama/llama_index) | framework | Leading data framework for LLM apps (MIT, ★50K) — document ingestion/parsing (LlamaParse), indexing, retrieval, and document agents for RAG over your own data | Building RAG/document-agent applications over private data (general LLM-app framework, out of dev-loop scope) | langchain, haystack, RAGFlow, cognee |
