# Evaluation: repro-lens

**Repo:** [00200200/repro-lens](https://github.com/00200200/repro-lens)
**Stars:** 38 | **Last updated:** 2026-09-13 (pushed) | **License:** MIT
**Last verified:** 2026-09-13
**Last triaged:** 2026-09-13  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Checks ML/data-science changes made by coding agents: randomness/seed checks,
experiment replay, and before/after output comparison — a reproducibility gate
rather than a general test-quality one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to weigh the
P2 redundancy question below; it would not support an ADOPT, and this eval offers
none.

## Triage note

`triage.py` bands this P2 (challenges `stryker-js`, a STACK pick) because
`stryker-js` sits in the Overlaps cell — but the two do different jobs.
`stryker-js` mutates *code* to check whether a JS/TS test suite catches injected
bugs; `repro-lens` checks whether an agent's change to *ML/data-science code*
(models, notebooks, pipelines) still reproduces the same experiment output —
randomness control and before/after diffing, not mutation testing, and not
JS/TS-specific. Not redundant; a `SKIP "redundant with stryker-js"` would misstate
what either tool does. Left at `discovery-log` — differentiated niche (ML
reproducibility for agent-made changes), no existing catalog entry covers it,
deserves a real eval.

## Verdict

**discovery-log — tentative read** — a reproducibility checker for agent-made ML
changes, a niche `stryker-js` and `agent-delivery-gates` don't cover; not evaluated
hands-on.
