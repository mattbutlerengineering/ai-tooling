# Evaluation: claude-statusline-burnrate

**Repo:** [Gui-Gou/claude-statusline-burnrate](https://github.com/Gui-Gou/claude-statusline-burnrate)
**Stars:** 18 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling (CLI statusline)

---

## What it does

A pure bash+jq Claude Code statusline that computes weekly-limit burn-rate math — today's
share of the limit, a sustainable pace, and sleep-aware pacing projections — so you don't
have to keep opening `/usage`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (ccusage, claude-monitor, ccstatusline). That
is sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: ccusage and claude-monitor report historical/live spend; ccstatusline
is a generic customizable statusline. None specifically does weekly-limit burn-rate math
(today's-share + sustainable-pace + sleep-aware projection) inline in the statusline the way
this tool claims to — narrow but real differentiation worth a hands-on look rather than a
redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
