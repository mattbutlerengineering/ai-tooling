# Evaluation: driving-seat

**Repo:** [Tanmay-Ts/driving-seat](https://github.com/Tanmay-Ts/driving-seat)
**Stars:** 10 | **Last updated:** 2026-10-20 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement (keeps a human owning decisions an agent would otherwise make silently mid-build)
**Layer:** Process

---

## What it does

A Claude Code skill that turns a vague goal into a measurable intent before building,
then surfaces the decisions Claude would otherwise fill in silently (a retry policy,
an error-handling choice, a dependency nobody approved) for explicit human sign-off,
while leaving everything else auditable rather than gated.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as P3 backlog (no overlap-pressure citation from another row).
It sits beside `be-ambitious-harness` (independent verifier blind to the worker's
reasoning) in Agent Harnesses, but the mechanism differs — a measurable-intent gate
plus a decision log, not a cheap-check/verify pair — so there is no clear incumbent
to call this redundant against. Left at `discovery-log` for a real hands-on eval
rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [driving-seat](https://github.com/Tanmay-Ts/driving-seat) | skill | Claude Code skill (MIT) turning a vague goal into a measurable intent, then surfacing the decisions Claude would otherwise make silently for human sign-off | Agents fill gaps (retry policy, error handling, dependency choice) silently in production with no human decision log | be-ambitious-harness, proof-of-done-loop, verification-before-completion |
