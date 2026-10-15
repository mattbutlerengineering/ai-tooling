# Evaluation: fde-gym

**Repo:** [deeplethe/fde-gym](https://github.com/deeplethe/fde-gym)
**Stars:** 91 | **Last updated:** 2026-10-11 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-15
**Last triaged:** 2026-10-15  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (agent-evaluation benchmark/judge)
**Layer:** Infrastructure (self-hostable online judge; Docker/Postgres)

---

## What it does

A self-hostable "online judge for the LLM era" — each case is a real customer-delivery
scenario the agent works end-to-end, graded once it's live, on traffic the case never
showed it. Assesses judgment on unwritten requirements and production risk rather than
a diff against known tests.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's description, topics, and the CATALOG.md one-liner/overlaps cell. That is
sufficient to place the lead at `discovery-log`; it would not support an ADOPT, and
this eval offers none.

## Triage note

Left at `discovery-log`. A newly catalogued lead (created 2026-10-06) with no
archival, license, or STACK-redundancy signal that would license a mechanical SKIP —
`overlap_pressure` is 0 and it cites no STACK pick. A real verdict needs a hands-on
run against the judge's own grading loop, which is outside eliminate-only authority.
Left for a future hands-on eval or the P0/`eval-runner` lane.

_Triaged 2026-10-15 by the P3 backlog band._
