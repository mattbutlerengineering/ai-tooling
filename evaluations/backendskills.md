# Evaluation: backendskills

**Repo:** [globalmpc/backendskills](https://github.com/globalmpc/backendskills)
**Stars:** 39 | **Last updated:** 2026-11-06 (pushed) | **License:** MIT
**Last verified:** 2026-11-06
**Last triaged:** 2026-11-06  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A skill pack stopping AI coding agents from writing backend code that passes a demo and
breaks under production load, concurrency, or edge cases. The repo's own README states a
measured before/after: 25 of 150 runs hit a critical mistake without the skill, 2 of 150 with
it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead and note
its overlap with existing quality-gate tools; it is not sufficient to verify the author's own
25/150-vs-2/150 claim, which would need an independent run.

## Triage note

Left at `discovery-log`. Brand new (created today), zero catalog overlap pressure from any
STACK pick. Its own claimed before/after number is exactly the kind of figure
`evaluations/token-savings-protocol.md`'s sibling (`measurement-protocols.md`) says must be
independently measured before it's trusted, not taken from the README — worth a real eval
later, not a mechanical SKIP today.

_Triaged 2026-11-06 by the P3 backlog band (daily discovery routine)._
