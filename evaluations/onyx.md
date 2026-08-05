# Evaluation: onyx

**Repo:** [onyx-dot-app/onyx](https://github.com/onyx-dot-app/onyx)
**Stars:** 31,423 | **Last updated:** 2026-08-05 (pushed) | **License:** NOASSERTION (GitHub could not parse the LICENSE file)
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An open-source AI chat platform with enterprise search and connectors, working across any LLM.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "**Open Source AI Platform — AI Chat** with advanced features that works with every LLM", and its `Overlaps with` cell names `cherry-studio` and `lobehub`. The `dify` eval disposed of that pair explicitly — "Like **cherry-studio (SKIP)** and **lobehub (SKIP)**, it's for building AI products, not for making developers more productive with AI coding agents". It is one of five agent/AI application platforms disposed together in this pass (`langflow`, `activepieces`, `onyx`, `mindsdb/minds`, `sim`), the same class as `dify` and `Flowise` — which the catalog already SKIPped with the note that they are "for building AI products, not for making developers more productive with AI coding agents".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

The `NOASSERTION` is not part of this disposal, for the same reason recorded on `hashbrown` and `activepieces`.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [onyx](https://github.com/onyx-dot-app/onyx) | platform | Open-source enterprise AI chat platform — multi-LLM, connectors, and document retrieval | Teams need a self-hostable, production-grade AI assistant grounded in internal docs, not just a demo chat UI | cherry-studio, lobehub |
