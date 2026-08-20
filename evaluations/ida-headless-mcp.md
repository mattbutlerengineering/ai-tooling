# Evaluation: ida-headless-mcp

**Repo:** [fuqiuluo/ida-headless-mcp](https://github.com/fuqiuluo/ida-headless-mcp)
**Stars:** 11 | **Last updated:** 2026-08-17 (pushed) | **License:** MIT
**Last verified:** 2026-08-20
**Last triaged:** 2026-08-20  <!-- triaged: bulk -->
**Dev loop stage:** None of the standard inner/outer loop — domain-specific tooling for
reverse engineering, same as its sibling `ida-pro-mcp`. In-scope only as a Security &
Safety capability.
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "Rust-native multi-session headless IDA Pro MCP server (MIT) — one
supervisor, one IDA worker per database, compatible with ida-pro-mcp's public
contract." A Rust supervisor process manages one IDA worker per open database,
exposing the same public MCP contract as `ida-pro-mcp` but without requiring a running
IDA GUI session per client.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata, README, and the CATALOG "Overlaps with" cell.

## Triage note

P3 backlog — no STACK pick cited in "Overlaps with" (`ida-pro-mcp` is catalogued but
not a STACK pick, and is complementary rather than redundant: headless/multi-session
vs. GUI-bound/single-session is a real capability difference). Left at `discovery-log`;
stamped only.

_Triaged 2026-08-20 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ida-headless-mcp](https://github.com/fuqiuluo/ida-headless-mcp) | MCP server | Rust-native multi-session headless IDA Pro MCP server (MIT) — one supervisor, one IDA worker per database, compatible with ida-pro-mcp's public contract | ida-pro-mcp needs a running IDA GUI/idalib per session; want a headless, multi-session RE server agents can drive concurrently | ida-pro-mcp, cve-mcp-server |
