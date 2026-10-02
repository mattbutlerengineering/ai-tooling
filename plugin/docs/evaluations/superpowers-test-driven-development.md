# Evaluation: superpowers:test-driven-development

**Repo:** [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/test-driven-development)
**Stars:** 294,366 (the container, `obra/superpowers`; the skill has no count of its own) | **Last updated:** 2026-09-27 | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Implement / Verify
**Layer:** Process

---

## What it does

Superpowers' strict red-green-refactor skill. Its Iron Law is `NO PRODUCTION CODE WITHOUT A FAILING TEST FIRST`, and code written before its test gets deleted. It is one skill inside `obra/superpowers` (`skills/test-driven-development/SKILL.md` plus `writing-good-tests.md`). skills.sh listed **243K installs** on 2026-10-02.

The cycle is a dot graph with two mandatory gates:

- **Verify RED:** the test must *fail, not error*, for the expected reason.
- **Verify GREEN:** the test passes *and the output is clean*. "Other tests" means the project's full suite, and a failure you saw and didn't report is "a report falsified by omission".

Beyond that, the skill says code written before its test must be deleted outright ("Don't keep it as reference… Delete means delete"). It carries an 11-row rationalization table, a red-flags list ending in "Delete code. Start over", and a verification checklist. The `writing-good-tests.md` reference adds two principles, *name the break* (state which production change should make the test fail) and *exercise the real thing* (mocks only at slow or external boundaries), plus a **mutation check**: mentally mutate the code, and some test should fail for each realistic mutation.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read both files through the GitHub API and compared them line by line against `addyosmani/agent-skills`' `test-driven-development` ([agent-skills-test-driven-development.md](agent-skills-test-driven-development.md)) and the hook-enforced [tdd-guard](tdd-guard.md). mattpocock's `tdd` is being measured separately and is not compared here. No feature was built with the skill loaded.

```bash
gh api repos/obra/superpowers --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/obra/superpowers/contents/skills/test-driven-development --jq '.[].path'
gh api repos/obra/superpowers/contents/skills/test-driven-development/SKILL.md --jq .content | base64 -d
gh api repos/obra/superpowers/contents/skills/test-driven-development/writing-good-tests.md --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **"Verify RED" demands a failure for the right reason**, not just a red result: "fails (not errors)", "fails because feature missing (not typos)". That separates a real red from a broken import, which both TDD skills here need and only this one spells out.
- **The best test-quality guidance of the three.** Name-the-break, independently derived expectations ("an expectation computed by the code under test… passes no matter what") and the mutation check go after *tautological tests*, the typical failure of agent-written tests. agent-skills' version has nothing as sharp.
- **The full-suite clause has teeth.** "A scope statement in your task bounds the deliverable, not your verification", plus the duty to report red tests you didn't cause, closes the "I only ran my file" loophole.
- **Pressure-resistant phrasing.** Like the rest of superpowers, it is written to hold up against an agent's "just this once".

## What didn't work or surprised us

- **Delete-means-delete is costly and not enforced.** Telling an agent to throw away working code it wrote first is the right ideology and an expensive habit. As prose it relies on compliance. [tdd-guard](tdd-guard.md) enforces the same rule mechanically with a hook, which is a different and stronger guarantee.
- **Assumes `npm test`.** Every example command is `npm test`. agent-skills' version opens with "Discover the Stack First" and lists "reaching for a default test command" as a red flag. This one doesn't do that.
- **No test-sizing guidance.** It says nothing about unit vs integration vs E2E or how to choose between them. agent-skills covers that with a pyramid and a size/resource model.
- **Very broad trigger.** The description is "when implementing any feature or bugfix", so in a stack with another TDD skill both fire on nearly every coding prompt.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Verify-RED-for-the-right-reason + mutation check target tests that cannot fail |
| Speed | - | The strict cycle, plus deleting pre-written code, adds turns, especially on exploratory work |
| Maintainability | + | Real-code-over-mocks and name-the-break produce fewer, more meaningful tests |
| Safety | neutral | Process skill; no new permissions or surface |
| Cost Efficiency | neutral | More turns per feature, offset by fewer wrong-implementation reworks; not measured |
| Verifiability | + | Each step leaves transcript evidence (a red run with its message, a green full-suite run) a reviewer can check |

## Verdict

**SKIP** — ships inside `obra/superpowers`. Installing the container settles it, since it is a component of that artifact and not a competitor to it.

The review above is kept as color. Of the TDD skills reviewed here, this is the strictest and has the best test-quality reference (`writing-good-tests.md`). It is weaker than agent-skills' version on discovering which test command to use and on test sizing. Because both containers are settled ADOPT, running both packs puts two TDD skills on the same trigger. That is a stack-composition decision, not a reason to queue this as its own lead.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [superpowers:test-driven-development](https://github.com/obra/superpowers/tree/main/skills/test-driven-development) | skill | Strict red-green-refactor: no production code without a watched-failing test; delete code written first | Agents write code first and bolt on tests that pass immediately and prove nothing | agent-skills:test-driven-development, tdd, tdd-guard |
