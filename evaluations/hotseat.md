# Evaluation: hotseat

**Repo:** [Maxteabag/hotseat](https://github.com/Maxteabag/hotseat)
**Stars:** 4 | **Last updated:** 2026-09-16 (pushed) | **License:** MIT
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A terminal dashboard and CLI (Go) for Claude Code and Codex accounts — shows quota status
and surfaces the work a usage limit interrupted.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `ccusage` (P2's catalogued incumbent) reports
token/cost spend from session logs; hotseat is quota-status-and-recovery focused —
cross-provider (Claude Code + Codex) account quota and what work a limit stopped — a
different job than cost reporting. Not clearly dominated by ccusage; left for a real look.

_Triaged 2026-09-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hotseat](https://github.com/Maxteabag/hotseat) | tool | Terminal dashboard and CLI (MIT, Go) for Claude Code and Codex accounts — quota status and the work a usage limit stopped | Usage-limit interruptions leave work stranded with no single view of quota across Claude Code/Codex accounts or what stopped | claude-monitor, ccusage, brink |
