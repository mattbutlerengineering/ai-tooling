# Evaluation: cyvisguard

**Repo:** [flankerhqd/cyvisguard](https://github.com/flankerhqd/cyvisguard)
**Stars:** 36 | **Last updated:** 2026-07-27 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (agent security / Outer Loop)
**Layer:** Infrastructure

---

## What it does

A security control plane for AI agents — identity and delegation, capability policy enforcement, data-flow taint tracking, and a live audit trail, enforced over MCP. Claims to guard a real Claude Code end to end.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 36 stars, Apache-2.0, pushed 2026-07-27) plus the CATALOG "Overlaps with" cell against agent-governance-toolkit/NeMo-Guardrails/superagent/agnix. Sufficient to catalog and note the gap (MCP-enforced capability policy + taint tracking specifically), not to judge enforcement robustness or bypass resistance hands-on.

## Triage note

Overlaps agent-governance-toolkit (Microsoft's broader OWASP-Agentic-mapped governance toolkit, also discovery-log and not a STACK pick) closely enough to warrant comparison, but cyvisguard's narrower MCP-enforced identity/taint/audit focus is differentiated rather than dominated. No STACK incumbent to SKIP against. Left at discovery-log for a future hands-on eval.
