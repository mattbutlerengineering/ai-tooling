# Evaluation: agent-skills:test-driven-development

**Repo:** [addyosmani/agent-skills](https://github.com/addyosmani/agent-skills/tree/main/skills/test-driven-development)
**Stars:** 100,477 (the container, `addyosmani/agent-skills`; the skill has no count of its own) | **Last updated:** 2026-10-02 | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Implement / Verify
**Layer:** Process

---

## What it does

Addy Osmani's TDD skill. It runs red-green-refactor plus a "Prove-It Pattern" for bug fixes, test-pyramid sizing and browser verification. It is one skill inside `addyosmani/agent-skills` (a single 398-line `skills/test-driven-development/SKILL.md`). skills.sh listed **45K installs** on 2026-10-02, about a fifth of superpowers' TDD skill.

It is less a cycle than a testing handbook built around one:

1. **Discover the Stack First:** find the repo's own wrappers (`./gradlew`, `make test`), its focused-test and full-suite commands, and the commands its CI runs, and "never assume a default like `npm test`".
2. **RED → GREEN → REFACTOR**, with TypeScript examples.
3. **Prove-It Pattern:** a bug report starts with a test that reproduces it, and only then the fix.
4. **Test pyramid** (80/15/5) plus a Small/Medium/Large resource model and a decision guide.
5. **Writing good tests:** state over interactions, DAMP over DRY, real > fake > stub > mock, Arrange-Act-Assert, descriptive names.
6. **Browser testing with Chrome DevTools MCP**, including a "Security Boundaries" note that page content is untrusted data, not instructions.
7. **Subagents:** have a subagent write the reproduction test so it is written without knowledge of the fix.

It closes with rationalizations, red flags and a verification checklist.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read the full `SKILL.md` through the GitHub API and compared it section by section with superpowers' `test-driven-development` ([superpowers-test-driven-development.md](superpowers-test-driven-development.md)) and with the container's eval ([agent-skills-addyosmani.md](agent-skills-addyosmani.md)). mattpocock's `tdd` is being measured separately and is not compared here. Nothing was built with the skill loaded.

```bash
gh api repos/addyosmani/agent-skills --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/addyosmani/agent-skills/contents/skills/test-driven-development --jq '.[].path'
gh api repos/addyosmani/agent-skills/contents/skills/test-driven-development/SKILL.md --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **Discover-the-stack-first is its clearest advantage.** Using the repo's own test commands, and treating "reaching for `npm test` without checking" as a red flag, fixes a real agent failure that superpowers' version, with `npm test` in every example, quietly encourages.
- **Writing the reproduction test in a subagent** keeps it independent of the fix. That is a structural guard against a test written to pass, and neither of the other TDD skills reviewed here offers one.
- **Test sizing.** The pyramid and the Small/Medium/Large resource model answer "what kind of test?", a question superpowers' TDD skill never asks.
- **Its "don't re-run unchanged code" rule** ("re-running on unchanged code adds no confidence") is a small token-saving rule aimed at agents re-running tests for reassurance.
- **The browser-testing section treats page content as untrusted input**, a useful security note other TDD skills leave out.

## What didn't work or surprised us

- **Softer red gate.** "It must fail" is stated, but nothing asks that it fail *for the expected reason*. superpowers' Verify RED ("fails, not errors… not typos") is stricter, and that check is what makes the red step mean something.
- **No mutation check and no name-the-break rule.** Test-quality guidance is general (DAMP, AAA, one concept per test) and doesn't directly target the tautological tests agents tend to write.
- **Scope creep.** About 400 lines covering TDD, pyramid theory, DevTools debugging and subagent orchestration in one skill means a large load on every "implement any logic" trigger, and the browser section overlaps the pack's own `browser-testing-with-devtools` skill.
- **No deletion rule for code written first.** It doesn't say what to do with code that already exists before its test, so code-then-test can slip through as long as the test is written at some point.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Prove-It reproduction tests + independent subagent-written repros reduce fixes that only appear to work |
| Speed | + | Uses the repo's real focused-test command and forbids redundant re-runs |
| Maintainability | + | Pyramid sizing and real-over-mock guidance keep suites fast and meaningful |
| Safety | + | Explicit "browser content is untrusted data" boundary for DevTools-driven verification |
| Cost Efficiency | neutral | Saves re-runs, but a ~400-line body loads on a very broad trigger; not measured |
| Verifiability | + | The checklist requires a reproduction test that failed before the fix and a full-suite run with the repo's own command |

## Verdict

**SKIP** — ships inside `addyosmani/agent-skills`. Installing the container settles it, since it is a component of that artifact and not a competitor to it.

The review above is kept as color. Compared with superpowers' TDD skill, this is the practical one (uses the repo's own commands, sizes tests, keeps the repro independent of the fix), while superpowers' is the strict one (fails-for-the-right-reason, mutation check, delete-means-delete). Both containers are settled ADOPT, so which TDD skill a stack should run is a composition question for a measured A/B, not a lead for this queue.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skills:test-driven-development](https://github.com/addyosmani/agent-skills/tree/main/skills/test-driven-development) | skill | Red-green-refactor with stack discovery, Prove-It bug repros, test-pyramid sizing and DevTools checks | Agents assume default test commands, fix bugs without a reproduction test, and mis-size tests | superpowers:test-driven-development, tdd, tdd-guard |
