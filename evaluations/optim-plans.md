# Evaluation: optim-plans

**Repo:** [Optim-Agent/optim-plans](https://github.com/Optim-Agent/optim-plans)
**Stars:** 99 | **Last updated:** 2026-07-29 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling (Claude/Codex plugin)

---

## What it does

A human-in-the-loop planning plugin for Claude and Codex — turns ideas into reviewed Markdown
plans, records decisions, enforces explicit execution gates, and provides tested controller
primitives for safer agent workflows. Surfaced in the 2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`planning-with-files`, `GSD`, `plannotator`). GSD is KEEP
in STACK.md, but optim-plans' emphasis — explicit execution gates and "controller primitives" as
a reusable library, not just a persistent planning loop — is different enough in kind from GSD's
full Discuss→Plan→Execute→Verify→Ship framework that a mechanical SKIP isn't defensible from
metadata alone; it reads more like a lighter, composable primitive than a competing full loop.

## Triage note

Left at `discovery-log`: plausibly complementary to GSD rather than redundant. Worth a real eval
to confirm whether it's a genuine gap-filler or ends up duplicating GSD's gate behavior.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
