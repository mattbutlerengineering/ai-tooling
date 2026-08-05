# Evaluation: agent-native

**Repo:** [BuilderIO/agent-native](https://github.com/BuilderIO/agent-native)
**Stars:** 4,408 | **Last updated:** 2026-08-05 (pushed) | **License:** **none declared**
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A framework for structuring applications so that AI agents can operate them by design.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "a framework for building **agent-native applications**". It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

**A second, independent ground: no license.** The `CATALOG.md` row already carries "⚠️ no license = not adoptable", and that was re-verified rather than trusted — a live fetch on 2026-08-04 returns `license: null`. The re-check was not ceremony: earlier in this same triage lane `vercel-labs/skills` was queued for elimination on a cached `NONE` and survived, because upstream had added an MIT LICENSE since the record was written. A cached `NONE` is not evidence; a same-day confirmed absence is.

Either ground alone would decide this row. Both are recorded so that a future LICENSE file re-opens only the licensing question, not the scope one.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-native](https://github.com/BuilderIO/agent-native) | framework | Framework for building agent-native applications (⚠️ no license = not adoptable, ★3.2K) — structure apps so AI agents can operate them by design | Apps aren't built for agents to drive; want a framework that makes an app agent-operable by design | CopilotKit, tambo, CLI-Anything |
