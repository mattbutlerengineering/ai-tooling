# Evaluation: langflow

**Repo:** [langflow-ai/langflow](https://github.com/langflow-ai/langflow)
**Stars:** 152,841 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A visual builder for AI-powered agents and workflows.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "a powerful tool for **building and deploying AI-powered agents and workflows**", and its `Overlaps with` cell names `Flowise`, `dify`, `LangGraph` and `crewAI` — **all four already SKIPped on this exact ground**. It is one of five agent/AI application platforms disposed together in this pass (`langflow`, `activepieces`, `onyx`, `mindsdb/minds`, `sim`), the same class as `dify` and `Flowise` — which the catalog already SKIPped with the note that they are "for building AI products, not for making developers more productive with AI coding agents".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

At ★152.8K this is the most-starred row this lane has disposed, by a wide margin. It changes nothing: the four tools its own overlaps cell names as its peers were SKIPped at every scale, and the `Flowise` eval's reasoning applies verbatim — hard-to-diff visual flows "actively cut against the engineering discipline (versioning, review, testing) the catalog's quality signals reward".

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [langflow](https://github.com/langflow-ai/langflow) | platform | Visual low-code builder for AI agents and workflows (MIT, ★150K) — drag-and-drop components across any model/vector DB/API, then deploy the flow as an API or MCP server | Want to prototype and ship agent/RAG workflows visually without wiring a framework by hand (out of dev-loop scope) | Flowise, dify, LangGraph, crewAI |
