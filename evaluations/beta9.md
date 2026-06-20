# Evaluation: beta9

**Repo:** [beam-cloud/beta9](https://github.com/beam-cloud/beta9)
**Stars:** ~1,670 | **Last updated:** 2026-06-20 | **License:** AGPL-3.0
**Dev loop stage:** Implement (serverless execution / sandboxes)
**Layer:** Infrastructure

---

## What it does

Beta9 (Beam) is a fast, open-source serverless runtime for AI workloads — a Pythonic interface to deploy and scale AI applications with zero infrastructure overhead. Relevant to this catalog, it includes **sandboxes** for running AI-generated code alongside its serving/jobs features.

Per the README: sub-second container builds (custom container runtime), parallelization/concurrency (fan out to hundreds of containers), scale-to-zero, hot-reloading, webhooks, and scheduled jobs — plus sandboxes for isolated code execution. The primary identity is serverless AI serving/inference, but the sandbox + fast-container capabilities make it usable as execution infrastructure for agent workloads (e.g. running untrusted generated code at scale).

## How we tested it

Architecture review against the README and feature list (fast image builds, fan-out concurrency, scale-to-zero, webhooks/jobs, sandboxes). Confirmed the serverless-AI-runtime identity and the sandbox capability relevant to agent code execution. Note: this is primarily AI-app serving infrastructure; it's catalogued for the sandbox/agent-execution angle. Not deployed live, so condition-gated.

```bash
gh api repos/beam-cloud/beta9 --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/beam-cloud/beta9/readme --jq '.content' | base64 -d
```

## What worked

- **Fast, scalable execution.** Sub-second container builds + fan-out to hundreds of containers + scale-to-zero is a strong base for running agent/AI workloads economically.
- **Sandboxes for generated code.** The sandbox capability makes it relevant to safely executing untrusted LLM-generated code at scale, not just serving models.
- **Pythonic DX.** Hot-reloading, webhooks, and scheduled jobs give a first-class developer experience for AI app deployment.

## What didn't work or surprised us

- **Primarily a serving runtime.** Its core identity is serverless AI inference/apps (MLOps-adjacent), not AI-assisted development — relevance here is the sandbox/execution angle, narrower than dedicated agent sandboxes.
- **AGPL-3.0.** Strong copyleft matters if you offer it as a networked service — review obligations (or use Beam's cloud).
- **Overlaps daytona/agent-sandbox/cua.** Those are purpose-built agent/code sandboxes; beta9 is a broader AI runtime that happens to include sandboxes.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Execution infra; correctness depends on the workload |
| Speed | + | Sub-second container builds and massive fan-out |
| Maintainability | + | Pythonic deploy with hot-reload/webhooks/jobs; zero infra mgmt |
| Safety | + | Sandboxes isolate execution of AI-generated code |
| Cost Efficiency | + | Scale-to-zero serverless; pay only for what runs |

## Verdict

**CONDITIONAL**

Adopt when you need fast, scalable, scale-to-zero serverless execution for AI workloads — and, relevant here, sandboxes for running agent/AI-generated code at scale with a Pythonic DX. Weigh AGPL-3.0 for productized/networked use. For purpose-built agent code-execution sandboxes specifically, daytona/agent-sandbox/cua are more focused; beta9 fits when you also want a general serverless AI runtime.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [beta9](https://github.com/beam-cloud/beta9) | platform | Open-source serverless runtime for AI workloads (AGPL-3.0, by Beam) — Pythonic deploy/scale with sub-second container builds, fan-out to 100s of containers, scale-to-zero, webhooks, scheduled jobs, and sandboxes for running AI-generated code | Need fast, isolated, scalable execution for agent/AI workloads (incl. running untrusted generated code) without managing infra | daytona, agent-sandbox, cua, modal (ext.) |
