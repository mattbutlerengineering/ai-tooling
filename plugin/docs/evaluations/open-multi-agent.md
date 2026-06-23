# Evaluation: open-multi-agent

**Repo:** [open-multi-agent/open-multi-agent](https://github.com/open-multi-agent/open-multi-agent)
**Stars:** ~6,400 | **Last updated:** 2026-06-20 | **License:** MIT
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

**CONDITIONAL**

Adopt for TypeScript backends where you want goal-first multi-agent orchestration — describe the outcome and let a coordinator build and parallelize the task DAG — rather than hand-wiring a graph. Best when adaptability matters more than strict reproducibility; for deterministic, code-controlled routing, agent-kit/Archon fit better. Coordinator decomposition quality is the key variable to validate.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [open-multi-agent](https://github.com/open-multi-agent/open-multi-agent) | framework | Goal-first TypeScript multi-agent orchestration (MIT, ★6.4K) — give it a goal and a coordinator decomposes it into a task DAG at runtime, parallelizes independents, and synthesizes; drops into any Node.js backend | Graph-first frameworks force you to enumerate every node/edge up front; want goal-first orchestration that builds the task DAG dynamically | agent-kit, voltagent, mastra, microsoft/agent-framework |
