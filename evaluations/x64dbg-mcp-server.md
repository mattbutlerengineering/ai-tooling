# Evaluation: x64dbg-mcp-server

**Repo:** [duty1g/x64dbg-mcp-server](https://github.com/duty1g/x64dbg-mcp-server)
**Stars:** 1,107 | **Last updated:** 2026-08-24 (pushed) | **License:** MIT
**Last verified:** 2026-08-24
**Last triaged:** 2026-08-24  <!-- triaged: bulk -->
**Dev loop stage:** Review (reverse engineering / malware analysis)
**Layer:** Infrastructure

---

## What it does

Native MCP plugin for the x64dbg Windows debugger, written in Zig with zero dependencies.
It exposes the debugger's full functionality — breakpoints, single-stepping, memory reads,
register dumps — over HTTP, so any MCP-compatible AI assistant can drive x64dbg
programmatically for binary/malware analysis and reverse engineering.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead and
compare it against the catalog's existing IDA Pro MCP servers, not to judge correctness or
runtime behavior.

## Triage note

Left at `discovery-log`. It cites no STACK pick in "Overlaps with" (its closest peers,
`ida-pro-mcp` and `ida-headless-mcp`, are themselves `discovery-log`/SKIP leads, not
adopted incumbents), so it doesn't clear the P2 challenger bar. Not archived, permissively
licensed (MIT), and not a vendored skill/plugin Type, so none of P1/P4/P5 apply either. A
native, dependency-free debugger-control MCP server for a widely-used free debugger is a
differentiated enough addition to the RE/malware-analysis corner of Security & Safety to
deserve a real hands-on look rather than a mechanical disposition.

_Triaged 2026-08-24 by the P3 backlog band (daily discovery)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [x64dbg-mcp-server](https://github.com/duty1g/x64dbg-mcp-server) | MCP server | Native MCP plugin for x64dbg (MIT, Zig, zero deps) exposing the debugger's full functionality over HTTP | Reverse engineering/malware analysis needs a real Windows debugger AI agents can drive — breakpoints, stepping, memory reads, register dumps | ida-pro-mcp, ida-headless-mcp, cve-mcp-server |
