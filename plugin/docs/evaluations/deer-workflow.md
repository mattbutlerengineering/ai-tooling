# Evaluation: deer-workflow

**Repo:** [deerwork-ai/deer-workflow](https://github.com/deerwork-ai/deer-workflow)
**Stars:** 373 | **Last updated:** 2026-07-27 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An open-source graph-engineering runtime (TypeScript) that keeps orchestration
structure in code and delegates the semantic (LLM) work to replaceable agent
runtimes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `LangGraph`, `sandcastle`, and `agent-kit`, all substantial incumbents, but
deer-workflow's pitch (keep the graph in versioned TypeScript rather than have the
LLM re-derive orchestration structure each run) is a real differentiator worth a
head-to-head comparison, not a name-only SKIP. 373 stars in under a week signals
real traction. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
