# Evaluation: otelyssey

**Repo:** [using-system/otelyssey](https://github.com/using-system/otelyssey)
**Stars:** 25 | **Last updated:** 2026-09-20 (pushed) | **License:** MIT
**Last verified:** 2026-09-20
**Last triaged:** 2026-09-20  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (observability instrumentation feeds retrospection)
**Layer:** Infrastructure (plugin marketplace/registry)

---

## What it does

A self-validating OpenTelemetry plugin marketplace for coding agents, in the Agent
Plugins format — open an issue, the repository validates, reviews, lists, and follows
your plugin.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (openinference, logfire, ltrace). That is
sufficient to place the lead and note none of its named overlaps is a STACK incumbent,
not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: a self-service OTel plugin marketplace is a different job than
the observability platforms/instrumentation libraries it overlaps with (it distributes
plugins rather than instrumenting or visualizing traces itself); not a mechanical SKIP.
Left for the P0/eval-runner lane.

_Triaged 2026-09-20 by today's discovery lead._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [otelyssey](https://github.com/using-system/otelyssey) | tool | Self-validating OpenTelemetry plugin marketplace for coding agents, in the Agent Plugins format | Wiring OpenTelemetry into a coding agent means hand-rolled instrumentation with no shared, reviewed plugin ecosystem | openinference, logfire, ltrace |
