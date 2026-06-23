# Evaluation: AutoResearchClaw

**Repo:** [aiming-lab/AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw)
**Stars:** 13,490 | **Last updated:** 2026-06-03 (pushed; created 2026-03-15) | **License:** MIT | **CLI:** `researchclaw`
**Dev loop stage:** Research & Discovery (autonomous end-to-end research)
**Layer:** Harness (multi-stage research pipeline over any ACP-compatible agent backend)

---

## What it does

AutoResearchClaw is a **fully autonomous, self-evolving research pipeline — "chat an idea, get a paper"** — backed by an arXiv paper. It runs a ~23-stage pipeline from hypothesis to written paper, and has grown well past a toy:

- **Multi-domain experiment agents** — the experiment stages route beyond a default ML sandbox to specialist executors: high-energy physics (Lagrangian → FeynRules → MadGraph5 → Delphes), biology (COBRApy metabolic modelling), statistics (simulation studies), and a generic Docker executor for chemistry/materials, auto-selected by research domain.
- **ARC-Bench** — a 55-topic open-ended autonomous-research benchmark (ML/HEP/quantum/biology/stats) with manifests + rubrics, released on Hugging Face.
- **Human-in-the-loop co-pilot** — 6 intervention modes (full-auto → step-by-step), Idea Workshop, Baseline Navigator, Paper Co-Writer, SmartPause, cost-budget guardrails, anti-hallucination claim verification.
- **Backend-agnostic** — runs on any ACP-compatible agent (Claude Code, Codex, Copilot, Gemini, Kimi), with skill loading (`researchclaw skills install` / `.claude/skills/`) and MetaClaw cross-run learning (failures → reusable skills).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No pipeline run, no paper generated, no benchmark reproduced. Capabilities and metrics (e.g. "+18.3% robustness") come from the README, release notes, and paper, not observed runs.

```bash
gh api repos/aiming-lab/AutoResearchClaw --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 13.5K, MIT
gh api repos/aiming-lab/AutoResearchClaw/readme --jq '.content' | base64 -d | head -30   # 23-stage pipeline, multi-domain agents, ARC-Bench, HITL
```

## What worked

- **Serious scope and rigor.** A 23-stage pipeline with domain-specialist executors, a released benchmark (ARC-Bench), a paper, and explicit anti-hallucination/claim-verification is far beyond the typical "autonomous researcher" demo.
- **Human-in-the-loop is the right correction.** Adding 6 intervention modes + cost guardrails to a once "purely autonomous" system acknowledges that unsupervised research drifts/hallucinates — the catalog's lesson from ARIS-class tools.
- **Backend-agnostic + skill-loadable.** Running on any ACP agent and ingesting custom `SKILL.md` skills makes it composable rather than locked-in.
- **Self-evolving via MetaClaw.** Turning pipeline failures into reusable skills is a genuine compounding-quality mechanism. MIT, ~13.5K stars.

## What didn't work or surprised us

- **Autonomous science is high-risk for fabrication.** "Idea → paper" pipelines can produce confident, well-formatted, wrong results; the anti-hallucination/verification layers are necessary but their efficacy is unverified here. Generated papers need expert review before any external use.
- **Heavy + domain-infra-dependent.** Real experiments need the domain executors (MadGraph/Delphes, COBRApy, Docker sandboxes) and compute — a substantial operational footprint, not a quick skill.
- **Token/compute cost.** A 23-stage multi-agent pipeline with experiments is expensive; budget guardrails exist for a reason.
- **Overlaps the catalog's research cluster** (ARIS, autoresearch, deer-flow, PaperOrchestra) — differentiation is multi-domain experiment execution + benchmark + paper backing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / − | Anti-hallucination/claim verification + HITL gates aim at trustworthy output; autonomous research is inherently fabrication-prone — verify results. |
| Speed | + | Compresses idea→experiment→draft dramatically when it works. |
| Maintainability | neutral / − | Backend-agnostic and skill-loadable, but the domain executors + sandboxes are heavy infra to run. |
| Safety | neutral / − | Autonomous experimentation + paper generation is a correctness/integrity surface; HITL and budget guardrails mitigate. |
| Cost Efficiency | − | 23-stage multi-agent pipelines with experiments are token/compute-heavy (hence the budget guardrails). |

## Verdict

**CONDITIONAL** — AutoResearchClaw is an unusually serious, MIT, paper-backed **autonomous research harness** — a 23-stage idea→paper pipeline with domain-specialist experiment agents (physics/biology/stats/ML), a released benchmark (ARC-Bench), human-in-the-loop modes, and anti-hallucination verification, runnable on any ACP agent. Adopt it for genuine autonomous/assisted research exploration if you can supply the domain compute and **treat every output as a draft requiring expert verification** — the failure mode (plausible fabricated findings) is the dangerous one, which is exactly why its HITL and claim-verification layers exist. It's heavy and costly; not a casual add to a coding loop.

Compared to neighbors: **ARIS** is an overnight plan→review→persist research loop; **autoresearch** and **deer-flow** are research agents; **PaperOrchestra** orchestrates paper work. AutoResearchClaw's distinguishing pitch is **multi-domain autonomous experimentation + a research benchmark + paper backing**.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AutoResearchClaw](https://github.com/aiming-lab/AutoResearchClaw) | harness | Autonomous, self-evolving research pipeline (MIT, paper-backed) — ~23 stages idea→paper with domain-specialist experiment agents (physics/biology/stats/ML), ARC-Bench benchmark, 6 human-in-the-loop modes + anti-hallucination verification; runs on any ACP agent | Want end-to-end autonomous/assisted research with real experiments, not single-shot summaries — with guardrails against fabrication | ARIS, autoresearch, deer-flow, PaperOrchestra |
