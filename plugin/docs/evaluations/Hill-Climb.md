# Evaluation: Hill-Climb

**Repo:** [Bil0000/Hill-Climb](https://github.com/Bil0000/Hill-Climb)
**Stars:** 136 | **Last updated:** 2026-11-12 (pushed) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Claude Code/Codex skill that keeps a change only if a locked test or
benchmark scores it strictly better than before — making a coding agent prove
"done" against a fixed metric rather than asserting it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier (not archived, not under a disqualifying license,
no declared container). It overlaps conceptually with `gap-trap`/`code-quality`
(mechanical gates on agent output) but isn't dominated by either — the
locked-benchmark-regression angle is a distinct mechanism. Left at
`discovery-log` for a full hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Hill-Climb](https://github.com/Bil0000/Hill-Climb) | skill | Claude Code/Codex skill (MIT) keeping a change only if a locked test or benchmark scores it better | An agent claims a change is "done" with nothing mechanically checking it actually scored better against a fixed metric | gap-trap, code-quality, agent-delivery-gates |
