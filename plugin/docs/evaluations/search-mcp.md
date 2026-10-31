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

## Try it in Claude Code

With [Claude Code](https://code.claude.com/docs/en/mcp) installed, run this from the
project where you want to research current API documentation:

```bash
claude mcp add --transport http --scope local Parallel-Search-MCP https://search.parallel.ai/mcp
```

Local scope keeps this opt-in configuration private to you and limited to the current
project. It does not add a shared `.mcp.json` or replace your existing MCP servers.
Start Claude Code in that project and run `/mcp` to confirm the server is connected.

For example, ask:

> Use Parallel-Search-MCP to find the current official documentation for Python's
> `asyncio.TaskGroup`. Fetch the relevant page and explain how task cancellation works,
> citing the source URLs. Distinguish documented behavior from your own inference.

The server exposes `web_search` and `web_fetch`; search uses Fast mode on the anonymous
endpoint. No Parallel account or API key is needed for light use. The free endpoint has
lower rate limits; see the [setup and authentication guide](https://docs.parallel.ai/integrations/mcp/search-mcp)
for higher-limit options. Only send queries and URLs that you can share with a hosted
service, and check the cited documentation before applying an answer to code.

To remove this local configuration:

```bash
claude mcp remove --scope local Parallel-Search-MCP
```

These are setup instructions, not a hands-on search-quality evaluation. The historical
evaluation and triage status below are unchanged.

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
