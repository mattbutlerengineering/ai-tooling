# Evaluation: Aegis

**Repo:** [GanyuanRan/Aegis](https://github.com/GanyuanRan/Aegis)
**Stars:** 542 | **Last updated:** 2026-06-17 (pushed; created 2026-04-30) | **License:** MIT | **Install:** natural-language, host-detected method-pack
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
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

**Evidence:** REVIEW

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

**SKIP** — redundant with [`superpowers`/GSD](https://github.com/obra/superpowers) (STACK, `MEASURED`) by its own self-description: it bills itself as a *"Superpowers
upgrade"*. A pack defined as an increment on the incumbent is the clearest case this band has.

The principles it packages — baseline-before-risky-changes, evidence-before-completion, risk-scaled
guardrails — are genuinely the right ones, and the evaluation says so. That is an argument for
wanting them *in* the installed methodology, not for layering a second method pack on top of it;
methodology packs contend for the same turns, and the evaluation frames the choice as exactly that:
*"evaluate whether it beats Superpowers + a verification-before-completion skill."*

The supporting facts do not carry a challenger through that comparison: ★627 against the
incumbent's ★251K, Chinese-first docs, and a self-installing paragraph the evaluation flags as
warranting a careful read before any global install. Self-installing instructions inside a skill
body are a supply-chain surface, not a convenience.

Re-open if evidence-before-completion lands as a standalone skill that composes with GSD rather
than a pack that replaces it.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Aegis](https://github.com/GanyuanRan/Aegis) | skill | Baseline-first, evidence-driven workflow-discipline pack for AI coding agents (MIT) — "Superpowers upgrade" adding baseline-before-risky-changes, evidence-before-completion, repair/retirement tracks, and risk-scaled guardrails as portable method-pack skills | Agents start coding before goals/architecture/verification are clear and over-claim completion | superpowers, GSD, compound-engineering |
