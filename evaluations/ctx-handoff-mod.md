# Evaluation: ctx-handoff-mod

**Repo:** [cablate/ctx-handoff-mod](https://github.com/cablate/ctx-handoff-mod)
**Stars:** 47 | **Last updated:** 2026-10-08 (pushed) | **License:** MIT
**Last verified:** 2026-10-08
**Last triaged:** 2026-10-08  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A Claude Code mod that hands off to a fresh conversation when context fills up,
keeps the cache warm while you're away, and turns what you taught Claude into
durable project notes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval
offers none.

## Verdict

**SKIP** — redundant with `headroom` (MEASURED STACK pick) — both exist to keep a
session usable as context fills; headroom compresses tool output to delay the fill,
this mod automates the restart after it happens. Same job, STACK already has a
measured answer for it, and a second tool earns nothing without evidence it does
the handoff better than a manual restart plus headroom's compression.

_Triaged 2026-10-08 by the P2 challenger band._
