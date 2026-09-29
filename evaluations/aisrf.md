# Evaluation: aisrf

**Repo:** [keyuraghao/aisrf](https://github.com/keyuraghao/aisrf)
**Stars:** 2 | **Last updated:** 2026-09-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-29
**Last triaged:** 2026-09-29  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

AI Security & Research Framework: every LLM request from an app or agent becomes a ticket a human approves before it reaches the backend. Bundles guardrail integrations (Rebuff, LLM Guard, NeMo, Lakera), red-teaming tools (garak, promptfoo, PyRIT), source code review, reporting, and an MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

None of its cited overlaps (cdmx-in/security-review, agent-scan, agentshield) is a STACK pick, so this lands in P3 backlog rather than a redundancy band. Newly catalogued (added 2026-09-29); 2 stars and 2 days old is too thin to judge past the README. Left at discovery-log rather than SKIPped — the human-approval-gateway framing is distinct from the static skill/MCP scanners already in the catalog and deserves a look once it has more history.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aisrf](https://github.com/keyuraghao/aisrf) | tool | AI Security & Research Framework (Apache-2.0) gating every LLM request behind human approval, plus bundled guardrails, red-teaming, and code review over MCP | Agent/app LLM calls reach the backend with no approval gate, and guardrail/red-team/code-review tooling is wired up by hand, tool by tool | cdmx-in/security-review, agent-scan, agentshield |
