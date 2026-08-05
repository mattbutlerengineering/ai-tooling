# Evaluation: open-multi-agent

**Repo:** [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent)
**Stars:** ~6,400 | **Last updated:** 2026-06-20 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A **goal-first** TypeScript multi-agent orchestration framework for Node.js backends. You give it a goal; a coordinator agent decomposes that goal into a task **DAG** at runtime, parallelizes independent tasks, and synthesizes the result.

The defining contrast (per the README): graph-first frameworks make you enumerate every node and edge up front; open-multi-agent is goal-first — "your engineers describe the goal, not the graph." The coordinator builds the task DAG dynamically, so the orchestration adapts to the goal instead of being hand-wired for one workflow. It drops into any Node.js backend.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the goal→DAG model (coordinator decomposes a goal into a task DAG at runtime, parallelizes independents, synthesizes). Confirmed the goal-first vs. graph-first distinction and the Node.js-backend integration. Not built a live orchestration, so condition-gated.

```bash
gh api repos/open-multi-agent/open-multi-agent --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/open-multi-agent/open-multi-agent/readme --jq '.content' | base64 -d
```

## What worked

- **Goal-first is a genuine ergonomic shift.** Describing an outcome and letting a coordinator build the DAG (vs. hand-enumerating nodes/edges) is less brittle and adapts to the goal — a real differentiator from graph-first frameworks.
- **Automatic parallelization.** Decomposing into a DAG and parallelizing independent tasks is exactly what you want from multi-agent orchestration, without manual wiring.
- **Drop-in for Node backends.** TS-native and embeddable in any Node.js backend lowers adoption friction for TS teams.

## What didn't work or surprised us

- **Dynamic DAG = less determinism.** Runtime decomposition trades the predictability of a hand-built graph for adaptability; for workflows needing strict reproducibility, a deterministic engine (agent-kit/Archon) may fit better.
- **Coordinator quality is the ceiling.** The whole approach hinges on the coordinator decomposing goals well; poor decomposition cascades.
- **Overlaps agent-kit/voltagent/mastra.** TS multi-agent is crowded; the edge here is goal-first dynamic DAGs.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Depends on coordinator decomposition + synthesis quality |
| Speed | + | Parallelizes independent tasks in the DAG automatically |
| Maintainability | + | Describe goals, not graphs — less orchestration to hand-maintain |
| Safety | neutral | Orchestration framework; safety depends on the tasks/tools |
| Cost Efficiency | neutral | OSS; multi-agent decomposition multiplies model calls |

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** A TypeScript framework for goal-first multi-agent orchestration — describe an outcome and let a coordinator build and parallelize the task DAG.

**Its own evaluation says so.** Its recommendation is "adopt for **TypeScript backends** where you want goal-first multi-agent orchestration", with `agent-kit`/`Archon` named as the deterministic alternatives.

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

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | framework | Goal-first TypeScript multi-agent orchestration (MIT, ★6.4K) — give it a goal and a coordinator decomposes it into a task DAG at runtime, parallelizes independents, and synthesizes; drops into any Node.js backend | Graph-first frameworks force you to enumerate every node/edge up front; want goal-first orchestration that builds the task DAG dynamically | agent-kit, voltagent, mastra, microsoft/agent-framework |
