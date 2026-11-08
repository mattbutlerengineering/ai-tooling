# Evaluation: mythical-agent-month

**Repo:** [MedAdemBHA/mythical-agent-month](https://github.com/MedAdemBHA/mythical-agent-month)
**Stars:** 20 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

An estimation skill calibrated on real agent runs, stopping an AI agent from quoting a human-dev
timeline (e.g. "5 months") for work it will actually finish in hours.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and its "Overlaps with" cell (`GSD`, `Foreman`, `superbrainstorming`). That is
sufficient to check for a named STACK redundancy; it is not sufficient to support an ADOPT, and
this eval offers none.

## Verdict

**discovery-log — tentative read** — cites `GSD` (a STACK pick) as an overlap, but GSD is a
context-engineering Discuss→Plan→Execute→Verify→Ship loop framework; it does not itself address
the specific bias of estimating agent task duration from human-dev intuition. Not clearly
dominated by the incumbent, so left rather than mechanically SKIPped as redundant. A narrow,
well-targeted skill worth a real hands-on read.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
