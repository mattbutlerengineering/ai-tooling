# Evaluation: genesis-memory

**Repo:** [HamidRezaeian/genesis-memory](https://github.com/HamidRezaeian/genesis-memory)
**Stars:** 62 | **Last updated:** 2026-09-17 (pushed) | **License:** BSL-1.1 (free for individuals and teams under 10, non-production; converts to MIT 2029-09-11)
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Local-first episodic memory OS for AI coding clients — an MCP daemon plus stateless proxy that
lets agents maintain architectural decisions and debugging insights across sessions, with a
sleep-consolidation pass and a dashboard, while compressing output to cut token spend.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (mex, opencontext, delx-memory). That is sufficient to place
the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`. Not SKIPped as redundant with `mex`/`opencontext`/`delx-memory` — those
are all source-grounded leads themselves, not settled STACK incumbents, so there is no named
tool this row is clearly dominated by. Worth flagging for whoever does pick this up: the license
is **Business Source License 1.1**, not permissive MIT-like OSS (free only for individuals, teams
under 10, and non-production use; converts to MIT in 2029) — this would need to clear that bar
before an ADOPT/KEEP, and is a mechanical-SKIP candidate the day this row's Type ever becomes a
vendored skill/plugin, though as a `tool`/MCP server today it is merely *run*, not copied in.

_Triaged 2026-09-17 by the P3 backlog band._
