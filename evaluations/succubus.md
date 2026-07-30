# Evaluation: succubus

**Repo:** [enowdev/succubus](https://github.com/enowdev/succubus)
**Stars:** 13 | **Last updated:** 2026-07-28 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Cross-agent coordination for AI coding agents. One daemon, one database — so multiple agents in
one repo can see each other's plan, tasks, and file claims.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (claude-squad, gastown, orca). That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question
the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `beads` (STACK, MEASURED — "work coordination ledger, prevents
duplicate agent effort"). beads already solves exactly the problem succubus describes: multiple
agents in one repo need a shared view of plans/tasks/file claims to avoid collisions. succubus is
a much smaller (13-star), week-old reimplementation of the same coordination-ledger idea with no
disclosed differentiation from the incumbent already in STACK.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
