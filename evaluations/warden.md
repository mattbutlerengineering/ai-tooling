# Evaluation: warden

**Repo:** [chris-asmussen/warden](https://github.com/chris-asmussen/warden)
**Stars:** 10 | **Last updated:** 2026-07-31 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

One MCP server that fronts many other MCP servers and skills behind a small tool
set, and routes each call to the best one — keeping an agent's context small instead
of loading every downstream server's schema up front.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `mcp-context-forge`, but that IBM-backed gateway federates for governance
(auth/rate-limiting/observability across MCP+A2A+REST); warden's angle is dynamic
tool-selection to shrink context, which is a different mechanism for a different
problem (context bloat, not governance). Very early (10 stars, 2 days old) — left at
`discovery-log` rather than SKIPped, since the differentiation is real even though
traction is unproven.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
