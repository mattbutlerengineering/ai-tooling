# Evaluation: winnow

**Repo:** [GhalebDweikat/winnow](https://github.com/GhalebDweikat/winnow)
**Stars:** 11 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A calibrated context sieve for Claude Code — every tool result is judged by a fast ("System One")
model before it is admitted into context, screening out irrelevant content proactively rather than
compressing it after the fact.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (headroom, context-mode, lean-ctx). That is sufficient to
place the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Verdict

**SKIP** — redundant with `headroom` (STACK, Tier 1, `MEASURED`). headroom already compresses
tool outputs, logs, and files before they reach the LLM (60-95% fewer tokens, reversibly via local
cache) — the same core problem (context bloat from verbose tool output) winnow addresses. winnow's
judge-before-admit mechanism differs from headroom's compress-after-the-fact approach, but at 11
stars and two days old with no measured comparison against the validated incumbent, that mechanism
difference is not itself a reason to carry a second unvalidated tool in an already-served niche.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
