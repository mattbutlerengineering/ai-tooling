# Evaluation: opentelemetry-skill

**Repo:** [o11y-dev/opentelemetry-skill](https://github.com/o11y-dev/opentelemetry-skill)
**Stars:** 49 | **Last updated:** 2026-10-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

An agent skill guiding Claude Code, Codex, and Cursor through production-grade
OpenTelemetry instrumentation and configuration tasks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped. `otelyssey` is a plugin *marketplace* for
OpenTelemetry instrumentation in the Agent Plugins format; opentelemetry-skill is
a single authored skill giving instrumentation guidance directly. Different
mechanism (marketplace of plugins vs. one skill's embedded guidance), and
otelyssey's own catalog row doesn't cite this tool back. Not plainly dominated;
left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-14 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opentelemetry-skill](https://github.com/o11y-dev/opentelemetry-skill) | skill | Agent skill (Apache-2.0) guiding Claude Code, Codex, and Cursor through production-grade OpenTelemetry instrumentation and config | Wiring OpenTelemetry into a codebase by hand means an agent guesses at config with no shared, reviewed instrumentation discipline | otelyssey, logfire |
