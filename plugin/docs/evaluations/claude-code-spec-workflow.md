# Evaluation: claude-code-spec-workflow

**Repo:** [Pimzino/claude-code-spec-workflow](https://github.com/Pimzino/claude-code-spec-workflow)
**License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Automated spec-driven Claude Code workflow — Requirements→Design→Tasks→Implementation, plus a
Report→Analyze→Fix→Verify bug flow.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (spec-kit, ccpm, GSD, OpenSpec). That is sufficient to place
the lead and note its relationship to STACK's lifecycle-framework pick, not to support an ADOPT —
this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped: `GSD` is STACK's chosen lifecycle framework, but per
STACK.md's own "pick one as primary" note, spec-driven lifecycle frameworks legitimately coexist
as alternatives — `spec-kit` and `OpenSpec`, this tool's closer peers, remain `discovery-log`
rather than SKIP for the same reason. Being consistent with that precedent rather than singling
this one tool out for a mechanical SKIP. Left for the P0/eval-runner lane.

_Triaged 2026-07-30 by the P3 backlog band._
