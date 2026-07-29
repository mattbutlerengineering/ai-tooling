# Evaluation: succubus

**Repo:** [enowdev/succubus](https://github.com/enowdev/succubus)
**Stars:** 8 | **Last updated:** 2026-07-28 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure (Go daemon + local DB)

---

## What it does

Cross-agent coordination for AI coding agents — one daemon, one database, so multiple agents
working the same repo can see each other's plan, tasks, and file claims. Surfaced in the
2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`agmsg`, `claude-squad`, `beads`, `guild`). `claude-squad`
and `beads` are in STACK.md, but `claude-squad` is a session-manager TUI (not shared-state
coordination) and `beads` is a work ledger, not live task/file-claim visibility across agents —
succubus' actual job (live file-claim + task visibility) is closest to `guild`, which is itself
still `discovery-log`. No clean dominating incumbent, so a mechanical SKIP isn't defensible.

## Triage note

Left at `discovery-log`: very early (8 stars, 1 day old) but fills a real gap — live cross-agent
file-claim visibility isn't clearly covered by any STACK incumbent. Worth revisiting once it has
more signal of traction, or bulk-triaging alongside `guild` given the overlap.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
