# Evaluation: r-doc

**Repo:** [riesaexe/r-doc](https://github.com/riesaexe/r-doc)
**Stars:** 16 | **Last updated:** 2026-09-15 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Plan (documentation maintenance)
**Layer:** Tooling

---

## What it does

An agent skill for maintaining a project's AGENTS.md and `docs/` documentation systems — keeping them current as the codebase changes rather than letting them rot silently.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `documentation-and-adrs` on agent-facing project documentation, but none of its citations is a STACK pick, and `documentation-and-adrs` is scoped to ADR templates/decision rationale while this skill is scoped to keeping AGENTS.md and `docs/` current day-to-day — a different job, not a duplicate. Worth a real look rather than a mechanical SKIP. 16★ and 1 day old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [r-doc](https://github.com/riesaexe/r-doc) | skill | Agent skill (MIT) for maintaining project AGENTS.md and docs/ documentation systems | AGENTS.md and project docs drift from the codebase with no agent skill keeping them current | claude-md-doctor, documentation-and-adrs, openwiki |
