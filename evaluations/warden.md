# Evaluation: warden

**Repo:** [chris-asmussen/warden](https://github.com/chris-asmussen/warden)
**Stars:** 10  <!-- repo-metadata.json, fetched 2026-08-04 -->
**License:** MIT
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

One MCP server that fronts many MCP servers and Skills behind a small tool set and routes to the
best one, keeping an agent's context tiny.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (token-optimizer-mcp, Pare, headroom). That is sufficient
to place the lead and note none of its named overlaps are STACK incumbents (headroom is a STACK
pick but solves a different problem), not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: headroom, token-optimizer-mcp, and Pare all *compress tool output*
after a call; warden instead *hides the tool surface itself* behind a router, a different
mechanism for the same underlying context-budget problem. Only 8 stars and a day old — worth a
revisit once it has more traction, but not a mechanical SKIP today. Left for the P0/eval-runner
lane.

_Triaged 2026-07-31 by today's discovery lead; re-confirmed 2026-08-18 — still not a
mechanical SKIP, still worth a hands-on look once it has more traction._
