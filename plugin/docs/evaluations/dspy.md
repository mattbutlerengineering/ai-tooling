# Evaluation: dspy

**Repo:** [stanfordnlp/dspy](https://github.com/stanfordnlp/dspy)
**Stars:** 36,626 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A framework for programming language models declaratively — composing and automatically optimizing LM programs instead of hand-writing prompts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "The framework for **programming—not prompting—language models**". What it programs is an LM pipeline inside an application; it does not intervene in the user's Plan/Implement/Verify/Review/Ship loop.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

Worth stating the strongest counter-argument, since DSPy is the least obviously out-of-scope row in this batch: its optimizers *measure* prompt programs against a metric, which is a genuinely evaluation-shaped activity, and this catalog cares about measurement. But the artifact under measurement is the product's LM pipeline, not the developer's workflow — the same reason `promptfoo` and `langfuse` sit under Outer Loop as *observability for AI products* rather than as dev-loop tools. If a future DSPy release optimizes a **coding agent's** prompts against a repo task set, that is the bridge, and this row should be re-opened on it.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dspy](https://github.com/stanfordnlp/dspy) | framework | Framework for programming—not prompting—LLMs (MIT, ★35K, Stanford) — declarative modules plus optimizers that compile your pipeline's prompts (and optionally weights) against a metric, so you tune programs instead of hand-editing prompt strings | Want to systematically optimize an LLM pipeline against a metric rather than manually tweaking brittle prompt strings (research/app framework, out of dev-loop scope) | langchain, llama_index, autogen, promptfoo |
