# Evaluation: semantic-kernel

**Repo:** [microsoft/semantic-kernel](https://github.com/microsoft/semantic-kernel)
**Stars:** 28,417 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Microsoft's SDK for integrating LLMs into applications across .NET, Python and Java — the predecessor and sibling of Microsoft Agent Framework.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "Integrate cutting-edge LLM technology quickly and easily into **your apps**" — the scope mismatch is in the sentence.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

Disposed alongside `microsoft/agent-framework` in this same pass, which is its successor and whose eval conceded the same point ("it builds agentic systems rather than serving the coding dev loop directly"). Keeping the predecessor after disposing the successor would leave the catalog recommending the older of two out-of-scope tools.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [semantic-kernel](https://github.com/microsoft/semantic-kernel) | framework | Microsoft's model-agnostic LLM orchestration SDK (MIT, ★28K) for .NET/Python/Java — plugins, planners, memory, and agent framework to embed AI into enterprise apps | Adding LLM orchestration (tools/planners/memory) to production .NET/Java/Python apps (general framework, out of dev-loop scope) | langchain, microsoft/agent-framework, autogen, pydantic-ai |
