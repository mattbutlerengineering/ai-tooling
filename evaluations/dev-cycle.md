# Evaluation: dev-cycle

**Repo:** [MaiconPereira/dev-cycle](https://github.com/MaiconPereira/dev-cycle)
**Stars:** 11 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

An agentic development cycle skill for Claude Code, Kiro, and Codex spanning plan, test,
implement, review, verify, and record stages, per the repo's own description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `feature-dev` (STACK, KEEP,
MEASURED) despite the overlap. `feature-dev` is a single-harness (Claude Code)
plan→implement→verify plugin; dev-cycle claims explicit test and record stages plus
Kiro/Codex support that feature-dev does not. Whether that's a real differentiator or
just more stages on paper needs a hands-on eval, not a mechanical SKIP.
