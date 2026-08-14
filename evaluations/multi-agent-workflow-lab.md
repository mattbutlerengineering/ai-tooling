# Evaluation: multi-agent-workflow-lab

**Repo:** [christiangrey922/multi-agent-workflow-lab](https://github.com/christiangrey922/multi-agent-workflow-lab)
**Stars:** 85 | **Last updated:** 2026-08-14 (pushed) | **License:** MIT
**Last verified:** 2026-08-14
**Last triaged:** 2026-08-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Testing and observability (MIT) for multi-agent delegation, MCP tool calls, permissions, sandboxed actions, and workflow replay." Instruments multi-agent MCP delegation so a maintainer can see which agent called which tool under what permissions, and replay a workflow run to debug it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to catalog the lead, not to reach a verdict.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`: overlaps `claude-code-hooks-multi-agent-observability` (SKIP verdict already
on file) and `harbor`, but its stated focus — permissions and sandboxed-action visibility across MCP
delegation, plus workflow replay — is not clearly a subset of either existing entry's scope, so a
mechanical "redundant with X" SKIP isn't defensible from metadata alone. Left for a closer look
rather than disposed.

_Triaged 2026-08-14 by the P3 backlog band (daily discovery routine)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [multi-agent-workflow-lab](https://github.com/christiangrey922/multi-agent-workflow-lab) | tool | Testing and observability (MIT) for multi-agent delegation, MCP tool calls, permissions, sandboxed actions, and workflow replay | Multi-agent MCP delegation is opaque — can't see which agent called which tool under what permissions, or replay a run to debug it | claude-code-hooks-multi-agent-observability, harbor, langfuse |
