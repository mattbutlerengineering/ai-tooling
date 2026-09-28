# Evaluation: opus-manager

**Repo:** [yanauto/opus-manager](https://github.com/yanauto/opus-manager)
**Stars:** 41 | **Last updated:** 2026-09-28 (pushed) | **License:** MIT
**Last verified:** 2026-09-28
**Last triaged:** 2026-09-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code skill that makes Claude the manager rather than the coder: it hands implementation work to cheaper AI CLIs, verifies the results, and gets a second vendor to review before accepting the work.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

No STACK pick in the row's Overlaps with cell (claude-octopus, kodus-ai, deadeye-cc — none is a STACK pick), so this lands in P3 backlog rather than a redundancy band. Newly catalogued (added 2026-09-28); zero overlap pressure keeps it low-priority for now. Left at discovery-log for a future hands-on look rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opus-manager](https://github.com/yanauto/opus-manager) | skill | Claude Code skill (MIT) delegating implementation to cheaper AI CLIs, verifying results, and getting cross-vendor review | Running every step on the expensive model wastes spend when cheaper CLIs can implement and a second vendor can review | claude-octopus, kodus-ai, deadeye-cc |
