# Evaluation: ratchet

**Repo:** [0xwilliamortiz/ratchet](https://github.com/0xwilliamortiz/ratchet)
**Stars:** 409 | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** Code Review & Quality
**Layer:** Tooling

---

## What it does

A git-hook compliance monitor for coding agents: intercepts agent edits via a `PostToolUse` hook and grades findings (certain/likely/heuristic) against complexity, duplication, and new-dependency rules, maintaining a session ledger of complexity trends. Blocks edits in strict mode or advises in guard mode (default).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: README, install instructions, and test-suite description gathered via web fetch (115 passing tests reported by the project, not independently re-run here).

## Triage note

Left at `discovery-log` rather than SKIPped: `tdd-guard` enforces test-first discipline and `cc-safety-net` blocks destructive commands, but neither grades mid-session complexity/duplication/dependency drift the way this tool claims to. The differentiation (a graded, ledger-tracked complexity monitor rather than a binary test/safety gate) is worth a real hands-on eval.

_Triaged 2026-08-02 by the daily discovery routine (today's new lead)._
