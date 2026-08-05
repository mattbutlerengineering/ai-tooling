# Evaluation: hashbrown

**Repo:** [liveloveapp/hashbrown](https://github.com/liveloveapp/hashbrown)
**Stars:** 716 | **Last updated:** 2026-07-21 (pushed) | **License:** NOASSERTION (GitHub could not parse the LICENSE file)
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A generative-UI framework for Angular and React in which the model selects and streams the application's exposed components.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "a framework for building **agents that run [in] the browser**, built for Angular and React". It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

**The `NOASSERTION` is not part of this disposal and must not be read as one.** GitHub records `NOASSERTION` here, which means its parser could not read the LICENSE file — nothing about whether a grant exists. This lane has now watched that same value conceal a permissive Apache-2.0 (`terraform-skill`) and a blocking CC BY-NC 4.0 (`academic-research-skills`). The ground here is scope alone, and it would be identical under any license.

At ★716 this is also the smallest row in the cluster, and its stated niche — generative UI for **Angular** shops, where the rest of the family is React-only — is a real gap it fills. That is an argument for its existence, not for this catalog carrying it.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hashbrown](https://github.com/liveloveapp/hashbrown) | framework | Generative-UI framework for Angular and React — the LLM picks and streams your exposed components (MIT) | Generative UI for Angular shops; most gen-UI frameworks are React-only | CopilotKit, tambo, assistant-ui |
