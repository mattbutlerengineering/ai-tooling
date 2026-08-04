# Evaluation: qodo-cover

**Repo:** [qodo-ai/qodo-cover](https://github.com/qodo-ai/qodo-cover)
**Stars:** 5,548 | **Last updated:** 2026-04-05 (pushed) | **License:** AGPL-3.0
**Dev loop stage:** Verify (test generation)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Iteratively writes tests, runs them, and keeps only those that pass and raise coverage toward a
target.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`stryker-js`, `pr-agent`). Enough to place it;
not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. The catalog row already records the right relationship — qodo-cover
*writes* tests, `stryker-js` grades whether existing tests are any good — so the overlap is
complementary and disposing it as redundant would repeat the category error this lane keeps
catching.

The interesting property is the loop: generate, run, keep only what passes and raises coverage. That
is a mechanical oracle, which makes it one of the few tools here whose value claim is directly
measurable under `evaluations/measurement-protocols.md` — coverage delta on a disclosed repo, with
and without. It is a good P0 candidate for exactly that reason.

Two things to weigh when someone runs it. Pushed 2026-04-05, four months quiet, which is long for a
tool in an area moving this fast. And coverage-maximizing generation has a well-known failure mode —
tests that execute lines without asserting anything meaningful — so the measurement worth taking is
mutation score after generation, not the coverage number the tool optimizes.

AGPL-3.0 does not dispose it: this is a `tool` you run, not a vendored skill whose text enters your
repo.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [qodo-cover](https://github.com/qodo-ai/qodo-cover) | tool | AI-powered automated test generation (AGPL-3.0, ★5K, by Qodo) — iteratively writes tests, runs them, and keeps only those that pass and raise coverage toward a target | Writing thorough tests by hand is slow; want an agent that generates passing, coverage-increasing tests automatically | stryker-js (complementary: qodo-cover writes tests, stryker tests their quality), pr-agent |
