# Evaluation: abide

**Repo:** [coldteadotai/abide](https://github.com/coldteadotai/abide)
**Stars:** 108 | **Last updated:** 2026-09-18 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Checks every edit a coding agent makes against the project's own custom instructions (CLAUDE.md/AGENTS.md-style rules) using a decision model, catching violations mid-session and requesting an agent repair automatically rather than relying on the agent to remember and self-police its own rules.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (ratchet, tdd-guard, procoder). That is sufficient to place
the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: overlaps `ratchet` (gone/404) and `tdd-guard` (test-discipline only, not
general project-rule compliance) and `procoder` (commit-gate framing, not mid-edit checking) —
none is a direct, dominating incumbent for "check every edit against custom instructions."
Distinct enough mechanism (decision-model-graded compliance checking) to be worth a first-time
look rather than a mechanical SKIP.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
