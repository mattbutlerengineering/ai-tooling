# Evaluation: web-mcp-bridge

**Repo:** [AstraxOf/web-mcp-bridge](https://github.com/AstraxOf/web-mcp-bridge)
**Stars:** 10 | **Last updated:** 2026-10-29 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A browser extension plus a Python WebSocket bridge that connects a web-hosted AI chat
interface to local MCP servers — giving a browser-based client the same local-tool
access a desktop coding-agent client already has.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Security implications of bridging a web page to
local MCP servers (origin checks, auth) are untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (mcp-remote, mac-developer-bridge, mcp-vision-bridge are catalogued
leads, not STACK picks). Not examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [web-mcp-bridge](https://github.com/AstraxOf/web-mcp-bridge) | tool | Browser extension + Python WebSocket bridge (MIT) connecting a web-based AI chat interface to local MCP servers | Web-hosted AI chat interfaces have no route to local MCP servers, unlike desktop coding-agent clients | mcp-remote, mac-developer-bridge, mcp-vision-bridge |
