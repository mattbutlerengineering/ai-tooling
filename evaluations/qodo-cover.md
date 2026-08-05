# Evaluation: qodo-cover

**Repo:** [qodo-ai/qodo-cover](https://github.com/qodo-ai/qodo-cover)
**Stars:** 5,548 | **Last updated:** 2026-04-05 (pushed) | **License:** AGPL-3.0
**Dev loop stage:** Verify (test generation)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->

---

## What it does

Iteratively writes tests, runs them, and keeps only those that pass and raise coverage toward a
target.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`stryker-js`, `pr-agent`). Enough to place it;
not enough for a positive verdict, and none is offered.

## Verdict

**SKIP — discontinued upstream, and the maintainer explicitly declines to name a successor.**

Read live on 2026-08-05, the README opens with:

> **⚠️ This repository is no longer maintained. Please fork it if you wish to continue development
> or use it in your own projects.**

That is repo-level and unambiguous, and "fork it" is the maintainer saying there is no successor —
which is the one thing P1's successor-check exists to establish before disposing an unmaintained
project. Pushed 2026-04-05; `archived` is still `false`, which is exactly why nothing caught this
until detector V (#351) started reading README banners.

**This eval's previous triage note is superseded, and how it failed is the point.** That pass ran on
2026-08-04, noted *"pushed 2026-04-05, four months quiet, which is long for a tool in an area moving
this fast"*, and still left the lead — because dormancy is not discontinuation and the lane was
right not to dispose on age alone. It looked directly at the only signal available and could not
tell. The banner was the missing fact, not the judgement.

What the SKIP costs is worth naming: that note argued qodo-cover was one of the better **P0
measurement** candidates in the catalog, because generate → run → keep-only-what-passes is a
mechanical oracle and coverage delta is directly measurable under
`evaluations/measurement-protocols.md`. That remains true of the *technique*; it is no longer a
reason to spend a measured evaluation on this implementation. An unmaintained LLM-driven test
generator is the `plandex` case — it rots as model APIs turn over, and here there will be no
release to fix it.

The row stays as reference (the `Flowise` precedent). AGPL-3.0 was never the disposing factor: it
is a `tool` you run, not a vendored skill.

_Triaged 2026-08-05 by the detector-V maintenance sweep ([#360](https://github.com/mattbutlerengineering/ai-tooling/issues/360))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [qodo-cover](https://github.com/qodo-ai/qodo-cover) | tool | AI-powered automated test generation (AGPL-3.0, ★5K, by Qodo) — iteratively writes tests, runs them, and keeps only those that pass and raise coverage toward a target | Writing thorough tests by hand is slow; want an agent that generates passing, coverage-increasing tests automatically | stryker-js (complementary: qodo-cover writes tests, stryker tests their quality), pr-agent |
