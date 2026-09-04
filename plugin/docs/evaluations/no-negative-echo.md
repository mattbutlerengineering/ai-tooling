# Evaluation: no-negative-echo

**Repo:** [LB623/no-negative-echo](https://github.com/LB623/no-negative-echo)
**Stars:** 583 | **Last updated:** 2026-08-26 (pushed) | **License:** MIT
**Last verified:** 2026-08-28
**Last triaged:** 2026-08-28  <!-- triaged: bulk -->
**Dev loop stage:** Ship
**Layer:** Tooling

---

## What it does

An Agent Skills-format skill that makes the agent regenerate delivery text — commit messages, PR titles and descriptions, code comments, doc openings — from the final adopted, verified state rather than the conversation, then checks multiple delivery surfaces for residue of rejected approaches (the "tomato-egg (no pork)" problem). Python 3.10+, tested, Codex-first but agent-portable.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata, README, plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition below, which turns on catalog placement and redundancy questions, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Cites `commit-commands` (a SKIP row) and `procoder` — neither is a STACK pick, so this lands in the P3 backlog band. Left at `discovery-log`: the problem it names (rejected-approach residue in final deliverables) is real and distinct from commit-message generation, and ★583 within a month of creation suggests it deserves a real eval when the queue reaches it.

_Triaged 2026-08-28 by the P3 backlog band._
