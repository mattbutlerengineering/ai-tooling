# Evaluation: context-guard

**Repo:** [dividehex/context-guard](https://github.com/dividehex/context-guard)
**Stars:** 3 | **Last updated:** 2026-09-15 (pushed) | **License:** MIT
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A deterministic health monitor (MIT, Rust) for LLM conversations that detects context pressure,
drift, repetition, and tool anomalies without adding anything to the model's own context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (ctxwise, mex, headroom). That is sufficient to note the
overlap with existing context tooling, not to judge whether its drift/anomaly detection is
materially better or redundant — it would not support an ADOPT, and this eval offers none.

## Triage note

`triage.py` bands this P2 (challenges `headroom`, a STACK pick) on citation alone, but the two
tools solve different problems: `headroom` compresses verbose tool output/logs before they reach
the model to cut token usage, while `context-guard` is a passive, deterministic health monitor
detecting context pressure, drift, repetition, and tool-call anomalies — a diagnostic signal, not
a compressor. Not clearly dominated by the incumbent; left at `discovery-log` for a first-time
hands-on eval rather than SKIPped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [context-guard](https://github.com/dividehex/context-guard) | tool | Deterministic health monitor (MIT, Rust) for LLM conversations — context pressure, drift, repetition, and tool anomalies | No mechanical signal exists that context pressure, drift, or tool-call anomalies are building up in a conversation before it degrades | ctxwise, mex, headroom |
