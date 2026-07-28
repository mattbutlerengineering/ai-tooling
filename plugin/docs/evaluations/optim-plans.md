# Evaluation: optim-plans

**Repo:** [Optim-Agent/optim-plans](https://github.com/Optim-Agent/optim-plans)
**Stars:** 71 | **Last updated:** 2026-07-28 | **License:** MIT
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A human-in-the-loop planning plugin for Claude and Codex — turns ideas into reviewed Markdown plans, records decisions, enforces explicit execution gates, and provides tested controller primitives so implementation can't start before a plan is reviewed.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 71 stars, MIT, pushed 2026-07-28) plus the CATALOG "Overlaps with" cell against GSD/planning-with-files/spec-kit/plannotator. Sufficient to catalog and note the gap (explicit, enforced execution gates before implementation), not to judge gate-enforcement reliability hands-on.

## Triage note

GSD is already a KEEP/STACK pick for the Plan stage, but optim-plans' differentiator — hard execution gates plus tested controller primitives, rather than GSD's context-engineering loop — is not "plainly dominated" by GSD; the two could be complementary (GSD structures the loop, optim-plans enforces the plan-review gate within it). Left at discovery-log rather than SKIPped, for a future hands-on comparison against GSD.
