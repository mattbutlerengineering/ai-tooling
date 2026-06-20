# Evaluation: haystack

**Repo:** [deepset-ai/haystack](https://github.com/deepset-ai/haystack)
**Stars:** ~25,600 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An open-source AI orchestration framework (Python) for building production-ready LLM applications, from deepset. Haystack's model is **modular pipelines**: you compose components with explicit control over retrieval, routing, memory, and generation, in a transparent architecture you can inspect and customize.

It targets a broad surface: RAG systems, semantic search, question answering, multimodal applications, conversational systems, and autonomous agents. The emphasis is on explicit, debuggable control flow — you wire components into pipelines (and agent workflows) rather than relying on an opaque agent loop, so you can experiment, customize deeply, and deploy with confidence. There's also a commercial "Haystack Enterprise" support/platform tier on top of the OSS framework.

## How we tested it

Architecture review against the README and the documented pipeline/component model. Confirmed the modular-pipeline architecture with explicit retrieval/routing/memory/generation control, the breadth (RAG, search, QA, multimodal, agents), the Python/pip install path, and the OSS vs. Enterprise split. Not built a live pipeline, so condition-gated.

```bash
gh api repos/deepset-ai/haystack --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/deepset-ai/haystack/readme --jq '.content' | base64 -d
```

## What worked

- **Explicit, transparent pipelines.** Wiring retrieval/routing/memory/generation as visible components is more debuggable and customizable than black-box agent loops — a real maintainability and trust win for production.
- **Mature and broad.** A long-standing framework (deepset) covering RAG, search, QA, multimodal, and agents — proven and well-documented, not a weekend project.
- **Production-oriented.** Designed for scalable deployment with an enterprise support path for teams that need it.

## What didn't work or surprised us

- **Heavier than a thin agent lib.** The pipeline abstraction has a learning curve; for a quick single-agent task it's more than you need.
- **Python-centric.** Best fit for Python stacks; TS teams will look to agent-kit/voltagent.
- **Overlaps LangChain/LlamaIndex.** The orchestration-framework space is crowded; Haystack's edge is the explicit, transparent pipeline model and deepset's production focus.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Explicit retrieval/routing control reduces opaque failure modes |
| Speed | neutral | Framework ergonomics; runtime depends on your components |
| Maintainability | + | Transparent, modular pipelines are inspectable and testable |
| Safety | + | Explicit control flow makes agent behavior easier to constrain |
| Cost Efficiency | neutral | OSS; deeper support is the paid Enterprise tier |

## Verdict

**CONDITIONAL**

Adopt for Python teams building production RAG/search/agent applications that want explicit, transparent, modular pipelines over opaque agent frameworks. For quick prototypes or TS stacks, lighter options fit better. Compare against LangChain/LlamaIndex for the orchestration slot; Haystack's transparency and production lineage are its selling points.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [haystack](https://github.com/deepset-ai/haystack) | framework | Production LLM orchestration framework (Apache-2.0, ★26K, by deepset) — modular, transparent pipelines with explicit control over retrieval, routing, memory, and generation; RAG, semantic search, QA, multimodal, and agents in Python | Black-box agent frameworks hide retrieval/routing/memory; want explicit, modular pipelines to experiment and deploy with confidence | pydantic-ai, voltagent, agent-kit, LightRAG |
