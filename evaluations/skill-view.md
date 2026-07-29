# Evaluation: skill-view

**Repo:** [pc-style/skill-view](https://github.com/pc-style/skill-view)
**Stars:** 56 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (local web GUI)

---

## What it does

A local-only web GUI for inspecting installed `SKILL.md` files across user, project, plugin,
cache, and marketplace sources. Surfaced in the 2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`skills-hub`, `capa`, `skills-manage`). None of those is in
STACK.md, and skill-view's angle (a browsable local GUI specifically for inspection, not
install/sync) is distinct enough from `skills-hub`'s cross-editor sync or `capa`'s single config
format that a mechanical SKIP isn't defensible from metadata alone.

## Triage note

Left at `discovery-log`: a small, focused inspection tool with no clear dominating incumbent.
Worth a real eval if skill sprawl across sources becomes a bigger pain point.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
