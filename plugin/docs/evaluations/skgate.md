# Evaluation: skgate

**Repo:** [helv-io/skgate](https://github.com/helv-io/skgate)
**Stars:** 8 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A self-hosted, OAuth-protected MCP gateway that can also run the servers it fronts,
plus AI-provider proxying with model aliases.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, stamped only (P3 backlog — no STACK pick cited). The MCP
gateway lane is already populated (`mcp-context-forge`, `bifrost`, `junctio`); skgate's
differentiator is running the servers itself rather than only fronting existing ones,
plus bundled Grok-as-OpenAI-compatible proxying. At ★8 and days old, too early to
judge whether that combination earns a slot over the incumbents.

_Triaged 2026-10-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skgate](https://github.com/helv-io/skgate) | tool | Self-hosted, OAuth-protected MCP gateway (MIT) that can also run the servers it fronts, plus AI-provider proxying with model aliases | Running and securing many MCP servers across clients means ad-hoc per-server auth and no single governed endpoint | mcp-context-forge, bifrost, junctio |
