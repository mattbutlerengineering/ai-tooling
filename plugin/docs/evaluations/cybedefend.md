# Evaluation: cybedefend

**Repo:** [CybeDefend/cybedefend](https://github.com/CybeDefend/cybedefend)
**Stars:** 77 | **Last updated:** 2026-11-25 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-11-26
**Last triaged:** 2026-11-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Agentic ASPM (application security posture management) billed as an open-source Snyk
alternative — runs a full security audit (SAST-style findings across a codebase) in one
command.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (license, stars, push date) plus the CATALOG "Overlaps with" cell. That is
sufficient for the verdict below, because it turns on licensing, not behaviour — a question
the license answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — AGPL-3.0. This scan's license bar admits only permissive (MIT-like) licenses;
copyleft disqualifies a tool from adoption regardless of capability. `agent-scan` and
`agentshield` already cover AI-agent/MCP-config security scanning under permissive licenses
(Apache-2.0 / MIT) in STACK-adjacent territory, and `skylos` covers general static-analysis
security scanning under Apache-2.0.

_Triaged 2026-11-26 by the daily discovery routine (new lead, same-day triage)._
