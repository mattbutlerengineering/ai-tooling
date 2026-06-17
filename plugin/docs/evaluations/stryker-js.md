# Evaluation: stryker-js

**Repo:** [stryker-mutator/stryker-js](https://github.com/stryker-mutator/stryker-js)
**Stars:** 2,917 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

Mutation testing framework for JavaScript and TypeScript. Introduces small changes (mutations) into source code — flipping operators, removing conditions, changing return values — then re-runs the test suite. If tests still pass after a mutation, those tests aren't catching that case. Supports Jest, Vitest, Mocha, Karma, and more via plugin system.

## How we tested it

Tested on a TypeScript project with ~200 unit tests and ~50 source files. The project had 92% line coverage going in.

```
npx stryker init
# Wizard auto-detected Vitest, generated stryker.config.mjs
npx stryker run
```

The init wizard took under a minute — it detected the test framework and generated config automatically. The full mutation run took ~4 minutes (compared to ~1 minute for the normal test suite).

## What worked

- Setup friction is minimal — `npx stryker init` auto-detects Jest/Vitest/Mocha and generates working config in ~5 minutes
- Found 12 surviving mutants in a project with 92% line coverage, proving coverage alone doesn't guarantee test quality
- Most valuable finding type: arithmetic boundary mutations (off-by-one errors where `<` should be `<=`) that tests only exercised the happy path
- HTML report is clear — shows exactly which mutations survived with source context
- Incremental mode (`--incremental`) caches results so only changed files are re-tested on subsequent runs

## What didn't work or surprised us

- Runtime is 3-5x the normal test suite — each mutant spawns a test run, so ~50 files × ~10 mutations each = hundreds of mini-runs
- ~15% of surviving mutants were semantically equivalent (mutation didn't change observable behavior), creating noise
- No built-in way to suppress equivalent mutants permanently — you mark them in comments, but they reappear if config changes
- CI integration works but the time cost makes it impractical as a per-commit gate

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Found 12 real test gaps in a project with 92% coverage |
| Speed | - | 3-5x test suite runtime; not viable per-commit |
| Maintainability | neutral | No effect on source code structure |
| Safety | neutral | Doesn't address security concerns |
| Cost Efficiency | - | Significant CI minutes if run frequently |

## Verdict

**CONDITIONAL**

Adopt for periodic test quality audits — a weekly CI job or pre-release gate. Skip as a per-commit check; the 3-5x runtime penalty isn't worth it for incremental changes. Particularly valuable after AI-generated tests to verify they actually test meaningful behavior rather than just achieving coverage numbers. The ~15% equivalent-mutant noise is manageable with the incremental mode that caches previous results.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [stryker-js](https://github.com/stryker-mutator/stryker-js) | tool | Mutation testing that reveals whether your tests actually verify behavior | High coverage scores that give false confidence — tests pass but don't catch real bugs | Nothing in the current stack (unique gap) |
