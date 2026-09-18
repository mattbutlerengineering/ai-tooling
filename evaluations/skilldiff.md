# Evaluation: skilldiff

**Repo:** [scs0209/skilldiff](https://github.com/scs0209/skilldiff)
**Stars:** 3 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

Behavioral regression testing for agent skills: runs a skill inside a real agent harness and diffs
its behavior on every PR, so a skill edit that silently changes behavior gets caught before it
ships.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (skillfid, waza (Microsoft), skill-creator). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped, despite citing STACK pick `skill-creator` in its overlaps.
skill-creator is a skill-*authoring* meta-skill (draft → eval → benchmark → package); skilldiff is
a CI *regression-testing* tool that diffs a skill's behavior across PRs — a different job, closer
in kind to `skillfid` (execution-fidelity checking) and `waza` (Microsoft's skill-eval CLI), neither
of which is a STACK pick. This repo's own `TEMPLATE.md`/detector S track a real gap here (skill
test-design coverage), so a mechanical SKIP against skill-creator would be inconsistent with our
own recorded analysis. Early (3 stars, created today) — worth a real eval once it has more
signal of adoption.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
