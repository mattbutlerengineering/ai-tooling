# Evaluation: harbor

**Repo:** [harbor-framework/harbor](https://github.com/harbor-framework/harbor)
**Stars:** ~2,600 | **Last updated:** 2026-06-20 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent evaluation / Outer Loop)
**Layer:** Infrastructure

---

## What it does

A framework for evaluating and optimizing **whole agents** (not just model outputs), from the creators of Terminal-Bench. Harbor lets you benchmark arbitrary coding agents, build/share environments, and generate training data for RL.

Per the README you can: evaluate arbitrary agents (Claude Code, OpenHands, Codex CLI, and more) against tasks; build and share your own benchmarks and environments; run experiments across **thousands of environments in parallel** via sandbox providers (Daytona, Modal, LangSmith, Blaxel, Novita); and generate **rollouts for RL optimization**. It's the agent-level analogue of an LLM eval harness — you score how a full agent performs in realistic, isolated environments, at scale.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the Harbor Cookbook reference. Confirmed the agent-level evaluation model (benchmark whole agents like Claude Code/OpenHands/Codex), the parallel-environment execution via sandbox providers, the build-your-own-benchmark capability, and the RL-rollout generation. The Terminal-Bench lineage lends credibility. Not run on a live eval, so condition-gated.

```bash
gh api repos/harbor-framework/harbor --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/harbor-framework/harbor/readme --jq '.content' | base64 -d
```

## What worked

- **Evaluates agents, not just models.** Scoring a full coding agent in realistic environments is the right granularity for comparing harnesses/configs — closer to what you actually ship than per-prompt evals.
- **Parallel scale via sandboxes.** Running thousands of environments through Daytona/Modal/etc. makes large, statistically-meaningful evals practical.
- **RL-ready + credible lineage.** Rollout generation for RL and the Terminal-Bench provenance make it a serious eval/optimization framework.

## What didn't work or surprised us

- **Heavyweight, infra-dependent.** Real value requires sandbox-provider setup and building environments — this is an eval platform, not a quick script.
- **For agent builders/researchers.** Most relevant if you build or tune agents (or compare harnesses); overkill for someone just using one agent.
- **Overlaps promptfoo/deepeval/phoenix.** Those eval model/app outputs; Harbor's niche is whole-agent, environment-based evaluation at scale.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Environment-based agent evals catch real task failures, not just output drift |
| Speed | + | Massively parallel environments speed large eval runs |
| Maintainability | + | Reusable, shareable benchmarks/environments |
| Safety | + | Sandboxed environments isolate agent execution during eval |
| Cost Efficiency | neutral | OSS; large parallel runs consume real sandbox/model compute |

## Verdict

**discovery-log — tentative read**

Adopt if you build, tune, or compare coding agents/harnesses and need rigorous, scaled, environment-based evaluation (and optionally RL rollouts) — the agent-level complement to promptfoo/deepeval's output evals. Requires sandbox-provider setup and environment authoring, so it's for agent builders/researchers, not casual users. Pairs naturally with daytona (one of its execution backends).

## Triage note

Left at `discovery-log`, and it is the row in this section most directly relevant to what this repo does.

Nearly everything else in the Outer Loop cluster evaluates *the AI product you build*. harbor evaluates
**coding agents and harnesses themselves** — rigorous, scaled, environment-based evaluation with optional
RL rollouts. That is the agent-level complement to `promptfoo` and `deepeval`'s output evals, and it is
the closest thing in the catalog to infrastructure for the measured comparisons `evaluations/measurement-protocols.md`
asks for.

Which makes it a genuinely interesting P0 candidate rather than a backlog row: a catalog whose weakest
point is the number of SOURCE-ONLY verdicts has an obvious use for a harness that runs agents against
environments and reports numbers.

The cost is real and the eval states it: sandbox-provider setup plus environment authoring, so this is for
agent builders and researchers, not casual use. `daytona` is one of its execution backends and pairs
naturally.

Apache-2.0, ★3.1K, pushed 2026-07-10.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [harbor](https://github.com/harbor-framework/harbor) | framework | Agent evaluation + RL-environment framework (Apache-2.0, by the Terminal-Bench creators) — evaluate arbitrary agents (Claude Code/OpenHands/Codex), build/share benchmarks, run thousands of environments in parallel via Daytona/Modal/etc., and generate RL rollouts | Want to benchmark whole coding agents (not just model outputs) at scale and produce RL training data | promptfoo, deepeval, phoenix, daytona |
