# Evaluation: agno

**Repo:** [agno-agi/agno](https://github.com/agno-agi/agno)
**Stars:** 41,571 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A framework and runtime for building, running and managing agent platforms.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "**Build, run, and manage agent platforms**" — the platform class this catalog excludes alongside `dify` and `Flowise`. Its `Overlaps with` cell names `crewAI`, `pydantic-ai`, `langchain` and `autogen`; two are already SKIPped.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agno](https://github.com/agno-agi/agno) | framework | Python framework for building, running, and managing full multi-agent platforms (Apache-2.0, ★41K) — agents, teams, and workflows with built-in memory and knowledge | Most frameworks handle single agents; Agno structures complete multi-agent platforms with teams and workflows (general agent framework, largely out of dev-loop scope) | crewAI, pydantic-ai, langchain, autogen |
