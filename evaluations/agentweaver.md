# Evaluation: agentweaver

**Repo:** [sabbour/agentweaver](https://github.com/sabbour/agentweaver)
**Stars:** 5 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Runs an AI agent on a task inside a sandboxed git worktree, streaming every step live and gating merges behind human review. Built with .NET and React, AKS-oriented, and ships an MCP server for integration with tools like GitHub Copilot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog). Conceptually adjacent to `gastown`/`stargate`/`sandcastle` (sandboxed agent execution + human review gate before merge), but the Azure/.NET/AKS orientation is a differentiator worth noting rather than a reason to SKIP as redundant — a team already on AKS may prefer this over a more generic tool. Small (★5) and unproven; leaving for a real eval rather than a mechanical call.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentweaver](https://github.com/sabbour/agentweaver) | tool | Runs an AI agent on a task inside a sandboxed git worktree (MIT), streaming every step live and gating merges behind human review; .NET/React, AKS-oriented, with an MCP server for integration | Running an agent unattended on real code needs live visibility and a human gate before merge, not blind trust | gastown, stargate, sandcastle, worktrunk |
