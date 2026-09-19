# Evaluation: i-dont-believe-you

**Repo:** [LeonardLeroy/i-dont-believe-you](https://github.com/LeonardLeroy/i-dont-believe-you)
**Stars:** 16 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A coding-agent skill running eight automated checks against a code diff before the agent is
allowed to claim that tests pass or the work is done — stopping the agent from asserting success
the diff doesn't actually back up.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (vet, prove-it, old-coder). That is sufficient to place the
lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: overlaps `vet`, `prove-it`, and `old-coder` (all evidence-first
verification skills), but none is a STACK incumbent and each uses a different mechanism (vet =
standalone verifier/CI, prove-it = adversarial proof skill, old-coder = "run the gauntlet"). A
fifth entrant in a crowded but unvalidated cluster — worth a first-time look, not a mechanical
SKIP, since no single incumbent dominates this specific "8 automated checks gate the claim"
mechanism.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
