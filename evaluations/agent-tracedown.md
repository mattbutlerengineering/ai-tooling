# Evaluation: agent-tracedown

**Repo:** [nbn07/agent-tracedown](https://github.com/nbn07/agent-tracedown)
**Stars:** 16 | **Last updated:** 2026-11-02 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

Finds the trace step that caused a wrong answer when an agent's trace reports success
but the final answer is wrong, and replays the run with a fix.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient to
place the lead in a triage band; it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log` — newly catalogued today, no STACK-pick overlap (P3 backlog).
Root-causing a failing step and replaying with a fix is a narrower, more actionable
claim than the general tracing tools (`agenttrace`, `blazo`) it's catalogued beside;
worth a first-time look, not examined further in this pass.

_Triaged 2026-11-02 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-tracedown](https://github.com/nbn07/agent-tracedown) | tool | Finds the trace step that caused a wrong answer (Apache-2.0) and replays the run with a fix | An agent trace reports success even when the final answer is wrong, with no way to locate which step actually caused the error | Tracely, agenttrace, blazo |
