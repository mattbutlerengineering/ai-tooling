# Evaluation: Assumptions

**Repo:** [Teycir/Assumptions](https://github.com/Teycir/Assumptions)
**Stars:** 17 | **Last updated:** 2026-07-27 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling (Claude Code skill)

---

## What it does

A skill that turns a code diff into an evidence-backed ledger of hidden assumptions, failure
modes, and falsification tests. Surfaced in the 2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`vet`, `brooks-lint`, `guard-skills`). None of those is in
STACK.md, and Assumptions' specific output shape (a structured assumptions/failure-mode/
falsification ledger per diff) is narrower and more specific than any of the three, so a
mechanical SKIP isn't defensible from metadata alone.

## Triage note

Left at `discovery-log`: low stars but a genuinely specific, differentiated review artifact.
Worth a real eval to see if the assumption ledger catches issues generic review tools miss.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
