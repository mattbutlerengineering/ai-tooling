# Evaluation: numbrone

**Repo:** [stevenmichaelthomas/numbrone](https://github.com/stevenmichaelthomas/numbrone)
**Stars:** 96 | **Last updated:** 2026-11-09 (pushed) | **License:** MIT
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A chief-of-staff router for coding agents — it routes incoming requests to per-project
manager agents, which in turn run parallel worker agents in their own git worktrees, all
riding on top of the `herdr` terminal multiplexer.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and its "Overlaps with" cell (`herdr`, `foreman (ilkemerol)`,
`agent-dispatcher`). That is sufficient to check for a named STACK redundancy; it is not
sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand new (created 2026-11-08) at 96 stars. None of
its cited peers (`herdr`, `foreman`, `agent-dispatcher`) is a STACK pick, so no mechanical
SKIP applies. It adds a manager layer on top of `herdr` rather than duplicating it
outright, which is worth a real hands-on look rather than a redundancy dismissal.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [numbrone](https://github.com/stevenmichaelthomas/numbrone) | tool | Chief-of-staff router (MIT) delegating coding-agent requests to per-project manager agents running parallel workers in git worktrees, on herdr | Running many coding-agent jobs across projects has no manager layer deciding and dispatching work to parallel worktree workers | herdr, foreman (ilkemerol), agent-dispatcher |
