# Evaluation: agent-delivery-gates

**Repo:** [emiquelito/agent-delivery-gates](https://github.com/emiquelito/agent-delivery-gates)
**Stars:** 0 | **Last updated:** 2026-09-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-12
**Last triaged:** 2026-09-12  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A delivery gate for AI coding agents that mutates code on purpose and re-runs a
change's new tests against the pre-change code, to check whether they actually
catch the break a report claims is handled — runnable as a git hook, CI step, or
MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Distinct from `stryker-js` (general JS/TS mutation testing) and `qodo-cover`
(discontinued test-generation) in scope — it targets exactly the new tests a change
adds, framed as a delivery gate rather than a general test-quality tool. Zero stars
and two days old; left at `discovery-log` rather than SKIPped as redundant, since it
isn't a clean subset of an existing incumbent.
