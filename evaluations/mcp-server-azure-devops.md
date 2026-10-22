# Evaluation: mcp-server-azure-devops

**Repo:** [Tiberriver256/mcp-server-azure-devops](https://github.com/Tiberriver256/mcp-server-azure-devops)
**Stars:** 396 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Infrastructure

---

## What it does

An MCP server (MIT, ★396) for Azure DevOps — work items, repos, pipelines, and wikis —
so an agent can read/update Azure DevOps state during development.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `github-mcp-server` (pressure 0), but the two are not
redundant — they serve different, non-overlapping platforms (Azure DevOps vs. GitHub).
A team on Azure DevOps has no GitHub-MCP substitute for this job. Real, established repo
(★396, forked 131×, maintained for over a year). Left at `discovery-log` as a
differentiated platform-specific MCP server rather than SKIPped as redundant.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-server-azure-devops](https://github.com/Tiberriver256/mcp-server-azure-devops) | MCP server | MCP server (MIT, ★396) for Azure DevOps — work items, repos, pipelines, and wikis | Agent needs to read/update Azure DevOps work items and pipelines during development, without a hand-rolled REST integration | mcp-atlassian (complementary: Atlassian = Jira/Confluence, this = Azure DevOps), github-mcp-server |
