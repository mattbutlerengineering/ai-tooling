# Evaluation: mcp-audit-tool

**Repo:** [graygnatconsole/mcp-audit-tool](https://github.com/graygnatconsole/mcp-audit-tool)
**Stars:** 56 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A pure-Python security-audit CLI (MIT) that scans Model Context Protocol server configs for tool
poisoning, rug pulls, hardcoded secrets, command injection, and supply-chain risk, emitting
SARIF for CI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (trustmcp, agent-scan, skill-scanner). That is sufficient to
note the overlap with existing MCP/skill scanners, not to judge whether its specific rule set
(rug pulls, tool poisoning) is materially better or redundant — it would not support an ADOPT,
and this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped as redundant: `trustmcp` and `agent-scan` both scan
MCP servers/agent configs, but neither is a STACK pick, so there is no validated incumbent this
lead is dominated by — three independent MCP scanners already coexist in the catalog with
distinct rule sets (static-only vs. static+dynamic vs. vendor-backed). Worth a first-time
hands-on eval to see how its rug-pull/tool-poisoning detection compares before any redundancy
call.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-audit-tool](https://github.com/graygnatconsole/mcp-audit-tool) | tool | Security-audit CLI (MIT, Python) scanning MCP server configs for tool poisoning, rug pulls, secrets, and command injection | MCP servers/configs ship with no scanner catching tool poisoning, rug pulls, hardcoded secrets, or supply-chain risk before an agent connects | trustmcp, agent-scan, skill-scanner |
