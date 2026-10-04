# Evaluation: factorylog

**Repo:** [flaviocopes/factorylog](https://github.com/flaviocopes/factorylog)
**Stars:** 56 | **Last updated:** 2026-10-04 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A macOS app (Swift, ★56, created 2026-10-01) that builds a timeline of what AI coding
agents did each day and week, by project, so you can see where the time actually went
without reconstructing it from scattered session logs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps with `vibe-log-cli` (already `SKIP`) and `agentacct`/`claude-fleet`
(discovery-log/SKIP) — all time/activity dashboards for coding-agent sessions, none a
STACK pick, so this does not band as a P2 challenger against any incumbent. No archived
flag, no disqualifying license, no `Ships inside` container. Left at `discovery-log`
rather than mechanically disposed, since "daily/weekly timeline across projects" is a
narrower, more specific framing than its listed peers and deserves its own look.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [factorylog](https://github.com/flaviocopes/factorylog) | tool | macOS app (MIT) building a daily/weekly timeline of what your coding agents did, project by project, and where the time went | Coding-agent work across projects leaves no at-a-glance record of what got done each day/week without checking each session | vibe-log-cli, agentacct, claude-fleet |
