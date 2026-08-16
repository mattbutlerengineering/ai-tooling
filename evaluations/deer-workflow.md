# Evaluation: deer-workflow

**Repo:** [deerwork-ai/deer-workflow](https://github.com/deerwork-ai/deer-workflow)
**Stars:** 391  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** MIT
**Last verified:** 2026-08-16
**Last triaged:** 2026-08-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Open-source graph engineering runtime that keeps orchestration in TypeScript and delegates
semantic work to replaceable Agent runtimes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (LangGraph, sandcastle, conductor). That is sufficient to
place the lead and note none of its named overlaps are STACK incumbents, not to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: none of LangGraph, sandcastle, or conductor is in STACK, and
deer-workflow's differentiator (orchestration logic decoupled from any one agent SDK, semantic
work delegated to replaceable runtimes) is a real architectural distinction, not a clone. At 365
stars and under two weeks old it has real traction; not a mechanical SKIP. Left for the
P0/eval-runner lane.

_Re-triaged 2026-08-16 by the P3 backlog band — no new STACK pick covers this job; reasoning unchanged._
