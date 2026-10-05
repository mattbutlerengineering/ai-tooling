# Evaluation: blazo

**Repo:** [agentblazo/blazo](https://github.com/agentblazo/blazo)
**Stars:** 46 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Traces agent runs — tool calls, LLM calls, errors, latency, tokens — with a stated goal
of eventually detecting agents that are stuck or caught in loops.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, stamped only — no STACK pick cited in overlap pressure (P3
backlog). Sits in an already-populated local agent-observability cluster
(`agenttrace`, `bar-observatory`, `tracecrate`); the stuck-loop-detection angle is
called out by the project itself as not yet built ("eventually detection for agents
that appear stuck"), so there isn't yet a shipped capability to judge against the
incumbents.

_Triaged 2026-10-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [blazo](https://github.com/agentblazo/blazo) | tool | Traces agent runs (MIT) — tool calls, LLM calls, errors, latency, tokens — toward detecting agents stuck in loops | Agent runs that go stuck or loop are invisible without a dedicated trace/observability layer | agenttrace, bar-observatory, tracecrate |
