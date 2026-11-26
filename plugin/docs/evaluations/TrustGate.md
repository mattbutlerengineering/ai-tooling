# Evaluation: TrustGate

**Repo:** [NeuralTrust/TrustGate](https://github.com/NeuralTrust/TrustGate)
**Stars:** 14 | **Last updated:** 2026-11-26 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-26
**Last triaged:** 2026-11-26  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hosted, Go-written AI gateway for LLM/agent traffic — multi-provider routing,
guardrails, semantic caching, and MCP support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and the "Overlaps with" cell.

## Triage note

Left at `discovery-log` — cites no STACK pick in its "Overlaps with" cell (`litellm`,
`bifrost`, `Portkey-gateway` are catalogued peers but none is installed in STACK today), so
no mechanical P2 redundancy SKIP applies. Brand-new repo (created 2026-11-24, 14 stars); worth
revisiting once it has more track record before a hands-on eval.

_Triaged 2026-11-26 by the daily discovery routine (new lead, same-day triage)._
