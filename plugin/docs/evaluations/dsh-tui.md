# Evaluation: dsh-TUI

**Repo:** [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI)
**Stars:** 1,460 | **Last updated:** 2026-08-16 (pushed) | **License:** MIT
**Last verified:** 2026-08-16
**Last triaged:** 2026-08-16  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Claude-Code-style terminal UI plugin for DeepSeek Harness — status bar, streaming thoughts,
context/TPS gauges, double-Esc rollback.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (ccstatusline, claude-hud, deepseek-harness). That is
sufficient to place the lead and note none of its named overlaps are STACK incumbents, not to
support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: ccstatusline and claude-hud are Claude-Code-specific status displays and
neither is in STACK; dsh-TUI targets a different harness (DeepSeek Harness) with no Claude Code
equivalent doing this job. Different ecosystem, not redundant. Left for the P0/eval-runner lane.

_Triaged 2026-08-16 by the P3 backlog band._
