# Evaluation: old-coder

**Repo:** [AmazingAng/old-coder](https://github.com/AmazingAng/old-coder)
**Stars:** 153 | **Last updated:** 2026-07-27 (pushed) | **License:** MIT
**Last verified:** 2026-07-29
**Last triaged:** 2026-07-29  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling (Claude Code skill)

---

## What it does

An "evidence-first" development skill for coding agents — don't trust code by reading it, make it
run the gauntlet (tests/checks) instead, inspired by Uncle Bob. Surfaced in the 2026-07-29 daily
discovery scan.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (`tdd-guard`, `vet`, `brooks-lint`). None of those three
incumbents is itself in STACK.md, so this lead doesn't turn on redundancy with an adopted tool —
it's a philosophy-level skill (habit/prompt) rather than `tdd-guard`'s mechanical hook or `vet`'s
independent verifier, and could plausibly earn a real hands-on eval on its own merits.

## Triage note

Left at `discovery-log`: distinct enough in mechanism (a skill nudging evidence-first habits,
not a hook or standalone verifier) from its named overlaps that a mechanical SKIP would be
premature. Candidate for a real eval in the P0/eval-runner lane if it keeps gaining traction.

_Triaged 2026-07-29 by the daily discovery scan's same-day triage pass._
