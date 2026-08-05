# Evaluation: assistant-ui

**Repo:** [assistant-ui/assistant-ui](https://github.com/assistant-ui/assistant-ui)
**Stars:** 11,408 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

TypeScript/React primitives for building AI chat interfaces that render tool calls and JSON as live interactive components, with inline human-in-the-loop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "**Typescript/React Library for AI Chat**" — the chat surface of an application you ship. It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [assistant-ui](https://github.com/assistant-ui/assistant-ui) | framework | TypeScript/React primitives that render tool calls and JSON as live components, with inline HITL (MIT, ★11K) | Building an AI chat UI that renders rich interactive components and pauses for human approval is bespoke | CopilotKit, tambo, vercel-ai |
