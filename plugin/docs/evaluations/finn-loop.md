# Evaluation: Finn-loop

**Repo:** [finna/Finn-loop](https://github.com/finna/Finn-loop)
**Stars:** 236 | **Last updated:** 2026-07-23 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling (Claude Code skill bundle)

---

## What it does

A 3-skill "AI software factory" for Claude Code — spec, build, review, with humans merging the
result. Surfaced in the 2026-07-29 daily discovery scan (topic `claude-code`, created 2026-07-22).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy
with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers
directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `GSD` (KEEP, already in STACK.md). GSD already provides a structured
Discuss→Plan→Execute→Verify→Ship loop with durable state for Claude Code, with a much larger
install base and a MEASURED verdict. Finn-loop's spec→build→review loop covers the same job one
week old and unvalidated; a second tool for this job earns nothing over the incumbent.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
