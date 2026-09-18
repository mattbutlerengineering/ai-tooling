# Evaluation: agent-router

**Repo:** [nidhi-singh02/agent-router](https://github.com/nidhi-singh02/agent-router)
**Stars:** 18 | **Last updated:** 2026-09-17 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A CLI that picks Cursor, Claude Code, Codex, or OpenCode plus a model/effort level for a given
task, then launches it — powered by two third-party judgment services (Jev, from TypeSafe.ai, and
Herdr).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (claude-code-router, deadeye-cc, claude-code-routing). Not
enough to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: no overlapping STACK pick (P3 backlog). Solves a different problem than
its catalog neighbors — `claude-code-router`/`deadeye-cc`/`claude-code-routing` route *within* a
single harness (model/effort per step); agent-router picks *which harness* to launch. Depends on
two external, unproven-in-this-catalog services (Jev, Herdr) for its judgment calls, which is worth
noting for whoever runs a real eval. 18 stars, one day old.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
