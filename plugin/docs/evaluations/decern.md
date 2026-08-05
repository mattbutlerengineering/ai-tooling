# Evaluation: decern

**Repo:** [anivar/decern](https://github.com/anivar/decern)
**Stars:** 11 | **License:** Apache-2.0
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Deterministic authorization plus tamper-evident audit for AI agents, humans, and workloads —
one principal type, safety invariants machine-checked by an SMT solver (cvc5), and every
decision independently verifiable offline. Pure Rust.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (agent-governance-toolkit, NeMo-Guardrails,
godkiller-mcp). That is sufficient to place the lead, not to support an ADOPT — this eval
offers none.

## Triage note

Left at `discovery-log`: agent-governance-toolkit is a broader governance framework without
a stated formal-verification core; NeMo-Guardrails governs conversational behavior, not
authorization decisions; godkiller-mcp gates task-completion claims, not access. An
SMT-solver-checked, offline-verifiable authorization layer is a distinct approach worth a
hands-on look rather than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
