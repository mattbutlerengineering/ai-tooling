# Evaluation: mcp-airlock

**Repo:** [Shalimov04/mcp-airlock](https://github.com/Shalimov04/mcp-airlock)
**Stars:** 21 | **Last updated:** 2026-09-15 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (agent governance / MCP policy enforcement)
**Layer:** Infrastructure

---

## What it does

A stateless governance proxy sitting in front of MCP tool calls — policy enforcement, dry-run mode, human-confirmation gates, audit logging, and tracing, so an agent's MCP tool calls pass through a policy layer instead of executing unchecked.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `toolpermit`, `ctrlrun`, and `decern` on agent tool-call governance, but none is a STACK pick, and it is scoped specifically to the MCP protocol layer (a stateless proxy in front of MCP calls) rather than a general agent-governance framework — a narrower, differentiated angle worth a real look rather than a mechanical SKIP. 21★ and 2 days old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mcp-airlock](https://github.com/Shalimov04/mcp-airlock) | tool | Stateless governance proxy (MIT) for MCP tool calls — policy, dry-run, human confirmation, audit, tracing | MCP tool calls execute with no policy gate, human confirmation, or audit trail in front of them | toolpermit, ctrlrun, decern |
