# Evaluation: ratchet

**Repo:** [0xwilliamortiz/ratchet](https://github.com/0xwilliamortiz/ratchet)
**Stars:** 404 | **Last updated:** 2026-07-31 (pushed) | **License:** MIT
**Last verified:** 2026-08-01
**Last triaged:** 2026-08-01  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A hooks-based checker for Claude Code that verifies whether an agent actually
followed your project's stated rules over a session, rather than trusting the
agent's own claim that it did.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Overlaps `tdd-guard`, `vet`, and `brooks-lint`, but those are narrower (TDD
discipline, intent/correctness verification, book-grounded design review) — none
mechanically check general rule-following the way ratchet claims to. Fast-growing
(404 stars in two days) and MIT. Left at `discovery-log` for a real hands-on eval
rather than a mechanical SKIP.

_Triaged 2026-08-01 by the daily discovery routine (today's lead)._
