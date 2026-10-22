# Evaluation: be-ambitious-harness

**Repo:** [alexpiar/be-ambitious-harness](https://github.com/alexpiar/be-ambitious-harness)
**Stars:** 22 | **Last updated:** 2026-10-21 (pushed) | **License:** MIT
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A Claude Code skill (plain markdown, EN + RU) that sets two bars per task — a cheap
gate check before expensive work is attempted, then an independent verifier that never
sees the worker's own reasoning, aimed at making agents aim higher without losing
control.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Brand new (created 2026-10-20). Differentiator over `proof-of-done-loop` and
`verification-before-completion` is the paired cheap-gate-then-blind-verifier structure
specifically aimed at calibrating task ambition, not just completion evidence. No
archived flag, no disqualifying license, no `Ships inside` container, zero overlap
pressure. Left at `discovery-log` for a real hands-on eval rather than SKIPped.

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [be-ambitious-harness](https://github.com/alexpiar/be-ambitious-harness) | skill | Claude Code skill (MIT) setting two bars per task — a cheap gate check before expensive work, then an independent verifier blind to the worker's own reasoning | Agents either under-aim on a task framed as easy or burn budget with no cheap pre-check, and self-graded completion has no independent verifier | proof-of-done-loop, verification-before-completion, Aegis |
