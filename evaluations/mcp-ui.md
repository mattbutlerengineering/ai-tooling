# Evaluation: mcp-ui

**Repo:** [MCP-UI-Org/mcp-ui](https://github.com/MCP-UI-Org/mcp-ui)
**Stars:** 5,073 | **Last updated:** 2026-07-08 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An SDK and convention for MCP servers to attach interactive UI resources that a host renders in a sandboxed iframe.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "**UI over MCP** — create next-gen UI experiences with the protocol and SDK". It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

This one earns a caveat the other six do not, because MCP is a protocol this catalog genuinely does track. The distinction that decides it: the **MCP Servers** category covers servers that give *your coding agent* new capabilities, whereas mcp-ui is about a server shipping *end-user interface* into a host application. Both involve MCP; only one is in the dev loop.

The closest in-scope neighbour is `MCP Apps (ext-apps)`, catalogued as a `reference` entry under Reference rather than as a framework to install — which is the right shape for a standard you should know exists. If mcp-ui is kept for the same reason, it belongs there too, as a reference row rather than an Implement-stage framework. That is a catalog edit, not a triage disposition, so it is recorded and not made.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-ui](https://github.com/MCP-UI-Org/mcp-ui) | framework | De-facto UI-over-MCP SDK — servers attach interactive UI resources rendered in a sandboxed iframe (Apache-2.0, ★5K) | Shipping interactive UI from an MCP server into a host needs a standard render/transport path | OpenGenerativeUI, CopilotKit, ag-ui, MCP Apps |
