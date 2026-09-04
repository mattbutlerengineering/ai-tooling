# Evaluation: agentic-resource-discovery

**Repo:** [neuronto/agentic-resource-discovery](https://github.com/neuronto/agentic-resource-discovery)
**Stars:** 51 | **Last updated:** 2026-09-02 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Federated search across every public agent-resource-discovery (ARD) registry, plus a
verified tool index read from each MCP server's own `tools/list`, hybrid lexical/semantic
retrieval, and a benchmark (ARD-Bench).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata from the daily discovery scan.

## Triage note

No STACK-pick overlap detected (P3 backlog). A genuinely new category — federated MCP
registry/tool discovery — with no directly-redundant catalogued incumbent (closest
conceptual peers, `mcp-context-forge` and `warden`, govern/route already-wired servers
rather than discover new ones). Left at `discovery-log`; worth a real look once it has
more usage history (2 days old, 51★).

_Triaged 2026-09-02 by the P3 backlog band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentic-resource-discovery](https://github.com/neuronto/agentic-resource-discovery) | MCP server | Federated search across every public agent-resource-discovery registry (Apache-2.0), plus a verified tool index read from each MCP server's own tools/list, hybrid lexical/semantic retrieval, and a benchmark | Finding the right MCP server/tool for a task means manually browsing scattered registries with no unified, verified index | mcp-context-forge, warden, mcp-github-trending |
