# Evaluation: mcptocodemode

**Repo:** [minkaworks/mcptocodemode](https://github.com/minkaworks/mcptocodemode)
**Stars:** 9 | **Last updated:** 2026-10-23 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement (cross-cutting — reduces MCP tool-call overhead during agent work)
**Layer:** Infrastructure

---

## What it does

A single MCP server that fronts every MCP server already configured on a machine,
presenting only 3 tools plus a sandbox to the model instead of one schema per
upstream tool — the model writes one short program (Code Mode) instead of making a
model turn per tool call. Ships as `npx mcptocodemode setup`, auto-detecting Claude
Code, Codex, Cursor, Grok, OpenCode, Pi, and Claude Desktop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as P3 backlog (no overlap-pressure citation from another row).
It sits beside `warden` (fronts many MCP servers/Skills behind a small tool set),
`mcp-context-forge` (MCP/A2A/REST gateway), and `mcp2cli` (turns an MCP server into a
CLI to avoid loading every schema) — a crowded "stop flooding the prompt with tool
schemas" niche, but the specific Code Mode mechanism (the agent writes and runs a
program against a sandbox instead of making tool calls) is not what any of those
three do, so there is no clean incumbent to call this redundant against yet. Left at
`discovery-log` for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcptocodemode](https://github.com/minkaworks/mcptocodemode) | tool | Puts every configured MCP server behind 3 tools and a sandbox (MIT) so the agent writes one short program instead of dozens of tool calls | Connecting several MCP servers floods the prompt with tool schemas and costs a model turn per call | warden, mcp-context-forge, mcp2cli |
