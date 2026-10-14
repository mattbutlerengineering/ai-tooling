# Evaluation: claude-code-usage-quota-mod

**Repo:** [anantraghunath/claude-code-usage-quota-mod](https://github.com/anantraghunath/claude-code-usage-quota-mod)
**Stars:** 23 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A statusline band for Claude Code showing 5-hour and weekly account usage, a
forecast of whether you'll hit limits before they reset, context-window usage,
and one-click/automatic context compacting.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Triage bands this P2 challenger against `ccusage`, but `ccusage` is a retrospective
CLI report over session logs, not a live statusline with a forward-looking
reset-window forecast — closer in spirit to `claude-statusline-burnrate`'s burn-rate
math and `claude-monitor`'s live tracking, both already named in the overlaps cell.
Differentiated by pairing the forecast with automatic/one-click compacting in the
same band; left at `discovery-log` for a real hands-on eval rather than a
mechanical SKIP.

_Triaged 2026-10-14 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-usage-quota-mod](https://github.com/anantraghunath/claude-code-usage-quota-mod) | plugin | Statusline band (MIT) for Claude Code showing 5-hour/weekly usage, a limit-reset forecast, context %, and one-click/automatic compacting | Hitting Claude's usage limits mid-task comes as a surprise with no live forecast against the reset window | claude-statusline-burnrate, ccusage, claude-monitor |
