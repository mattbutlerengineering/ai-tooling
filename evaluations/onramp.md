# Evaluation: onramp

**Repo:** [SanyamWadhwa07/onramp](https://github.com/SanyamWadhwa07/onramp)
**Stars:** 1 | **Last updated:** 2026-11-06 (pushed) | **License:** MIT
**Last verified:** 2026-11-06
**Last triaged:** 2026-11-06  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An agent skill for building a verified route through an unfamiliar codebase, checking every
claim it makes against the code itself rather than asserting a summary.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, not SKIPped, despite citing `codegraph` (a STACK pick, ADOPT/MEASURED)
in its Overlaps cell — which lands this lead in the P2 challenger band. The two tools solve
different problems: codegraph is an always-on code-intelligence graph agents query instead of
reading whole files (structural awareness), while onramp's distinguishing claim is
*verification* — every statement in its generated route is checked against the code, which
codegraph does not do. That's a real differentiator, not just a rebrand of the same mechanism,
so this is not SKIPped as redundant. Extremely early (1 star, created today); worth a real
eval once it has more history to confirm the verification claim holds up in practice.

_Triaged 2026-11-06 by the P2 challenger band (daily discovery routine) — leave, not SKIP:
differentiated from its named incumbent (`codegraph`)._
