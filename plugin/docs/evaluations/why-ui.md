# Evaluation: why-ui

**Repo:** [Yudis-bit/why-ui](https://github.com/Yudis-bit/why-ui)
**Stars:** 1 | **Last updated:** 2026-09-06 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Chrome extension paired with an MCP server that surfaces runtime browser evidence — console, network, and DOM state — to a coding agent debugging frontend code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Overlaps chrome-devtools-mcp (official, ★48.5K, far more mature — live Chrome via CDP, Lighthouse, Core Web Vitals) closely enough that a real eval would likely find this redundant, but at 1★ and one day old there isn't enough here yet to write a defensible SKIP naming chrome-devtools-mcp as the incumbent; a mechanical SKIP this early risks disposing something not yet differentiated from, or against, the mature tool.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [why-ui](https://github.com/Yudis-bit/why-ui) | tool | Chrome extension + MCP server (MIT) surfacing runtime browser evidence — console, network, DOM state — to coding agents | Agents debugging frontend issues only see the code, not what actually happened in the browser at runtime | dev3000, chrome-devtools-mcp, agent-browser |
