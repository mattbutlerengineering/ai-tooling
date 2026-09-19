# Evaluation: no-honest-caveat

**Repo:** [valentinozegna/no-honest-caveat](https://github.com/valentinozegna/no-honest-caveat)
**Stars:** 3 | **Last updated:** 2026-09-17 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

An agent skill that gates a response on "can I resolve this now?" before it is allowed to close
with caveats or unfinished items — aimed at agents that defer or hedge instead of finishing the
work in front of them.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (forward-implementation-first, old-coder, frank). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: overlaps three anti-hedging/anti-caveat skills, none of which is a STACK
incumbent and each targeting a different failure mode (forward-implementation-first = unrequested
bookkeeping scaffolding, old-coder = unproven claims, frank = sycophancy under pushback) rather
than no-honest-caveat's specific "gate on resolvability before allowing a caveat" mechanism.
Very early (3 stars) — worth a first look rather than a mechanical SKIP given no direct incumbent.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
