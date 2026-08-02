# Evaluation: mcp-github-trending

**Repo:** [hetaoBackend/mcp-github-trending](https://github.com/hetaoBackend/mcp-github-trending)
**Stars:** 56 | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

An MCP server exposing two tools: `get_github_trending_repositories` and `get_github_trending_developers`, with filters for programming language, time period (daily/weekly/monthly), and spoken language.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: README gathered via web fetch. Sufficient to catalog a narrow, single-purpose MCP server; not sufficient to confirm reliability or freshness of the underlying trending data source.

## Triage note

Left at `discovery-log` rather than SKIPped: no catalogued incumbent does GitHub-trending discovery specifically via MCP (the closest neighbor, `exa-mcp-server`, is general web search/research, not trending-repo discovery). Niche and low-star, but not clearly redundant with a named incumbent, so a mechanical SKIP isn't defensible — left for a real eval or further evidence of adoption.

_Triaged 2026-08-02 by the daily discovery routine (today's new lead)._
