# Evaluation: system-design-skill

**Repo:** [pinchen147/system-design-skill](https://github.com/pinchen147/system-design-skill)
**Stars:** 26 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

A skill (MIT) that reads a repo's current architecture, runs capacity math, and compares
candidate designs into an interactive evidence report — system design from the repo's
actual constraints rather than from vibes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `GSD` (ADOPT, pressure 0), but the overlap is shallow:
GSD is a general dev-loop orchestration framework, while this is narrowly scoped to
architecture/capacity-math comparison — a distinct, specialized job GSD does not claim to
do. Established for ~3 months (created 2026-07-30, ★26). Left at `discovery-log` rather
than SKIPped as redundant.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [system-design-skill](https://github.com/pinchen147/system-design-skill) | skill | Skill (MIT) that reads a repo's current architecture, runs capacity math, and compares candidate designs into an interactive evidence report | Architecture decisions default to vibes instead of the repo's actual constraints and load math; want an evidence-backed comparison | GSD, Archon, codebase-map |
