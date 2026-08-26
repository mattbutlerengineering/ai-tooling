# Evaluation: review-skills

**Repo:** [amElnagdy/review-skills](https://github.com/amElnagdy/review-skills)
**Stars:** 49 | **Last updated:** 2026-08-26 (pushed) | **License:** MIT
**Last verified:** 2026-08-26
**Last triaged:** 2026-08-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

Two-model debate review of PRs and MRs, plus a "babysitter" skill that works the
review rounds to resolution. Skills for any coding agent, not Claude Code-specific.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Genuinely overlaps `hubo` (already SKIPped here as redundant with adversarial-review
incumbents) on the core mechanic — two agents disputing one review — but adds a
babysitter that drives the rounds to closure, which `hubo`'s eval doesn't claim. Too
new (5 days old) and too close to an already-SKIPped tool to leave un-examined without
comment, but not clearly dominated either given the babysitter addition. Left at
`discovery-log`; a real eval should explicitly compare it against `hubo` and
`claude-octopus` before any disposition.
