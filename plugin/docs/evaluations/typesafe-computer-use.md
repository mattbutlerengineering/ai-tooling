# Evaluation: typesafe-computer-use

**Repo:** [awlevin/typesafe-computer-use](https://github.com/awlevin/typesafe-computer-use)
**Stars:** 401 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Computer-use automation for macOS combining screen OCR with a cheap decision classifier
(TypeSafe.ai's Jev "System One" model) to pick the next action, instead of an expensive
frontier-model call per step — claimed at roughly $0.0002/step for routine navigation.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (UI-TARS-desktop, cua, nuphus-mcp). That is sufficient to
place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: `UI-TARS-desktop` and `cua` are themselves `discovery-log` (no STACK
incumbent for computer-use yet), so there is no incumbent to be redundant with. At 401 stars and a
genuinely different cost/architecture pitch (cheap classifier vs. vision-model-driven agent),
significant enough to deserve a first-time look rather than a mechanical disposition. Depends on a
proprietary TypeSafe API key.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
