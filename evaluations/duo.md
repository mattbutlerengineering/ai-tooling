# Evaluation: duo

**Repo:** [Audatic07/duo](https://github.com/Audatic07/duo)
**Stars:** 16 | **Last updated:** 2026-10-02 (pushed) | **License:** MIT
**Last verified:** 2026-10-03
**Last triaged:** 2026-10-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local Electron desktop app (★16, created 2026-10-02) pairing Claude Code and Codex for
chat, pair programming, debates, councils, and code review in one window.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new today (created 2026-10-02). Functionally close to the already-catalogued
`claude-codex-coop` (also a Claude+Codex desktop cross-review app) and to `claude-octopus`
/ `review-skills` (multi-model debate/review) — none of which is a STACK pick, so this does
not band as a P2 challenger. No archived flag, no disqualifying license, no `Ships inside`
container. The overlap with `claude-codex-coop` in particular is close enough that a real
eval should compare the two directly rather than disposing either mechanically. Left at
`discovery-log`.

_Triaged 2026-10-03 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [duo](https://github.com/Audatic07/duo) | tool | Desktop app (MIT) pairing Claude Code and Codex for chat, pair programming, debates, and code review | Single-model sessions get no second opinion; want Claude and Codex collaborating together in one local app | claude-codex-coop, claude-octopus, review-skills |
