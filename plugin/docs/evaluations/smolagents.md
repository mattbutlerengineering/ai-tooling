# Evaluation: smolagents

**Repo:** [huggingface/smolagents](https://github.com/huggingface/smolagents)
**Stars:** 28,676 | **Last updated:** 2026-07-21 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Hugging Face's minimal library for building agents that express actions as executable code rather than JSON tool calls.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "a barebones **library for agents** that think in code" — a library you build agents with, in the same class as `crewAI` and `langchain`, both already SKIPped. Its `Overlaps with` cell names `langchain`, `crewAI`, `pydantic-ai` and `autogen`; two of those four are already out of scope.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

The code-as-action design is genuinely interesting and is the reason to read the project. It is an argument about how agents should act at an application's runtime, not about the loop in which a human writes code.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [smolagents](https://github.com/huggingface/smolagents) | framework | Hugging Face's barebones agent library (Apache-2.0, ★28K) — agents that "think in code" (write Python actions instead of JSON), minimal abstractions, any model via the HF ecosystem | Want a minimal, hackable code-acting agent framework without a heavy stack (general agent framework, out of dev-loop scope) | langchain, crewAI, pydantic-ai, autogen |
