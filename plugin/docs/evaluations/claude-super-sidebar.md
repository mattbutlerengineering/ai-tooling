# Evaluation: claude-super-sidebar

**Repo:** [Zafer-Liu/claude-super-sidebar](https://github.com/Zafer-Liu/claude-super-sidebar)
**Stars:** 86 | **Last updated:** 2026-10-20 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A visual sidebar (Apache-2.0) showing agent trees, live status, and conversation task
flows for Claude Code and Codex sessions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Bands as a P2 challenger against `abtop` (pressure 1), but the two are differentiated
rather than redundant: `abtop` is a terminal resource/rate-limit monitor across projects,
while this is a visual agent-tree/task-flow sidebar for a single session's structure. Not
worth a mechanical SKIP on that basis. No archived flag, no disqualifying license, no
`Ships inside` container. Left at `discovery-log` for a real hands-on eval.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-super-sidebar](https://github.com/Zafer-Liu/claude-super-sidebar) | tool | Visual sidebar (Apache-2.0) showing agent trees, live status, and conversation task flows for Claude Code and Codex | A bare terminal gives no at-a-glance view of what multiple running agent sessions are doing | agent-orchestration-standard, abtop, peek |
