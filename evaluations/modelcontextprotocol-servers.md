# Evaluation: modelcontextprotocol/servers

**Repo:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers)
**Stars:** 89,346 | **License:** MIT
**Last verified:** 2026-08-08
**Last triaged:** 2026-08-08  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting (MCP Servers infrastructure)
**Layer:** Infrastructure

---

## What it does

The protocol authors' reference server monorepo — filesystem, memory, fetch, git,
sequential-thinking and more, each independently installable.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: this is the container repo, not a redundant lead — several of its
members (`server-memory`, `server-filesystem`, `server-github`, `sequential-thinking`) are
already catalogued as their own rows declaring `Ships inside:
modelcontextprotocol/servers`. The container row itself (canonical protocol-author
reference implementations) is not redundant with `fastmcp`/`mcp-use` (those are frameworks
for *building* MCP servers, not a set of reference servers) or `claude-plugins-official` (a
different ecosystem's plugin pack), so a mechanical SKIP against those overlaps would be
wrong. Left for a real look at what, if anything, in this monorepo isn't already covered by
its already-catalogued member rows.

_Triaged 2026-08-08 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers) | MCP server | The protocol authors' reference server monorepo — filesystem, memory, fetch, git, sequential-thinking and more, each independently installable | Need canonical, minimal implementations of the common MCP server patterns rather than third-party reinventions | fastmcp, mcp-use, claude-plugins-official |
