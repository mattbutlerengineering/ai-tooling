# Evaluation: Flow-Next

**Repo:** [gmickel/flow-next](https://github.com/gmickel/flow-next)
**Stars:** 635 | **Last updated:** 2026-06-18 (pushed) | **License:** MIT | **Language:** Python (pure-stdlib `flowctl` CLI) + agent skills
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Dev Workflow (spec-driven engineering) — Plan → Implement → Review → Ship
**Layer:** Process + Tooling (plugin: 28 skills layered on a deterministic CLI)

---

## What it does

Flow-Next is a **spec-driven AI workflow plugin** for Claude Code, OpenAI Codex, and Factory Droid (also runs on Grok Build and Cursor; community OpenCode port). It is "the workflow layer for AI coding agents: durable specs, re-anchored workers, adversarial reviews, receipts," with **28 agent-native skills** covering idea → spec → tasks → review → ship → maintain, layered on a bundled **pure-stdlib Python CLI (`flowctl`)**. Its premise: agentic engineering removed Agile's safety valves (standups, mid-flight correction), so "the spec has to carry the weight." Between idea and merge it defines **six named handover objects**, each reviewable, **verified by a *different* model**, and frozen at handover. Tenets: spec-driven (`.flow/specs/<id>.md`), context-fit planning (tasks sized to one ~100k-token window), re-anchored work (every worker re-reads spec/task/git state), adversarial gates (a different model — RepoPrompt/Codex/Copilot — reviews every plan and implementation), receipts (commits/tests/verdicts recorded), and self-improving memory/glossary/decisions. Everything lives in-repo under `.flow/`; uninstall is `rm -rf .flow/`. Includes a "Ralph" autonomous mode.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No plugin installed, no spec authored, no worker/review cycle executed.

```bash
gh api repos/gmickel/flow-next --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 635, MIT, pushed 2026-06-18
gh api repos/gmickel/flow-next/readme --jq '.content' | base64 -d | sed -n '369,460p'        # six handover objects, tenets, multi-harness install
```

## What worked

- **Diagnosis is sharp.** "The bottleneck moved upstream to requirements, review, and verification" is the right read on agentic engineering, and the design follows from it rather than being feature soup.
- **Re-anchored workers + context-fit tasks.** Sizing tasks to one fresh ~100k window and re-reading spec/task/git before each run directly targets context rot and mid-task drift.
- **Adversarial cross-model gates.** Reviewing every plan and implementation with a *different* model ("different models make different mistakes") is a strong, concrete quality mechanism — close to the catalog's architect-loop idea, generalized.
- **Receipts, not narration.** Recording commits/tests/review verdicts per task makes "done" falsifiable.
- **Zero-dep, in-repo, reversible.** Pure-stdlib CLI, all state under `.flow/`, `rm -rf` uninstall — no SaaS, code-reviewable artifacts.
- **Genuinely multi-harness.** First-class on Claude Code, Codex, and Factory Droid.

## What didn't work or surprised us

- **Ceremony cost.** Six handover objects + adversarial gates is heavier than lightweight SDD (OpenSpec); the payoff is on large, multi-session work, not quick fixes.
- **Cross-model reviews need other models wired up.** The adversarial gate's value depends on having RepoPrompt/Codex/Copilot available — more setup and possibly more cost.
- **Crowded SDD field.** Competes with spec-kit, OpenSpec, BMAD-METHOD, ccpm, reversa; the differentiators are re-anchoring, different-model gates, and receipts, not spec-driven dev per se.
- **Solo-maintainer, 635 stars.** Younger/smaller than the incumbent SDD frameworks; the design is opinionated and tied to one author's methodology.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Durable specs + re-anchored workers + different-model adversarial review on every plan/implementation catch drift and gaps. |
| Speed | neutral | Faster on large work via context-fit slices; the spec/review ceremony slows trivial tasks. |
| Maintainability | + | In-repo, git-reviewable specs/receipts/decisions + self-improving glossary leave durable, inspectable artifacts. |
| Safety | + | Adversarial gates + receipts ("proof, not narration") guard against over-claimed completion. |
| Cost Efficiency | neutral | Zero external deps; cross-model reviews and multi-pass gates add inference cost on big tasks. |

## Verdict

**CONDITIONAL** — Flow-Next is one of the more thoughtfully designed **spec-driven workflow plugins**: it diagnoses agentic engineering's real failure (drift, forgotten requirements, unreviewable mega-diffs) and answers with durable specs, context-fit task slices, re-anchored workers, and — its strongest feature — **different-model adversarial review of every plan and implementation**, all as in-repo, reversible `.flow/` artifacts with receipts. Adopt it for **large, multi-session work** on Claude Code/Codex/Factory Droid when you want enforced specs and cross-model verification and will wire up a second model for the gates. For quick fixes or minimal SDD, OpenSpec is lighter; Flow-Next earns its ceremony when the spec genuinely has to carry the weight. Smaller/younger than spec-kit/BMAD — pilot before standardizing a team on it.

Compared to neighbors: **spec-kit** is GitHub's Specify→Plan→Tasks→Implement with human checkpoints; **OpenSpec** is lightweight agent-agnostic SDD; **BMAD-METHOD** is role-based agile; **ccpm** uses GitHub Issues as the spec DB; **reversa** generates specs backward from legacy code. Flow-Next's distinguishing pitch is **six frozen handover objects, each verified by a different model, with receipts — zero-dep and in-repo.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [flow-next](https://github.com/gmickel/flow-next) | plugin | Spec-driven workflow plugin (MIT) for Claude Code / Codex / Factory Droid — 28 skills + pure-stdlib `flowctl` CLI turning intent into durable specs → context-sized task graphs → re-anchored worker runs → adversarial cross-model reviews → receipts; everything in-repo under `.flow/` | Agents drift, forget requirements, and hand reviewers huge diffs; want durable specs and verified, different-model handoffs with zero external deps | spec-kit, OpenSpec, BMAD-METHOD, reversa, ccpm |
