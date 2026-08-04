# Evaluation: vibe-coding-prompt-template

**Repo:** [KhazP/vibe-coding-prompt-template](https://github.com/KhazP/vibe-coding-prompt-template)
**Stars:** 2,623 | **Last updated:** 2026-04-19 (pushed) | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Templates and a workflow for generating PRDs, technical designs, and MVP specs before starting
AI-assisted development, so a project begins from structured requirements rather than a vague
prompt.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run these templates. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner and "Overlaps with" cell (`planning-with-files`, `GSD`,
`compound-engineering`). That is sufficient for a SKIP resting on redundancy with a STACK
incumbent, and not sufficient for a positive verdict, which this eval does not offer.

## Verdict

**SKIP** — redundant with [`GSD`](https://github.com/obra/superpowers), and skipped on exactly
the precedent already recorded for its closest peer.

GSD is the installed STACK framework that owns the Plan→Implement→Verify loop, and it already
produces the artifacts these templates produce: durable spec and phase documents, grounded in the
codebase, driven by a state machine rather than a prompt the operator remembers to paste. Adding a
second source of PRD/spec scaffolding puts two answers on the same "plan this" trigger — the same
friction `evaluations/planning-with-files.md` describes when it SKIPs a *higher-quality* skill for
the same reason: *"two planning skills on the same trigger, writing two competing artifact sets …
net friction, not net capability."*

If planning-with-files — mature, hook-enforced, multi-runtime — does not survive that argument, a
static prompt-template repo does not either. It has less to offer against the incumbent, not more:
templates a human pastes, versus GSD's enforced lifecycle.

Watch item recorded rather than relied on: last pushed 2026-04-19, roughly three and a half months
quiet at triage.

Re-open if GSD is ever dropped from STACK — for someone with no planning framework at all this is
a reasonable, zero-cost starting point, and the skip does not claim otherwise.

_Triaged 2026-08-04 by the P2 challenger band ([#265](https://github.com/mattbutlerengineering/ai-tooling/issues/265))._
