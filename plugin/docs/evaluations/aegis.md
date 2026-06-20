# Evaluation: Aegis

**Repo:** [GanyuanRan/Aegis](https://github.com/GanyuanRan/Aegis)
**Stars:** 542 | **Last updated:** 2026-06-17 (pushed; created 2026-04-30) | **License:** MIT | **Install:** natural-language, host-detected method-pack
**Dev loop stage:** Implement / Dev Workflow (workflow-discipline guardrails)
**Layer:** Skill pack (portable "method-pack" skills across multiple agent hosts)

---

## What it does

Aegis is a **baseline-first, evidence-driven workflow-discipline pack for AI coding agents** — explicitly positioned as a **"Superpowers upgrade"** for real software work. It keeps composable skills but adds engineering guardrails:

- **Baseline first** — read current project facts before high-risk changes.
- **Evidence before completion** — no "done" claim without fresh verification evidence.
- **Repair track + retirement track** — when fixing, explicitly state whether the old path is kept or retired.
- **Workflow-quality guardrails** — stay lightweight on simple tasks, expand only as risk rises.
- **Portable method-pack skills** across multiple agent hosts.

The pitch is that agents tend to start coding before goal/owner/architecture boundaries or verification paths are clear; Aegis pulls work back to a steadier engineering rhythm. Install is itself agent-driven: you hand the agent a paragraph that detects your host, installs globally, and runs `aegis-doctor.py` until it reports `"ok": true`.

## How we tested it

**Source-grounded inspection — not installed, not run.** No method-pack installed, no workflow exercised. Behavior comes from the README (largely Chinese) and metadata, not observed runs.

```bash
gh api repos/GanyuanRan/Aegis --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 542, MIT
gh api repos/GanyuanRan/Aegis/readme --jq '.content' | base64 -d | head -40   # baseline-first, evidence-before-completion, repair/retirement tracks
```

## What worked

- **The two core guardrails are exactly right.** "Read the baseline before high-risk changes" and "no completion claim without fresh verification evidence" are the disciplines that most reduce confident-but-wrong agent output — the same principles behind verification-before-completion and implementation-discipline.
- **Risk-scaled workflow.** Staying lightweight on trivial tasks and expanding only as risk rises avoids the ceremony tax that kills heavier process packs.
- **Repair vs. retirement tracking** is a thoughtful touch — it forces agents to be explicit about legacy-path disposition instead of silently orphaning code.
- **Portable across hosts, MIT.** Method-pack skills aim to work across multiple agent hosts rather than locking to one.

## What didn't work or surprised us

- **Directly overlaps superpowers** (and the principles in GSD/compound-engineering). It's framed as an *upgrade* to that family, so the question is incremental value over Superpowers + a verification skill, not a new category.
- **Install ergonomics are unusual.** Handing the agent a paragraph to self-install and gating on `aegis-doctor.py` JSON is clever but opaque; verify what it installs globally before running it.
- **Docs are mostly Chinese.** Fine if you read it; a friction point otherwise, and harder to audit the guardrails' exact behavior.
- **Young, single-author, discipline-by-convention.** Like all skill-based guardrails, it nudges the agent rather than hard-enforcing — effectiveness depends on adherence.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Baseline-first + evidence-before-completion directly reduce unverified/confidently-wrong changes. |
| Speed | neutral / − | Adds discipline steps on risky work (intended); risk-scaling keeps trivial tasks light. |
| Maintainability | + | Repair/retirement tracking and reading project facts first reduce silent drift and orphaned paths. |
| Safety | + | "Don't claim done without evidence" and baseline reads shrink blast radius on high-risk changes. |
| Cost Efficiency | neutral | Verification/baseline reads cost some tokens; offset by fewer bad-change redo loops. |

## Verdict

**CONDITIONAL** — Aegis packages the highest-leverage agent disciplines — **baseline-first** and **evidence-before-completion**, plus repair/retirement tracking and risk-scaled workflow — as portable method-pack skills, MIT-licensed. The principles are exactly the ones that curb confident-but-wrong agent work, so it's worth a look for teams wanting that discipline as installable guardrails. The catch is heavy overlap with **superpowers** (it bills itself as a Superpowers upgrade): evaluate whether it beats Superpowers + a verification-before-completion skill for your hosts. The self-installing paragraph and Chinese-first docs warrant a careful read before global install.

Compared to neighbors: **superpowers** is the composable-skills harness it builds on; **GSD** and **compound-engineering** impose phased/structured discipline; **sentrux** gives architectural feedback. Aegis's distinguishing pitch is **baseline-first + evidence-before-completion guardrails** layered onto the Superpowers skill model.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Aegis](https://github.com/GanyuanRan/Aegis) | skill | Baseline-first, evidence-driven workflow-discipline pack for AI coding agents (MIT) — "Superpowers upgrade" adding baseline-before-risky-changes, evidence-before-completion, repair/retirement tracks, and risk-scaled guardrails as portable method-pack skills | Agents start coding before goals/architecture/verification are clear and over-claim completion | superpowers, GSD, compound-engineering |
