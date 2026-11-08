# Evaluation: rexpad

**Repo:** [almonk/rexpad](https://github.com/almonk/rexpad)
**Stars:** 46 | **Last updated:** 2026-11-04 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A live todo list for coding agents, rendered in a Rex terminal pane via the kitty graphics
protocol — a running agent's plan stays visible at a glance instead of scrolling off in its own
terminal output.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and its "Overlaps with" cell (`shoulder`, `claude-super-sidebar`, `abtop`). That is
sufficient to check for a named STACK redundancy; it is not sufficient to support an ADOPT, and
this eval offers none.

## Verdict

**discovery-log — tentative read** — cites `abtop` (a STACK pick) as an overlap, but the two cover
different facets of session observability: `abtop` is a token/context/rate-limit monitor, while
rexpad renders the agent's own todo/plan list. Not clearly dominated by the incumbent, so this is
left rather than mechanically SKIPped as redundant. The kitty-graphics-protocol / "Rex pane"
dependency is also unclear from the one-liner alone and worth checking in a hands-on pass.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-08 by the daily discovery-and-triage routine._
