# ADR-0004: Add Verifiability as a sixth quality signal

- **Status:** Accepted
- **Date:** 2026-08-03
- **Issue:** #307
- **Relates to:** [ADR-0003 (methodologies directory)](0003-methodologies-directory.md)

## Context

The repo scored every tool against five quality signals — Correctness, Speed,
Maintainability, Safety, Cost Efficiency ([WORKFLOW.md](../../WORKFLOW.md)) — and all five
ask a question about the *generated artifact*: is it right, is it fast, is it clean, is it
safe, was it cheap.

None asked whether a human can confirm the answer at the rate the artifact is produced.
Speed comes closest ("how fast from prompt to merged PR?") but treats review as **latency
to minimize**, not as a **capacity a tool can expand or consume**.

That gap changes verdicts. A tool that generates far more code at unchanged quality scores
well on Speed, neutral on the rest, and lands ADOPT — while transferring cost onto the one
resource the field's own retrospectives keep identifying as scarce. The repo could not see
the trade.

A survey of ~22 practitioner talks and methodology writeups on software factories and the
agentic SDLC (issue #307) found this to be the dominant convergent finding, reached
independently by speakers with no shared frame:

- Implementation collapsed from weeks to hours while requirements-gathering and validation
  did not, so specification quality becomes the binding constraint — which is why AI
  assistants can 10× an engineer's output without 10×ing the business's
  ([Cole Medin on Google's agentic-engineering material](https://www.youtube.com/watch?v=zbmuiaPuiNM)).
- The reviewer side of the same constraint: if every piece of generated code requires your
  review, you have made yourself the bottleneck
  ([Kun Chen, "L8 Principal's Agentic Engineering Workflow"](https://www.youtube.com/watch?v=iQyg-KypKAA)).
- Review is not one step but a loop of validate, fix, re-run — so "PR review is solved" is
  a category error
  ([Overcut, "From SDLC to ADLC"](https://www.youtube.com/watch?v=x61b6_lHWQw)).

## Decision

**Add `Verifiability` as a sixth quality signal**: *can a human confirm the output is
right, at the rate it's produced?* Example metrics: diff size per unit of reviewed intent,
share of claims machine-checkable, review round-trips before merge.

Consequences we accept:

1. **It is required for new evaluations, not retrofitted.** ~556 existing evals carry
   five-row signal tables. Backfilling all of them would be a mechanical diff across the
   entire back catalog with no new evidence behind any cell. New evals use the six-row
   table in [TEMPLATE.md](../../evaluations/TEMPLATE.md); old ones are upgraded
   opportunistically when otherwise revisited.
2. **No detector gates it.** No script parses the signal tables today, so adding a row is
   inert to `make check`. Gating signal-table shape is a separate decision, deferred until
   the six-row form has settled across enough new evals to be worth pinning.
3. **Speed and Verifiability may disagree, and that is the point.** When they do,
   Verifiability is the signal that predicts whether end-to-end cycle time actually
   improved. A tool earns its slot on the loop, not on the stage it visibly accelerates.

## Alternatives considered

**Widen the definition of Speed.** Rejected: it collapses two measurements that genuinely
diverge. A tool can shorten time-to-merge *by* degrading reviewability (larger diffs waved
through faster), and one number cannot express that as a trade-off.

**Fold it into Maintainability.** Rejected: Maintainability asks whether someone can work
with the code *later*. Verifiability asks whether anyone can check it *now*, before merge.
Different time horizon, different remedies — the first wants smaller files and less
abstraction, the second wants machine-checkable output and smaller reviewable units.

**Do nothing; treat it as an eval-author judgment call.** Rejected: it was already
available as a judgment call and no eval made it. An unnamed signal is not applied.
