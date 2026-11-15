# Evaluation: runelay

**Repo:** [Andsu-dev/runelay](https://github.com/Andsu-dev/runelay)
**Stars:** 10 | **Last updated:** 2026-11-15 (pushed) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A self-hosted, open-source MCP gateway providing one endpoint for every
account, skill, and memory store an agent uses across Claude Code, Codex, and
Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier. Joins an already-crowded MCP-gateway cluster
(`mcp-context-forge`, `junctio`, `skgate`) but at only 10 stars and days old,
there isn't yet a basis to call it dominated or differentiated. Left at
`discovery-log` for a full hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [runelay](https://github.com/Andsu-dev/runelay) | tool | Self-hosted MCP gateway (MIT) — one endpoint for every account, skill, and memory your agents use | MCP servers, accounts, and memory stores accumulate per client with no single governed endpoint for Claude Code, Codex, and Cursor | mcp-context-forge, junctio, skgate |
