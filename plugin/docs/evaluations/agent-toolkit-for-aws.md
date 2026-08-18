# Evaluation: agent-toolkit-for-aws

**Repo:** [aws/agent-toolkit-for-aws](https://github.com/aws/agent-toolkit-for-aws)
**Stars:** 1,805 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

AWS's official agent toolkit: MCP servers plus skills and plugins for agents building on AWS, going beyond raw MCP coverage with first-party skill/plugin packaging.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: CATALOG.md's existing one-liner plus `repo-metadata.json` (1.8K stars, Apache-2.0, pushed 2026-07-10).

## Triage note

Left at `discovery-log`, not SKIPped: the CATALOG entry itself already records this as *complementary* to `awslabs/mcp` (toolkit adds skills+plugins vs. MCP-only), not redundant. As an official first-party AWS artifact it's a reasonable eval candidate, not a mechanical skip.

_Triaged 2026-08-02 by the daily discovery routine (backlog band: P2 challenger);
re-confirmed 2026-08-18 — still complementary to `awslabs/mcp`, not redundant._
