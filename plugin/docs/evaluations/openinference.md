# Evaluation: openinference

**Repo:** [Arize-ai/openinference](https://github.com/Arize-ai/openinference)
**Stars:** 1,077 | **Last updated:** 2026-07-09 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Outer Loop (tracing standard)
**Layer:** Infrastructure
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

OpenTelemetry-based semantic conventions and instrumentation libraries for LLM and agent
applications — a vendor-neutral way to emit traces any compatible backend can read.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell (`phoenix`, `logfire`, `langfuse`, `opik`). Enough to place it;
not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, and its overlap cell is misleading in a way worth recording.

It is listed as overlapping `phoenix`, `logfire`, `langfuse` and `opik` — all four of which are *backends*.
OpenInference is not a backend; it is the **semantic convention layer** those backends consume: OTel
conventions plus instrumentation for LLM and agent frameworks. Instrument once against it and the backend
becomes a swap rather than a migration. Its relationship to all four is layering, not competition, and a
redundancy pass keying on the overlap cell alone would dispose it wrongly — the same trap `pg-aiguide` sat in
one slice earlier.

That layering matters more after this pass than before it: `phoenix` (from the same authors) was SKIPped over
Elastic License 2.0 terms, and OpenInference is **Apache-2.0**. The convention layer being permissively
licensed is precisely what makes the backend replaceable, which is the argument that leaves `logfire`,
`langfuse` and `opik` all standing as alternatives.

★1.1K is the corroborating detail that it is infrastructure rather than a product — standards layers are
depended on far more often than they are starred.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [openinference](https://github.com/Arize-ai/openinference) | framework | OpenTelemetry instrumentation + semantic conventions for LLM/agent apps (Apache-2.0, by Arize) — auto-instrumentors for OpenAI, Anthropic, LangChain, LlamaIndex, DSPy, CrewAI and more that emit vendor-neutral spans to any OTel backend (Phoenix, langfuse, Jaeger, …) | Want standardized, framework-agnostic tracing of LLM calls without coupling instrumentation to one observability vendor | phoenix, logfire, langfuse, opik |
