# Evaluation: stargate

**Repo:** [dogo/stargate](https://github.com/dogo/stargate)
**Stars:** 0 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A deliberately small, local, vendor-agnostic orchestrator that lets multiple AI coding agents (Claude, Codex, Kiro, etc.) collaborate on one software task without concurrently editing the same checkout — using isolated git worktrees, linear or fan-out parallel execution, token budgeting, retries, and resumable runs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog) — no existing STACK pick's "Overlaps with" cell cites it. It sits in the same conceptual space as `gastown`/`worktrunk`/`orca` (worktree-isolated multi-agent coordination), but is small, brand-new, and unproven; not a mechanical SKIP candidate. Worth a look if the fan-out-with-token-budgeting angle turns out to be genuinely differentiated from the existing worktree-management tools.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stargate](https://github.com/dogo/stargate) | tool | Small, local, vendor-agnostic orchestrator (MIT) letting AI agents collaborate on one task via isolated git worktrees — linear or fan-out parallel execution, token budgeting, retries, resumable runs | Multiple agents touching the same checkout conflict; want safe worktree isolation plus an orchestration layer without a heavyweight platform | gastown, buildd, worktrunk, orca |
