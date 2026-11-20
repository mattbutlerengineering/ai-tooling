# Evaluation: testscope

**Repo:** [Ar9av/testscope](https://github.com/Ar9av/testscope)
**Stars:** 12 | **Last updated:** 2026-11-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A pytest plugin that runs only the tests a change can affect — impact-scoped test
selection for AI coding agents and CI, so an agent (or a CI run) doesn't burn turns
and wall-clock time re-running the whole suite on every small diff.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Cites `stryker-js` in its "Overlaps with" cell, which bands this P2 challenger —
but `stryker-js` is mutation testing (checks whether your *tests* are good),
while `testscope` is test *selection* (picks which tests to *run* for a given
change). Those are complementary jobs, not competing ones: a team could run
`testscope` on every commit to cut CI time and still run `stryker-js`
periodically to grade test quality. Installing the STACK's `stryker-js` pick does
not settle this lead, so SKIPping it as "redundant" would be the false-SKIP the
P2 band's guardrail warns against. Left at `discovery-log` — a real hands-on
comparison against the existing test-quality/CI-efficiency cluster would need a
first-time eval, not a mechanical SKIP.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [testscope](https://github.com/Ar9av/testscope) | tool | pytest plugin (Apache-2.0) running only the tests your change can affect, for AI coding agents and CI | Full test suites waste agent and CI time running tests a change couldn't possibly break; want impact-scoped test selection instead | stryker-js, farol, code-quality |
