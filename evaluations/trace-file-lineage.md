# Evaluation: trace-file-lineage

**Repo:** [uczltw6/trace-file-lineage](https://github.com/uczltw6/trace-file-lineage)
**Stars:** 136 | **Last updated:** 2026-07-31 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A CLI that traces which script, notebook, data source, command, or AI agent produced
a given file — locally, with evidence and honest uncertainty rather than a guess.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `re_gent` and `h5i`, but both of those are narrower — prompt-level git
provenance for *code* changes specifically. trace-file-lineage is broader (any file:
data, notebooks, config) and works without adopting a new VCS layer. Differentiated
enough to deserve a real hands-on eval rather than a mechanical SKIP; left at
`discovery-log`.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
