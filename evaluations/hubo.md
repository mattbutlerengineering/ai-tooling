# Evaluation: hubo

**Repo:** [h0ngcha0/hubo](https://github.com/h0ngcha0/hubo)
**Stars:** 25 | **Last updated:** 2026-07-29 (pushed) | **License:** MIT
**Last verified:** 2026-07-30
**Last triaged:** 2026-07-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process (skill)

---

## What it does

Two agents spar over one codebase until every review finding is reconciled — an adversarial
multi-agent code review loop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (code-review, claude-octopus, vet). That is sufficient for a
SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a
question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `code-review` (STACK, MEASURED — 4-agent parallel PR review with
confidence scoring) and `claude-octopus` (multi-LLM consensus review with a 75% gate). Both
already give multi-agent/multi-model review reconciliation; hubo's "two agents spar until
reconciled" is a narrower version of the same job with a small (25-star) unproven implementation.
The STACK already covers this job.

_Triaged 2026-07-30 as part of a new discovery-log intake, not a P1/P2/P3 bulk-band pass._
