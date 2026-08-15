# Evaluation: CodeJury

**Repo:** [krishagarwal314/CodeJury](https://github.com/krishagarwal314/CodeJury)
**Stars:** 114 | **Last updated:** 2026-07-30 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-08-15  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Terminal-first, knowledge-grounded multi-agent software delivery pipeline: scope requirements,
implement changes, run tests, and gate pull requests with deterministic QA and ensemble code
review.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (BMAD-METHOD, ccpm, flow-next). Sufficient to place the
lead and note how it differs from those peers, not to support an ADOPT.

## Triage note

Left at `discovery-log` rather than SKIPped: `GSD` (STACK, KEEP) is a general Discuss->Plan->
Execute->Verify->Ship loop; CodeJury is a narrower, opinionated end-to-end pipeline that couples
requirements scoping to deterministic QA gates and ensemble review in one system, closer in shape
to `BMAD-METHOD`/`ccpm` (both still `discovery-log`, neither a STACK incumbent) than to GSD. No
STACK pick already covers this specific "gated multi-agent SDLC pipeline" niche, so this isn't a
clean redundancy SKIP — left for the P0/eval-runner lane.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._

_Re-confirmed 2026-08-15 by the daily discovery routine (oldest-stamped pass): `BMAD-METHOD`
and `ccpm` remain `discovery-log`, no STACK pick has moved into this niche; disposition
unchanged — left at `discovery-log` for the P0/eval-runner lane._
