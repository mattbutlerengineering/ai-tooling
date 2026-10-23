# Evaluation: lunopeak

**Repo:** [idevtim/lunopeak](https://github.com/idevtim/lunopeak)
**Stars:** 1 | **Last updated:** 2026-10-22 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A local-first desktop dashboard (TypeScript/Rust, Tauri) for repos, sessions, agents,
costs, and configs across Claude Code, Codex, and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Pressure 0 — nothing in the catalog cites it yet. Its "Overlaps with" cell names
`agentsview`, `claude-monitor`, and `vibe-log-cli`, none of which is a STACK pick, so this
does not band as a P2 challenger. No archived flag, no disqualifying license (MIT), no
`Ships inside` container. Very low signal so far (★1, no discussion activity) — a crowded
corner of the catalog (cost/session dashboards) with several established peers already
present. Left at `discovery-log` rather than SKIPped as redundant, since "several peers
exist" is not the same as "clearly dominated" and this bulk pass makes no behavioral
comparison.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lunopeak](https://github.com/idevtim/lunopeak) | tool | Local-first desktop dashboard (MIT) for repos, sessions, agents, costs, and configs across Claude Code, Codex, and Cursor | Tracking coding-agent sessions and spend across several harnesses means checking each tool separately | agentsview, claude-monitor, vibe-log-cli |
