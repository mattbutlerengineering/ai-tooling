# Evaluation: mcp-atlassian

**Repo:** [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)
**Stars:** 5,708 | **License:** MIT
**Last verified:** 2026-08-08
**Last triaged:** 2026-08-08  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

One MCP server covering both Atlassian products, exposing Jira and Confluence as separate
tool groups.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: this row is the umbrella entry for the same repo that `jira` and
`confluence` already catalogue as facets (each declaring `Ships inside:
sooperset/mcp-atlassian`) — not a duplicate lead but the container those two rows already
name. Nothing to SKIP here: the repo is already represented in the catalog via its two
component rows, and this row itself remains a legitimate install target for someone who
wants both tool groups from one server rather than choosing a single facet.

_Triaged 2026-08-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-atlassian](https://github.com/sooperset/mcp-atlassian) | MCP server | One MCP server covering both Atlassian products, exposing Jira and Confluence as separate tool groups (MIT) | Agent needs to read and update tickets and pages in Atlassian during development, without two servers | github-mcp-server (complementary: Atlassian = issues/docs, GitHub = code), linear |
