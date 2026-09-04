# Evaluation: delx-memory

**Repo:** [davidmosiah/delx-memory](https://github.com/davidmosiah/delx-memory)
**Stars:** 1 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A shared, local-first SQLite memory store any MCP-speaking agent (Claude Desktop, Cursor, Hermes, OpenClaw, Codex) can read and write, so context survives across sessions **and** across tools. Ships 15 MCP tools, secret-blocking, TTL support, multi-agent namespacing, and zero telemetry.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. `triage.py` bands this P2 (challenges `claude-mem`), but claude-mem is a Claude Code-specific plugin while delx-memory's core pitch is cross-tool interoperability — one SQLite store shared across five different agent clients. That's a genuine differentiator, not obviously redundant. Tiny (★1) and unproven; leaving for a real eval to check whether the cross-tool claim holds up.

_Triaged 2026-09-04 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [delx-memory](https://github.com/davidmosiah/delx-memory) | MCP server | Shared local SQLite memory store (MIT) any MCP-speaking agent (Claude, Cursor, Hermes, OpenClaw, Codex) can read/write — context survives across sessions and across tools, with secret-blocking and TTL support | Each tool/session keeps its own throwaway context; want one local, cross-tool memory store with zero telemetry | claude-mem, mex, opencontext |
