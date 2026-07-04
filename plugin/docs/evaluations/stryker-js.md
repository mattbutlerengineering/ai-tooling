# Evaluation: stryker-js

**Repo:** [stryker-mutator/stryker-js](https://github.com/stryker-mutator/stryker-js)
**Stars:** 2,917 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

Mutation testing framework for JavaScript and TypeScript. Introduces small changes (mutations) into source code — flipping operators, removing conditions, changing return values — then re-runs the test suite. If tests still pass after a mutation, those tests aren't catching that case. Supports Jest, Vitest, Mocha, Karma, and more via plugin system.

## How we tested it

**Evidence:** RUN

Built a minimal project (`@stryker-mutator/core` + `@stryker-mutator/jest-runner`, Jest) with one deliberately **under-tested** function, to see whether Stryker catches gaps that line coverage misses. The function has four branches; the test suite only asserts two of them:

```js
// src/classify.js
function classify(n) {
  if (n < 0)   return 'negative';
  if (n === 0) return 'zero';
  if (n > 100) return 'large';
  return 'small';
}
// test/classify.test.js — only covers 'negative' and 'small'
test('negative', () => expect(classify(-5)).toBe('negative'));
test('small',    () => expect(classify(50)).toBe('small'));
```

```
npm i -D jest @stryker-mutator/core @stryker-mutator/jest-runner
npx jest          # 2 passed, 2 total — green
npx stryker run   # testRunner: jest, coverageAnalysis: perTest
```

The Jest suite passed green (2/2). Stryker then mutated the source and re-ran the tests per mutant. Final score: **64.71% mutation score — 11 killed, 4 survived, 2 no-coverage** out of 17 mutants.

## What worked

- **Caught exactly the gaps coverage hides.** The `if (n < 0)` boundary was mutated to `n <= 0` and **survived** — an off-by-one the green suite never tested. The `n === 0` and `n > 100` branches were mutated to `if (false)` and to `return ""`; those **survived or had no coverage**, proving the tests never actually verify the `zero` and `large` logic despite a passing run.
- **Output points straight at the weak test.** For each surviving mutant Stryker prints the exact line, the original-vs-mutated diff, and which tests ran — e.g. the `n > 100` mutant shows only `small` ran, so nothing exercised the large case.
- **Setup was genuinely low-friction** — install two packages, a 5-line `stryker.config.json` naming the `jest` runner, and `npx stryker run` worked first try.

## What didn't work or surprised us

- **Mutation score is not coverage and reads lower.** A suite that *feels* covered scored 64.71%; the two `[NoCoverage]` mutants (string-literal mutations in untested branches) drag the number down separately from the four `[Survived]` ones. You have to read both buckets to know whether the gap is "no test reaches this" vs "a test reaches it but doesn't assert enough."
- **Cost is structural, not incidental.** Stryker runs the test suite (or a coverage-filtered subset) once *per mutant* — here 17 mutants on one tiny file. On a real codebase that is hundreds-to-thousands of suite executions, which is why it belongs in a periodic job, not a per-commit gate. (This tiny run finished in seconds; the penalty only bites at scale.)

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Surfaced 4 surviving + 2 no-coverage mutants (incl. a `<`→`<=` boundary) in a suite that passed green. |
| Speed | - | One test run per mutant; structural N× cost that makes it impractical per-commit at scale. |
| Maintainability | neutral | No effect on source code structure. |
| Safety | neutral | Doesn't address security concerns. |
| Cost Efficiency | - | Significant CI minutes if run frequently; best as a periodic audit. |

## Verdict

**CONDITIONAL**

Verified hands-on: on a green-passing Jest suite, Stryker correctly exposed untested branches and an off-by-one boundary that line coverage rated as fine (64.71% mutation score, 4 survived + 2 no-coverage of 17). Adopt for periodic test-quality audits — a weekly CI job or pre-release gate — and especially right after AI-generated tests, which often hit coverage targets without asserting behavior. Skip it as a per-commit check: the per-mutant re-run cost is structural and doesn't scale to incremental changes.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stryker-js](https://github.com/stryker-mutator/stryker-js) | tool | Mutation testing that reveals whether your tests actually verify behavior | High coverage scores that give false confidence — tests pass but don't catch real bugs | Nothing in the current stack (unique gap) |
