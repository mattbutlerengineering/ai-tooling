# Evaluation: hermes (Vinyl-Davyl)

**Repo:** [Vinyl-Davyl/hermes](https://github.com/Vinyl-Davyl/hermes)
**Stars:** 17 | **Last updated:** 2026-09-28 (pushed) | **License:** MIT
**Last verified:** 2026-10-03
**Last triaged:** 2026-10-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local-first handoff CLI (Go, ★17, created 2026-09-26) that packs unfinished work on
disk and hands it to the next coding agent — Claude, Cursor, Codex, Antigravity, and
more — with no plugin or cloud involved.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new today (created 2026-09-26). Its "Overlaps with" cell names `cli-continues`,
`claude-rein`, and `cc-switch` — none of which is a STACK pick, so this does not band as
a P2 challenger. No archived flag, no disqualifying license, no `Ships inside` container.
`cli-continues` already covers cross-tool session handoff for 16 agents; this entrant's
differentiator (no plugin, no cloud, pure disk-based handoff) is real but unverified. Left
at `discovery-log` for a real hands-on eval rather than a mechanical disposition on day one.

_Triaged 2026-10-03 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hermes](https://github.com/Vinyl-Davyl/hermes) | tool | Local-first handoff CLI (MIT) packing unfinished work on disk and handing it to the next coding agent | Switching coding agents mid-task or hitting a rate limit loses context, with no plugin or cloud involved | cli-continues, claude-rein, cc-switch |
