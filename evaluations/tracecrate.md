# Evaluation: tracecrate

**Repo:** [FankChen/tracecrate](https://github.com/FankChen/tracecrate)
**Stars:** 50 | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A local-first trace workbench that inspects Claude Code, Codex, and OTLP agent logs,
lets you compare runs side by side, and exports privacy-conscious reports — no backend
service and no API keys required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That distinguishes its job (run
comparison/debugging) from the cost-focused observability tools already catalogued,
but doesn't establish how well it actually parses or diffs real session logs.

## Triage note

Left at `discovery-log` rather than SKIPped: `bar-observatory` is the closest
catalogued peer (also local-only, also Claude-Code-log-focused) but is audit/tamper-
evidence-oriented rather than run-comparison-oriented, and `peek`/`ccusage` are
cost-attribution tools, a different job than diffing two runs. No existing catalog
entry does what tracecrate specifically does (cross-run comparison across Claude Code
*and* Codex *and* raw OTLP), so this isn't a clean redundancy call.

_Triaged 2026-09-11 — daily discovery pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tracecrate](https://github.com/FankChen/tracecrate) | tool | Local-first trace workbench (MIT) inspecting Claude Code, Codex, and OTLP agent logs — compares runs and exports privacy-conscious reports with no backend or API keys | Debugging why one agent run diverged from another means manually diffing raw session logs; want a local comparison workbench instead | bar-observatory, peek, ccusage |
