# Evaluation: slideops

**Repo:** [glukicov/slideops](https://github.com/glukicov/slideops)
**Stars:** 36 | **Last updated:** 2026-09-01 (pushed) | **License:** MIT
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Tooling

---

## What it does

Turns a repository into a slide deck that flags when it stops matching the code —
treating documentation as a build artifact rather than prose that silently rots.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata from the daily discovery scan.

## Triage note

No STACK-pick overlap detected (P3 backlog). Conceptually closest to `claude-md-doctor`
and `oo-component-documentation` (both flag doc/instruction drift), but slideops' medium
(a generated slide deck) and trigger (drift detection as a CI-style gate) are distinct
enough not to call it redundant. Left at `discovery-log`.

_Triaged 2026-09-02 by the P3 backlog band (daily discovery-and-triage routine, bulk,
eliminate-only)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [slideops](https://github.com/glukicov/slideops) | tool | Turns a repository into a slide deck (MIT) that flags when it stops matching the code | Documentation and slide decks drift silently from the codebase with nothing flagging when they go stale | claude-md-doctor, oo-component-documentation, open-skill-sunset |
