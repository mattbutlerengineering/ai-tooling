# Evaluation: Assumptions

**Repo:** [Teycir/Assumptions](https://github.com/Teycir/Assumptions)
**Stars:** 17 | **Last updated:** 2026-07-27 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process (skill)

---

## What it does

A SKILL that turns a code diff into an evidence-backed ledger of hidden assumptions, failure
modes, and falsification tests.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (vet, brooks-lint, tdd-guard). Sufficient to place the lead
and note its distinct output artifact, not to support an ADOPT.

## Triage note

Left at `discovery-log` rather than SKIPped: `vet` verifies intent-adherence and correctness,
`brooks-lint` diagnoses design decay against book citations, `tdd-guard` enforces red-green-
refactor mechanically — none of them produce Assumptions' specific artifact, a structured
assumption/failure-mode/falsification-test ledger per diff. Small (17 stars) but a genuinely
different review lens, not a rehash of an existing catalog entry. Left for the P0/eval-runner
lane rather than a mechanical SKIP.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
