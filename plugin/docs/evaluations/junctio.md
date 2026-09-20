# Evaluation: junctio

**Repo:** [k2so-dev/junctio](https://github.com/k2so-dev/junctio)
**Stars:** 2 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A self-hosted MCP gateway — one container, one endpoint per client, upstream OAuth that never goes
stale; aggregates stdio, Docker, and remote MCP servers behind a single URL for Claude Code, Codex,
and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (mcp-context-forge, bifrost, Portkey-gateway). Not enough to
support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: no overlapping STACK pick (P3 backlog). Very early (2 stars, created two
days ago) in a niche already served by more mature options (`mcp-context-forge` from IBM,
`bifrost`, `Portkey-gateway`) — not clearly dominated by any single one on scope (junctio's
"OAuth that never goes stale" claim and single-binary self-host framing is a narrower, simpler
pitch than ContextForge's full registry+gateway), so left rather than mechanically SKIPped
pending more signal.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
