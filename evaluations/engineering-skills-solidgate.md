# Evaluation: engineering-skills (solidgate)

**Repo:** [solidgate-tech/engineering-skills](https://github.com/solidgate-tech/engineering-skills)
**Stars:** 6 | **Last updated:** 2026-11-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Process

---

## What it does

A Claude Code plugin marketplace of the agent skills a real engineering team
(Solidgate) uses day to day: a GitLab MR workflow, a Go service review skill,
ADRs and design docs, planning, and pnpm audit fixes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Cites `mattpocock/skills` in its "Overlaps with" cell, which bands this P2
challenger — but `mattpocock/skills` (already a STACK pick) is a general-purpose
TDD/debugging/planning skill set, while this pack is a specific company's
day-to-day skills scoped to GitLab MR review, Go service review, and pnpm audit
fixes. Installing `mattpocock/skills` does not cover the GitLab/Go-specific
workflow this pack carries, so SKIPping it as "redundant" would be the false-SKIP
the P2 band's guardrail warns against. Left at `discovery-log` — whether a
production team's own skill pack earns a slot alongside the generic one would need
a first-time eval, not a mechanical SKIP.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [engineering-skills (solidgate)](https://github.com/solidgate-tech/engineering-skills) | skill | Claude Code plugin marketplace (Apache-2.0) of the skills a real engineering team uses daily — GitLab MR workflow, Go service review, ADRs, pnpm audit fixes | Teams want a real company's day-to-day skill set instead of a generic skill grab-bag with no production pedigree | mattpocock/skills, agent-skill-creator, governed-agent-skills |
