# Evaluation: json-render

**Repo:** [vercel-labs/json-render](https://github.com/vercel-labs/json-render)
**Stars:** 15,825 | **Last updated:** 2026-07-08 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A generative-UI framework in which the model emits a JSON UI tree that is rendered to React, Vue, Svelte, Solid or React Native.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "**The Generative UI framework**". It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

At ★15.8K it is the most-starred row in the cluster, which is worth stating plainly because popularity is the one thing that might make a reader question the call. It is not an input: `dify`, `Flowise` and `langchain` were all SKIPped at comparable or greater scale, and `langflow` is SKIPped in this same pass at ★152K. Scope is not a function of adoption.

Same vendor as `vercel/ai`, which is the one framework this lane has left at `discovery-log` on a genuine dev-loop bridge, and `vercel/workflow`, which was SKIPped alongside these. Three Vercel rows, three separate determinations.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [json-render](https://github.com/vercel-labs/json-render) | framework | Generative-UI framework (Vercel Labs) — model emits a JSON UI tree rendered to React/Vue/Svelte/Solid/RN (Apache-2.0, ★15.5K) | Driving real UI components from LLM output portably across frontends needs hand-built spec plumbing | tambo, hashbrown, OpenGenerativeUI, openui (ext.) |
