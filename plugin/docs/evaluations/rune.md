# Evaluation: rune

**Repo:** [unstablebuild/rune](https://github.com/unstablebuild/rune)
**Stars:** 310 | **Last updated:** 2026-09-11 (pushed) | **License:** GPL-3.0
**Last verified:** 2026-09-12
**Last triaged:** 2026-09-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A terminal-native development environment for coding agents — combines a workspace
manager, terminal multiplexer, and editor in one Go binary, positioned as "the
development environment for pros" for running multiple agent sessions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on the license bar, not on the tool's behaviour — a question this
evaluation does not answer. It would not support an ADOPT, and this eval offers
none.

## Verdict

**SKIP** — GPL-3.0, a copyleft license outside the permissive/MIT-like bar this pass
applies to every new lead. `ai-terminal-manager` and `worktrunk` already cover the
same terminal-workspace-for-agents job under permissive licenses.

_Triaged 2026-09-12 by the daily discovery pass (today's-lead triage)._
