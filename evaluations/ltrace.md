# Evaluation: ltrace

**Repo:** [nishantmodak/ltrace](https://github.com/nishantmodak/ltrace)
**Stars:** 1 | **Last updated:** 2026-09-07 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local OpenTelemetry trace viewer (Rust desktop app + CLI + agent skill) for developers and coding agents — inspect trace waterfalls, detect N+1 queries, and verify a test run actually exercised the code path.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Local-first, OTel-native trace inspection aimed specifically at agents verifying their own changes (N+1 detection, test-run verification) is a narrower and more dev-loop-native angle than the LLM-observability platforms (langfuse, opik) it overlaps with, which trace model calls rather than application requests. Too new (1★, today) to call redundant with dev3000 either, which is browser/server-timeline-focused rather than OTel-trace-focused.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ltrace](https://github.com/nishantmodak/ltrace) | tool | Local OpenTelemetry trace viewer (MIT, Rust) for developers and coding agents — waterfalls, N+1 detection, test-run verification | Agents changing backend code can't see request traces to catch N+1 queries or verify a test actually exercised the code path | dev3000, langfuse, opik |
