# Evaluation: optim-plans

**Repo:** [Optim-Agent/optim-plans](https://github.com/Optim-Agent/optim-plans)
**Stars:** 195 | **Last updated:** 2026-07-31 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process / Tooling

---

## What it does

A human-in-the-loop planning plugin for Claude and Codex — turns ideas into
reviewed Markdown plans, records decisions, and enforces explicit execution gates
before an agent is allowed to start implementing.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `GSD` (KEEP), `vibe-coding-prompt-template`, and `know-before-act`, but its
angle — explicit, enforced human-approval gates plus tested controller primitives —
is narrower and more mechanical than GSD's full context-engineering loop. Whether it
adds real value on top of an already-adopted GSD workflow is exactly the kind of
question a hands-on eval (not a name-match) should answer. Left at `discovery-log`.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
