# Evaluation: mastra

**Repo:** [mastra-ai/mastra](https://github.com/mastra-ai/mastra)
**Stars:** ~25,300 | **Last updated:** 2026-06-20 | **License:** source-available (repo SPDX returns NOASSERTION)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A TypeScript framework for building AI-powered applications and agents, from the team behind Gatsby. Mastra is designed to take you from early prototype to production with a modern TS stack, integrating with React/Next/Node or deploying as a standalone server.

Per the README, highlights include: **model routing** (40+ providers through one interface — OpenAI/Anthropic/Gemini/…); **agents** (autonomous, tool-using, iterate until a final answer/stop condition); **graph-based workflows** with an explicit control-flow syntax (`.then()`, `.branch()`, `.parallel()`); **human-in-the-loop** suspend/resume backed by storage (pause indefinitely, resume with state intact); plus RAG, memory, and evals. The pitch is a batteries-included, production-oriented TypeScript framework built around established AI patterns.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the feature highlights (model routing, agents, graph workflows with `.then()`/`.branch()`/`.parallel()`, HITL suspend/resume, RAG, memory, evals). Confirmed the TypeScript-first, production-oriented positioning and the framework integrations (React/Next/Node/standalone). License resolves to NOASSERTION via the API — confirm exact terms before commercial reliance. Not built a live app, so condition-gated.

```bash
gh api repos/mastra-ai/mastra --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/mastra-ai/mastra/readme --jq '.content' | base64 -d
```

## What worked

- **Production TS stack, batteries included.** Agents + graph workflows + model routing + RAG + memory + evals in one framework that deploys to React/Next/Node — less glue than assembling pieces.
- **HITL suspend/resume is first-class.** Storage-backed pause-and-resume of agents/workflows (pause indefinitely, resume with state) is a genuinely useful production capability many frameworks lack.
- **Explicit workflow control flow.** `.then()`/`.branch()`/`.parallel()` graph workflows give deterministic orchestration alongside autonomous agents — a good control/autonomy split, from a credible (Gatsby) team.

## What didn't work or surprised us

- **License unresolved.** NOASSERTION via the API — pin the exact terms before commercial use.
- **Crowded TS-agent space.** Overlaps voltagent, agent-kit, and (Python) pydantic-ai/haystack; Mastra's edge is the batteries-included, frontend-integrated, production-with-HITL framing.
- **Framework commitment.** Adopting Mastra means building around its abstractions; heavier than a thin agent library for simple needs.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Graph workflows + evals + HITL approval reduce uncontrolled behavior |
| Speed | + | Batteries-included stack accelerates prototype→production |
| Maintainability | + | One framework with explicit workflows is testable and inspectable |
| Safety | + | Human-in-the-loop suspend/resume gates risky actions |
| Cost Efficiency | neutral | OSS; model routing helps, but framework adds its own overhead |

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** A batteries-included TypeScript framework for production AI apps — graph workflows, model routing, RAG, memory, evals, human-in-the-loop.

**Its own evaluation says so.** Its recommendation is "adopt for TypeScript teams **building production AI apps/agents**", and it routes readers to `voltagent` and `agent-kit` as the alternatives inside that same category.

The bar is not new and is not this lane's invention. `WORKFLOW.md`'s **Tools Deliberately
Excluded** table states it — "Flowise, LangGraph — visual/programmatic agent builders: for building AI
products, not for your own dev workflow" — and the catalog has already applied it nine times, to
`langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`, `aisuite`, `dify`, `Flowise` and
`RAGFlow`. The `langchain` eval spells out both the test and the exceptions: a framework earns a slot
only if it has a **dev-loop bridge**, as `fast-agent` does by doubling as a runnable MCP-native coding
agent and `vercel/ai` does by shipping a coding-agent skill plus a harness-building primitive.

A SKIP here removes nothing. Per the `Flowise` precedent — "SKIP for this catalog's purpose (keep as
a reference entry)" — the row stays in `CATALOG.md`; what changes is that it stops reading as
something to install into a dev loop.

The eval also carries an unresolved item worth preserving through the SKIP: "**pin the license terms**". Recorded rather than chased, since the scope call decides the row regardless.

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mastra](https://github.com/mastra-ai/mastra) | framework | TypeScript AI framework (★25K, by the Gatsby team; SPDX unverified) — agents, graph-based workflows (`.then()`/`.branch()`/`.parallel()`), model routing across 40+ providers, RAG, memory, evals, and human-in-the-loop suspend/resume; React/Next/Node or standalone | Want a batteries-included, production-oriented TypeScript stack for agents + workflows with HITL and evals, not hand-rolled glue | voltagent, agent-kit, pydantic-ai, haystack |
