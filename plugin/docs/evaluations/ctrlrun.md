# Evaluation: ctrlrun

**Repo:** [CTRLRun/ctrlrun](https://github.com/CTRLRun/ctrlrun)
**Stars:** 12 | **Last updated:** 2026-09-08 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (agent governance / execution safety)
**Layer:** Infrastructure

---

## What it does

A Python library acting as a safety layer between AI agents and consequential actions — enforces policies requiring human approval for sensitive operations (refunds, deployments, deletions), and prevents duplicate effects from a lost or retried response by making execution at-most-once. Ships adapters for LangGraph and OpenAI Agents, plus an MCP gateway for tool-call policy enforcement.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. None of its overlap citations (decern, agent-governance-toolkit, toolpermit) are STACK picks, so it doesn't clear the P2 challenger bar. 12★ and 5 days old is too early to call it dominated by the more established governance tools it overlaps with — its specific angle (at-most-once execution against duplicate/retried effects, not just a policy gate) looks differentiated enough to leave for a real look rather than a mechanical SKIP.

_Triaged 2026-09-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ctrlrun](https://github.com/CTRLRun/ctrlrun) | tool | Execution safety layer (Apache-2.0) enforcing human-approval policies and at-most-once execution for consequential agent actions (refunds, deploys, deletions) | Agents can double-fire an irreversible action on a lost/retried response, with no approval gate in front of consequential tool calls | decern, agent-governance-toolkit, toolpermit |
