# Evaluation: agent-safe-pipeline

**Repo:** [decionis/agent-safe-pipeline](https://github.com/decionis/agent-safe-pipeline)
**Stars:** 294 | **Last updated:** 2026-08-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-14
**Last triaged:** 2026-08-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "Reference architecture (Apache-2.0) where agents propose actions but cannot authorize them — immutable intent capture, an independent policy verdict, and a single-use execution grant." Agents capture intent, an independent Decionis policy verdict (ALLOW/ESCALATE/BLOCK) judges it, a human approval step confirms it, and only then does a SafeExecutor consume a single-use intent-bound grant to actually perform the action.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to catalog the lead, not to reach a verdict.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`: a reference architecture for separating an agent's decision from its
execution authority is a real and underrepresented pattern in the Security & Safety category
(`decern` and `agent-governance-toolkit` are the closest existing entries, both also
un-exercised leads). Not SKIPped as redundant — the single-use intent-bound grant mechanism is
distinct enough from the existing entries' approaches to warrant a first look rather than a
mechanical dismissal.

_Triaged 2026-08-14 by the P3 backlog band (daily discovery routine)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-safe-pipeline](https://github.com/decionis/agent-safe-pipeline) | framework | Reference architecture (Apache-2.0) where agents propose actions but cannot authorize them — immutable intent capture, an independent policy verdict, and a single-use execution grant | Agents that both decide and execute a risky action have no separation of powers; want ALLOW/ESCALATE/BLOCK judged independently before a SafeExecutor consumes a one-time intent-bound grant | decern, agent-governance-toolkit, NeMo-Guardrails |
