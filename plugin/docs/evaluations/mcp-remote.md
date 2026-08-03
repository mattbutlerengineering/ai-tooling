# Evaluation: mcp-remote (abluva)

**Repo:** [abluva/mcp-remote](https://github.com/abluva/mcp-remote)
**Stars:** 12 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Bridge for remote MCP — seamless OAuth, resilient auth recovery, and production-grade reliability
for connecting to remote MCP servers.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (mcp-context-forge, bifrost, warden). That is sufficient to
place the lead and note none of its named overlaps is a STACK incumbent, not to support an ADOPT —
this eval offers none.

## Triage note

Left at `discovery-log`: mcp-context-forge/bifrost/warden are broader gateways (federation,
provider routing, context-tiny tool fronting) rather than tools focused specifically on remote
MCP's OAuth resilience; that narrower, real pain point (auth flows that break and don't recover) is
not squarely covered by the named overlaps. Very low traction (12 stars, 3 days old) — watch for
maturity. Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead._
