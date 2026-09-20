# Evaluation: agent-track

**Repo:** [narekgevorgyan/agent-track](https://github.com/narekgevorgyan/agent-track)
**Stars:** 1 | **Last updated:** 2026-09-07 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

A self-hosted task board for AI coding agents — one Cloudflare Worker, a D1 database, a live web UI, an 8-tool MCP server, and a companion skill.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. A shared, human-and-agent-visible kanban board (with its own hosted backend) is a different shape from the local dashboards it overlaps with (agentacct, claude-fleet, agentsview all read local session logs rather than hosting shared task state). 1★, today — too early to call it redundant with any of them.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-track](https://github.com/narekgevorgyan/agent-track) | tool | Self-hosted task board (MIT) for AI coding agents — one Cloudflare Worker, D1, a live web UI, an 8-tool MCP server, and a skill | Coding-agent task/plan state has no shared, inspectable board across agent and human, only ad-hoc todo lists | agentacct, claude-fleet, agentsview |
