# Evaluation: old-coder

**Repo:** [AmazingAng/old-coder](https://github.com/AmazingAng/old-coder)
**Stars:** 166 | **Last updated:** 2026-07-27 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process (skill)

---

## What it does

An "old coder's strategy for the agent era" — don't read the code, make it run the gauntlet.
Evidence-first development skill for coding agents, inspired by Uncle Bob's TDD discipline.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (tdd-guard, vet, brooks-lint). That is sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question
the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `Aegis` (already CATALOG'd, itself framed as a "Superpowers upgrade")
and the `superpowers`/GSD lineage already in STACK. Aegis already ships baseline-before-risky-
changes and evidence-before-completion discipline as portable method-pack skills; old-coder's
"run the gauntlet instead of reading code" pitch is the same evidence-first idea with no
differentiated mechanism disclosed. `superpowers` (GSD's underlying plugin) is already the
STACK's agent-harness/TDD-discipline pick, so a second thin skill for the same job earns nothing.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
