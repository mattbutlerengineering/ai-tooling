# Evaluation: vercel/workflow

**Repo:** [vercel/workflow](https://github.com/vercel/workflow)
**Stars:** 2,283 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A TypeScript SDK for durable, reliable, observable workflows and AI agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "Workflow SDK: Build durable, reliable, and observable **apps and AI Agents in TypeScript**" — application infrastructure.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

Note it is a different artifact from its stablemate `vercel/ai`, which is the one framework left at `discovery-log` in this pass: that one ships a coding-agent skill and a harness-building primitive and so clears the bar. Same vendor, different disposition — which is the bar working as a test rather than as a blanket.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vercel/workflow](https://github.com/vercel/workflow) | framework | Durable workflow SDK for TypeScript (by Vercel) — write long-running, reliable, observable apps and AI agents as code that survives crashes/restarts via step-level durability and automatic retries; runs on Vercel or self-hosted | Agent/LLM pipelines that span minutes-to-days lose state on failure and are hard to observe; want durable execution without a separate orchestrator | trigger-dev, humanlayer, mastra, ag-ui |
