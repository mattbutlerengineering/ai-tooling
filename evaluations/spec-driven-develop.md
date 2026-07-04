# Evaluation: Spec-Driven Develop

**Repo:** [zhu1090093659/spec_driven_develop](https://github.com/zhu1090093659/spec_driven_develop)
**Stars:** 905 | **Last updated:** 2026-06-09 (pushed; created 2026-03-21) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (architecture-first spec workflow feeding Implement; tracks via GitHub Issues/PRs into Ship)
**Layer:** Process (pure-Markdown skills — no SDK, no runtime)

---

## What it does

Spec-Driven Develop is a **platform-agnostic, architecture-first workflow** for AI coding agents, shipped as **pure Markdown skills** (no SDK, no runtime, no dependencies) that any agent reading custom skills can execute — Claude Code, Codex, Cursor, and others. It turns large software changes into a spec-driven loop: deep project analysis, **phased task decomposition**, document-driven progress tracking, **GitHub Issue/PR tracking**, progress continuity across sessions, and "adaptive control" the README explicitly frames as inspired by **Qian Xuesen's engineering cybernetics**.

It ships **two complementary skills**:
- **Spec-Driven Develop** — automates the full pipeline for large/complex tasks (analysis → phased decomposition → document-driven tracking → execution within a single session), organized around an **S.U.P.E.R** architectural backbone.
- **Deep Discuss** — a structured deep-discussion workflow for problem analysis, brainstorming, and solution design through disciplined multi-phase thinking.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No skills installed, no workflow executed. Claims come from the repository (GitHub metadata, README "What It Does" / S.U.P.E.R / platform sections) — the project's own documentation, not observed behavior.

```bash
gh api repos/zhu1090093659/spec_driven_develop --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/zhu1090093659/spec_driven_develop/readme --jq '.content' | base64 -d   # two skills, S.U.P.E.R, GitHub tracking
```

## What worked

- **Markdown-only, zero-dependency, platform-agnostic.** Like the best SDD frameworks (OpenSpec, ccpm), it's just files any agent can read — trivial to install, audit, fork, and run anywhere, with no lock-in or runtime.
- **GitHub Issue/PR tracking + cross-session continuity** is a practical answer to the real failure mode of long, complex tasks: the agent losing the thread between sessions. Document-driven progress is the right durable substrate.
- **The Deep Discuss skill is a genuine add.** A disciplined multi-phase *thinking/brainstorming* workflow paired with the execution pipeline covers the "design before build" half that pure task-runners skip.
- **Coherent design philosophy.** The cybernetics-inspired "adaptive control" framing and S.U.P.E.R backbone give it an opinionated, traceable structure rather than ad-hoc prompts.
- **Active, MIT, bilingual.**

## What didn't work or surprised us

- **Crowded SDD niche.** It competes directly with spec-kit, OpenSpec, BMAD-METHOD, ccpm, and aidlc-workflows — all Markdown spec-driven workflows. Differentiation is the Deep Discuss skill + cybernetics framing, not a new category.
- **Quality is unverified and model-dependent.** "Automates the full pipeline" is the claim; actual decomposition/tracking quality depends on the driving agent and isn't measured here.
- **Opinionated backbone (S.U.P.E.R).** Like any methodology, teams with their own spec process may find it redundant or conflicting; the cybernetics framing is novel but unproven as a practical advantage.
- **Single-maintainer, mid-size.** 905★, one author — less social proof and ecosystem than spec-kit/BMAD; longevity less certain.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Architecture-first decomposition + Deep Discuss design phase + Issue/PR tracking reduce "agent wandered off-spec" errors on large tasks. |
| Speed | + / neutral | Structure speeds large multi-session work; adds planning overhead on small tasks. |
| Maintainability | + | Spec/document-driven, GitHub-tracked work leaves a durable trail; encourages decomposition over monolithic changes. |
| Safety | neutral | Not a security tool; standard agent trust model. |
| Cost Efficiency | neutral | Free/MIT; spends planning/execution tokens. |

## Verdict

**CONDITIONAL** — a solid, dependency-free spec-driven workflow whose distinguishing features are the paired **Deep Discuss** thinking skill and cybernetics-inspired adaptive control, plus first-class GitHub Issue/PR tracking and cross-session continuity. Adopt if you want a Markdown SDD framework for large, multi-session changes and value the explicit design-discussion phase. But it's one of several strong SDD options — if you're not already invested, compare against spec-kit (largest ecosystem), OpenSpec, and BMAD-METHOD first; pick this one specifically for the Deep Discuss workflow or if its S.U.P.E.R structure resonates. Quality is model-dependent and unverified.

Compared to neighbors: same family as **spec-kit** / **OpenSpec** / **BMAD-METHOD** / **ccpm** / **aidlc-workflows**. Its edge is the **Deep Discuss design-phase skill** and cybernetics-framed adaptive control bundled with the execution pipeline — a "discuss then decompose then track" loop rather than decomposition alone.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [spec_driven_develop](https://github.com/zhu1090093659/spec_driven_develop) | skill | Architecture-first, Markdown-only SDD workflow for any agent — phased task decomposition, GitHub Issue/PR tracking, cross-session continuity, plus a "Deep Discuss" structured design-thinking skill | Large multi-session changes drift off-spec and lose continuity; want dependency-free spec-driven decomposition with a design-discussion phase | spec-kit, OpenSpec, BMAD-METHOD, ccpm |
