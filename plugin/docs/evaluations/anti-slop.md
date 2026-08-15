# Evaluation: anti-slop

**Repo:** [AgriciDaniel/anti-slop](https://github.com/AgriciDaniel/anti-slop)
**Stars:** 12 | **Last updated:** 2026-07-28 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-07-30
**Last triaged:** 2026-08-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Finds and repairs substance defects in AI-assisted prose, code, docs, and agent output using
structural tests rather than LLM-as-judge, because LLM judges agree with human "slop" labels only
at chance.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (skylos, brooks-lint, vet). Sufficient to place the lead and
note its scope, not to support an ADOPT.

## Triage note

Left at `discovery-log` rather than SKIPped: `skylos` catches AI-code mistakes (missing guards,
fake helpers, invented APIs) but is scoped to code; `brooks-lint` and `vet` are also code-scoped.
anti-slop's explicit scope spans prose, docs, and agent output as well as code, and its core
methodology claim (structural tests over LLM judgment) is itself worth verifying hands-on rather
than dismissing as redundant with a narrower, code-only incumbent.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._

_Re-confirmed 2026-08-15 by the daily discovery routine (oldest-stamped pass): note this is
`AgriciDaniel/anti-slop`, distinct from `dmmulroy/anti-slop` (an unrelated Oxlint-rules repo
surfaced in today's scan and left uncatalogued as a same-name duplicate — see the scan issue).
Disposition unchanged — left at `discovery-log` for the P0/eval-runner lane._
