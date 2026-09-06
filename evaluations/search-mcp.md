# Evaluation: search-mcp

**Repo:** [parallel-web/search-mcp](https://github.com/parallel-web/search-mcp)
**Stars:** 12 | **Last updated:** 2026-09-04 (pushed) | **License:** MIT
**Last verified:** 2026-09-06
**Last triaged:** 2026-09-06  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

A hosted MCP server providing free web search and page fetching for agents, with no API key
required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge search
quality or the hosted service's reliability hands-on.

## Triage note

Left at `discovery-log`. P3 backlog — no structural disposition. It overlaps `exa-mcp-server` and
`firecrawl-mcp` on the job (web search/fetch for agents) but differentiates on being a zero-config
hosted option needing no API key; that's a real, if modest, differentiator rather than a clean
redundancy, and it doesn't cite a STACK pick in "Overlaps with" so it isn't banded P2. Stamped and
left for a real eval to weigh the hosted/no-key tradeoff against the incumbents.

_Triaged 2026-09-06 by the P3 backlog band._
