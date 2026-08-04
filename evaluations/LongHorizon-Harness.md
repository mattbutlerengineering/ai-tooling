# Evaluation: LongHorizon-Harness

**Repo:** [AMAP-ML/LongHorizon-Harness](https://github.com/AMAP-ML/LongHorizon-Harness)
**Stars:** 121 | **License:** MIT
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Harness

---

## What it does

A long-horizon computer-use harness: runs AI agents across desktop apps and the CLI for
extended periods while preserving task state. Features fresh-context execution, durable
verified state, independent auditing, and recoverable progress, with native Claude Code /
Codex / OpenClaw integration.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (UI-TARS-desktop, cua, deer-flow). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: UI-TARS-desktop and cua are themselves `discovery-log`, not STACK
incumbents, and neither claims durable, independently-audited state across extended
multi-hour runs the way this tool does. The differentiation (recoverable progress + auditing
for long-horizon tasks specifically) is worth a real hands-on eval.

_Triaged 2026-08-04 by the daily discovery routine (today's new lead)._
