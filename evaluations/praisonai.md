# Evaluation: praisonai

**Repo:** [MervinPraison/PraisonAI](https://github.com/MervinPraison/PraisonAI)
**Stars:** 8,550 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A multi-agent framework for building autonomous, self-improving agent workforces that research, plan, code and execute.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description sells "a 24/7 AI Workforce … autonomous self-improving agents" — an agent-application platform. Its `Overlaps with` cell names `crewAI`, `autogen` and `fast-agent`; `crewAI` is already SKIPped on this exact ground.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

The description does say the agents "code", which is the only thing here resembling a bridge. It describes what the *built* agents do at the user's application runtime, not a tool that helps the reader write code — the distinction the `crewAI` eval drew as "orchestrates *product* agents at *your app's* runtime, outside [the loop]".

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [praisonai](https://github.com/MervinPraison/PraisonAI) | framework | Multi-agent framework — autonomous self-improving agents with built-in memory, RAG, and 100+ LLM support, deployable in ~5 lines (MIT) | Want to build autonomous multi-agent workflows (research/plan/code/execute) without boilerplate (largely out of dev-loop scope) | crewAI, autogen, fast-agent |
