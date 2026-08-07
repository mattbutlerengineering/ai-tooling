# Evaluation: subagent-context

**Repo:** [msshives-gif/subagent-context](https://github.com/msshives-gif/subagent-context)
**Stars:** 2 | **Last updated:** 2026-08-03 (pushed) | **License:** MIT
**Last verified:** 2026-08-07
**Last triaged:** 2026-08-07  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling (Claude Code plugin)

---

## What it does

A Claude Code plugin reporting subagent context-size to the orchestrator and guarding
against re-tasking an already near-overloaded subagent.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (claude-fleet, abtop, headroom). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: claude-fleet and abtop dashboard whole-session status, not
per-subagent context headroom specifically, and headroom compresses tool output rather than
guarding orchestrator re-tasking decisions. The job (a live guard against re-tasking an
overloaded subagent) is narrow but not clearly redundant with a named incumbent — too thin
(2 stars) to confidently judge either way, so left rather than mechanically SKIPped.

_Triaged 2026-08-07 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [subagent-context](https://github.com/msshives-gif/subagent-context) | plugin | Claude Code plugin (MIT) reporting subagent context-size to the orchestrator and guarding against re-tasking an already near-overloaded subagent | Orchestrators re-task subagents without knowing they're near their context limit, risking silent truncation or failure | claude-fleet, abtop, headroom |
