# Evaluation: model-citizen

**Repo:** [JakeSelby/model-citizen](https://github.com/JakeSelby/model-citizen)
**Stars:** 23 | **Last updated:** 2026-09-28 (pushed) | **License:** MIT
**Last verified:** 2026-09-28
**Last triaged:** 2026-09-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A cross-harness control plane for coding agents: one checkout of rules, skills, subagents, hooks, and stances, projected into Claude Code and Codex. Adds hook-enforced guardrails, usage telemetry, cost postures, and model tiering on top of whatever rules library or orchestration layer a team already uses.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

No STACK pick in the row's Overlaps with cell (abide, reporails/cli, deadeye-cc — none is a STACK pick), so this lands in P3 backlog rather than a redundancy band. Newly catalogued (added 2026-09-28); zero overlap pressure and a small stage gap keep it low-priority for now. Left at discovery-log for a future hands-on look rather than a mechanical SKIP — a 216-open-issue count against 23 stars is worth a human glance before any deeper evaluation.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [model-citizen](https://github.com/JakeSelby/model-citizen) | tool | Cross-harness control plane (MIT) for coding-agent rules, skills, hooks, and cost policy | Rules, skills, hooks, and cost policy are duplicated per harness with nothing projecting one checkout into Claude Code and Codex consistently | abide, reporails/cli, deadeye-cc |
