# Evaluation: portable-handoff

**Repo:** [legoambarish/portable-handoff](https://github.com/legoambarish/portable-handoff)
**Stars:** 15 | **Last updated:** 2026-08-20 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-22
**Last triaged:** 2026-08-22  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting (Memory & Context)
**Layer:** Tooling

---

## What it does

A CLI that maintains the same project context across AI chats, models, and coding agents, so switching tools mid-task doesn't mean re-explaining the project from scratch.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a leave decision, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `handoff-skill` already covers cross-agent handoff documents, but the Memory & Context category is large and dense with near-neighbors (storybloq, byterover-cli, getspecstory) where "redundant" calls have historically needed a real hands-on comparison rather than a metadata skim. Low stars (15) and very new (created 2026-08-18); worth revisiting with more signal before a redundancy call.

_Triaged 2026-08-22 by the P3 backlog band._
