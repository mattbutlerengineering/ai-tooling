# Evaluation: cyvisguard

**Repo:** [flankerhqd/cyvisguard](https://github.com/flankerhqd/cyvisguard)
**Stars:** 45 | **Last updated:** 2026-07-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure (MCP-enforced control plane)

---

## What it does

A security control plane for AI agents — identity and delegation, capability policy, data-flow
taint tracking, and a live audit trail, enforced over MCP; claims to guard a real Claude Code
instance end to end. Surfaced in the 2026-07-29 daily discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`agent-governance-toolkit`, `agentlint`, `superagent`).
None of those is in STACK.md, and none combines identity/delegation + capability policy +
data-flow taint + audit trail specifically *over MCP* the way cyvisguard claims to — the
overlap is topical, not a clean incumbent match, so a mechanical SKIP isn't defensible from
metadata alone.

## Triage note

Left at `discovery-log`: a differentiated security-plane angle (MCP-enforced taint tracking) with
no dominating incumbent. Worth a real eval given the general trend toward stricter agent
governance.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
