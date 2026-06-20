# Evaluation: evo

**Repo:** [evo-hq/evo](https://github.com/evo-hq/evo)
**Stars:** ~1,210 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Reflect (autoresearch / optimization)
**Layer:** Tooling

---

## What it does

A plugin for your agentic framework that turns a codebase into an **autoresearch loop**: it optimizes code through experiments. You give it a codebase; it discovers what metrics to optimize, instruments the benchmark, then runs experiments in a loop — trying things, keeping what improves the score, reverting what doesn't.

Per the README, it's inspired by Karpathy's autoresearch (an LLM autonomously running training experiments to beat its own best score). Plain autoresearch is a pure hill-climb on a single branch; **evo adds structure** on top — notably **tree search with parallel subagents** rather than a single linear branch, so it explores multiple optimization directions concurrently. Two commands get you started; there's also a hosted platform/dashboard for larger or custom deployments.

## How we tested it

Architecture review against the README and the described loop (discover metrics → instrument benchmark → tree-search experiments with parallel subagents → keep/revert by score). Confirmed the autoresearch lineage (Karpathy) and the structural additions (tree search, parallelism) over a pure hill-climb. Note an upgrade path toward a hosted "evo platform." Not run on a live codebase, so condition-gated.

```bash
gh api repos/evo-hq/evo --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/evo-hq/evo/readme --jq '.content' | base64 -d
```

## What worked

- **Closes the optimize loop autonomously.** Discovering metrics, instrumenting a benchmark, and hill-climbing them without hand-holding is a genuinely useful pattern for perf/quality optimization.
- **Tree search + parallel subagents.** Exploring multiple directions concurrently (vs. a single linear branch) is a real improvement over naive autoresearch — better coverage of the optimization space.
- **Low-friction start.** "Two commands" to begin lowers the barrier to trying it on a real repo.

## What didn't work or surprised us

- **Needs a measurable objective.** Like all autoresearch, it only works where you can define/auto-discover a numeric score; fuzzy "make it better" goals don't fit.
- **Token/compute heavy.** A loop of parallel experiment subagents spends real money; the hosted platform exists partly to manage that.
- **Overlaps evolver/ACE/textgrad.** Several tools do self-improvement/optimization; evo's edge is the autoresearch hill-climb over a codebase with tree search.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Keeps only changes that improve the measured score |
| Speed | + | Parallel subagent tree search explores faster than linear |
| Maintainability | neutral | Optimizes code; you still review what it keeps |
| Safety | neutral | Revert-on-no-improvement bounds risk; review merged changes |
| Cost Efficiency | - | Parallel experiment loops are token/compute heavy |

## Verdict

**CONDITIONAL**

Adopt when you have a codebase with a measurable optimization target (performance, a quality metric, a benchmark) and want an autonomous experiment loop that discovers and hill-climbs it with parallel tree search — a structured upgrade over manual tuning or naive autoresearch. Budget for the compute of parallel experiment subagents. For prompt/solution optimization specifically, textgrad/ACE are alternatives; evo's niche is codebase-level metric optimization.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [evo](https://github.com/evo-hq/evo) | tool | Autoresearch loop over your codebase (Apache-2.0) — discovers what metrics to optimize, instruments the benchmark, then runs tree search with parallel subagents (keep what improves, revert what doesn't); extends Karpathy's autoresearch hill-climb with structure | Optimizing code against perf/quality metrics by hand is slow and unsystematic; want an autonomous experiment loop | evolver, ACE, textgrad, AutoSci |
