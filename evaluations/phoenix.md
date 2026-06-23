# Evaluation: phoenix

**Repo:** [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)
**Stars:** ~10,200 | **Last updated:** 2026-06-20 | **License:** Elastic License 2.0 (source-available)
**Dev loop stage:** Reflect (Outer Loop / observability + evaluation)
**Layer:** Infrastructure

---

## What it does

An open-source AI observability and evaluation platform from Arize, built for experimentation, evaluation, and troubleshooting. The `arize-phoenix` pip package is the whole platform and runs locally, in a notebook, in Docker/Kubernetes, or via Arize's cloud.

Core capabilities per the README: **Tracing** (OpenTelemetry-based instrumentation of your LLM app's runtime), **Evaluation** (LLM-as-judge response and retrieval evals), **Datasets** (versioned example sets for eval/experimentation/fine-tuning), **Experiments** (track and evaluate changes to prompts/LLMs/retrieval), a **Playground** (compare models, tune params, replay traced LLM calls), **Prompt Management** (version/tag/experiment on prompts), and **PXI** (an AI engineering agent built into Phoenix for debugging traces and iterating on prompts). It's vendor/language/framework-agnostic with out-of-the-box instrumentation for OpenAI Agents SDK, Claude Agent SDK, LangGraph, Vercel AI SDK, Mastra, CrewAI, LlamaIndex, and DSPy, via the OpenInference project.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README, the capability list, and the integration matrix. Confirmed the OTel/OpenInference tracing foundation, the eval + datasets + experiments loop, the playground/prompt-management features, the built-in PXI debugging agent, and the local/notebook/Docker/cloud deployment story. Verified the license is Elastic License 2.0 (source-available, not OSI-open). Not run on a live app, so condition-gated.

```bash
gh api repos/Arize-ai/phoenix --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/Arize-ai/phoenix/readme --jq '.content' | base64 -d
gh api repos/Arize-ai/phoenix/contents/LICENSE --jq '.content' | base64 -d | head -2
```

## What worked

- **Tracing + evals + datasets + experiments in one tool.** Most competitors do a subset; Phoenix spans the whole experiment→eval→troubleshoot loop, self-hostable from a notebook.
- **OTel/OpenInference-native and framework-agnostic.** First-class instrumentation for Claude Agent SDK, LangGraph, CrewAI, LlamaIndex, DSPy, etc. — low lock-in, broad coverage.
- **PXI debugging agent + playground.** A built-in agent for trace debugging and a replay/compare playground are genuinely useful beyond passive dashboards.

## What didn't work or surprised us

- **Elastic License 2.0, not OSI-open.** Source-available with ELv2 restrictions (notably no offering it as a managed service) — fine for internal use, but not "truly open" like langfuse/opik (Apache/MIT).
- **Heavyweight for small jobs.** Full platform install; for a quick one-file trace you may want a lighter SDK.
- **Crowded category.** Overlaps langfuse, opik, logfire; the differentiators are the experiments/datasets workflow and Arize's prod-ML lineage.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | LLM-as-judge response/retrieval evals + experiments catch regressions |
| Speed | + | Playground replay and PXI debugging shorten the troubleshoot loop |
| Maintainability | + | OTel/OpenInference-standard tracing; versioned datasets/prompts |
| Safety | neutral | Observability/eval aids review; not a guardrail |
| Cost Efficiency | ✓/$ | Self-host free; Arize cloud and judge-eval token use cost |

## Verdict

**CONDITIONAL**

Strong pick when you want one self-hostable, OTel-native tool covering tracing, evals, datasets, and prompt experimentation — especially across multiple agent frameworks. Weigh the Elastic License 2.0 terms versus the Apache/MIT alternatives (langfuse, opik) if license purity or offering-as-a-service matters. Re-evaluate hands-on against logfire and langfuse for an observability-stack decision.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [phoenix](https://github.com/Arize-ai/phoenix) | platform | Open-source AI observability + evaluation (ELv2, by Arize) — OTel tracing, LLM-as-judge response/retrieval evals, versioned datasets + experiments, prompt playground/management, and a built-in debugging agent (PXI); framework-agnostic, self-host or cloud | Want tracing, evals, datasets, and prompt experimentation in one self-hostable, OTel-native tool | langfuse, opik, logfire, deepeval |
