# Evaluation: exoproc

**Repo:** [w0ldan/exoproc](https://github.com/w0ldan/exoproc)
**Stars:** 89 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-10-31
**Last triaged:** 2026-10-31  <!-- triaged: bulk -->
**Dev loop stage:** None of the standard inner/outer loop — this is domain-specific tooling for Windows reverse engineering / binary analysis, not software-build work. In-scope only as a Security & Safety capability (cf. ida-pro-mcp, Corvus).
**Layer:** Infrastructure

---

## What it does

A TypeScript CLI/MCP toolkit (MIT) for Windows x64 native systems programming — memory manipulation, process instrumentation, and static/dynamic binary analysis, exposed so an AI agent can drive it directly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (ida-pro-mcp, Corvus, ida-headless-mcp). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P3 backlog. Left at `discovery-log`; its overlaps (ida-pro-mcp, Corvus, ida-headless-mcp) are themselves discovery-log leads, not STACK picks, so it doesn't land in P2. Windows-native memory manipulation/process instrumentation is a narrower niche than the existing IDA-centric reverse-engineering MCP servers and deserves its own look rather than a bulk disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [exoproc](https://github.com/w0ldan/exoproc) | tool | TypeScript CLI/MCP toolkit (MIT) for Windows x64 native systems programming — memory manipulation, process instrumentation, and static/dynamic binary analysis for agents | AI agents doing Windows reverse engineering/binary analysis have no native toolkit exposing memory manipulation and process instrumentation over MCP | ida-pro-mcp, Corvus, ida-headless-mcp |
