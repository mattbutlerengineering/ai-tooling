# Evaluation: phoenix

**Repo:** [Arize-ai/phoenix](https://github.com/Arize-ai/phoenix)
**Stars:** ~10,200 | **Last updated:** 2026-06-20 | **License:** Elastic License 2.0 (source-available)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
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

**SKIP** — permissively-licensed equivalents cover the same job. The tentative read above puts the
question precisely: *"Weigh the Elastic License 2.0 terms versus the Apache/MIT alternatives (langfuse,
opik) if license purity or offering-as-a-service matters."* Weighed, the alternatives win.

ELv2 is source-available, not open source: it forbids offering the software as a managed service and
permits the licensor to change terms. That is a live constraint rather than a theoretical one for
anything self-hosted, and this catalog's adoption bar is permissive OSS. GitHub's `NOASSERTION` on the
record is consistent with a licence its parser does not recognise, and — per CLAUDE.md — is *not*
itself the ground here; the eval's own reading of the terms is.

What makes it a disposition instead of a caveat is that the substitutes are not hypothetical.
`langfuse` and `opik` are both **P0 leads**, both permissively licensed, and both cover
tracing, evals, datasets and prompt experimentation. `logfire` (MIT) is the OTel-native option for
Python stacks and stays. There is no capability here that requires accepting the licence.

Nothing against the software: OTel-native, self-hostable, broad framework coverage, ★10.5K behind it,
and Arize is a serious shop. The row stays catalogued so anyone who does not share the licence
constraint finds it.

Re-open if it relicenses permissively, or if a measured comparison shows it doing something langfuse
and opik cannot.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [phoenix](https://github.com/Arize-ai/phoenix) | platform | Open-source AI observability + evaluation (ELv2, by Arize) — OTel tracing, LLM-as-judge response/retrieval evals, versioned datasets + experiments, prompt playground/management, and a built-in debugging agent (PXI); framework-agnostic, self-host or cloud | Want tracing, evals, datasets, and prompt experimentation in one self-hostable, OTel-native tool | langfuse, opik, logfire, deepeval |
