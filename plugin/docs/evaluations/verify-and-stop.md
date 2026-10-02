# Evaluation: verify-and-stop

**Repo:** [JuliusBrussee/caveman](https://github.com/JuliusBrussee/caveman/tree/main/skills/verify-and-stop)
**Stars:** 108,996 (the container, `JuliusBrussee/caveman`; the skill has no count of its own) | **Last updated:** 2026-10-01 | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Dev loop stage:** Verify
**Layer:** Process

---

## What it does

Proves that existing work meets its acceptance conditions *without expanding scope*, then stops. It is one skill inside `JuliusBrussee/caveman` (`skills/verify-and-stop/SKILL.md` plus an `agents/openai.yaml` that sets a Codex display name and the default prompt "Use $verify-and-stop to prove acceptance criteria without adding scope."). skills.sh listed **80K installs** on 2026-10-02.

The whole skill is about ten lines of body. It turns the acceptance conditions into the **smallest set of checks that proves them**:

- Reuse results that are still current for the same repository state.
- Run focused checks before wider gates.
- Report each result as exactly one of **pass, fail, unavailable or blocked**.
- Don't edit product code unless the request includes fixes.
- Don't add polish, cleanup or unrelated tests after the criteria pass.
- "Stop immediately when acceptance proof is complete. Report commands, results, and unresolved risk only."

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read both files through the GitHub API and compared them with the container's measured eval ([caveman.md](caveman.md)) and, conceptually, with superpowers' `verification-before-completion`. That skill is being measured separately and isn't reviewed here. The whole text is in front of us, so the analysis below is of all of it.

```bash
gh api repos/JuliusBrussee/caveman --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/JuliusBrussee/caveman/contents/skills/verify-and-stop --jq '.[].path'
gh api repos/JuliusBrussee/caveman/contents/skills/verify-and-stop/SKILL.md --jq .content | base64 -d
gh api repos/JuliusBrussee/caveman/contents/skills/verify-and-stop/agents/openai.yaml --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **A four-way result vocabulary.** "pass, fail, unavailable, blocked" is the most useful line in the skill. It stops an agent from rounding "couldn't run the check" up to "pass", the same distinction this repo's own detectors draw between `UNCHECKED` and `BROKEN` (#319, #447).
- **It works against over-verification.** "Smallest sufficient proof set", "reuse still-current results" and "stop immediately" target agents that keep polishing, re-testing and refactoring after the job is done. `verification-before-completion` pushes the other way, against claiming success *without* evidence. The two are complementary halves rather than rivals.
- **Very cheap.** About ten lines, in caveman's terse register, costs almost nothing to load, which fits the container's token-efficiency purpose.

## What didn't work or surprised us

- **It assumes the acceptance conditions exist.** It turns criteria into checks but has no step for when the criteria are vague or missing. In that case "smallest sufficient proof" turns into whatever the agent decides counts.
- **"Reuse still-current results" depends on judgement.** "Matching repository state" isn't defined: same commit, same working tree, same lockfile? A stale green result reused after an edit is exactly the false pass this skill should prevent.
- **No evidence format.** "Report commands, results" is the whole reporting rule. It doesn't require the output to be pasted, so a reviewer may only get the agent's summary of a run rather than the run itself.
- **A narrow trigger by design.** It fires for "validation-only tasks". On a normal implement-then-finish task it may never fire, which is the moment over-claiming actually happens.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Distinguishing unavailable/blocked from pass removes a common false-success path |
| Speed | + | Focused-first checks and an explicit stop cut post-completion churn |
| Maintainability | + | Forbids unrequested cleanup and extra tests, keeping verification diffs out of product code |
| Safety | neutral | Process skill; no new surface |
| Cost Efficiency | + | ~10-line body; stops agents spending turns after acceptance is proven |
| Verifiability | + | Reports commands, results and remaining risk, though it doesn't require pasting raw output |

## Verdict

**SKIP** — ships inside `JuliusBrussee/caveman`. Installing the container settles it, since it is a component of that artifact and not a competitor to it.

The review above is kept as color. It is a small, well-aimed skill that limits scope (stop once proof is complete) and states each result's status precisely. It complements rather than duplicates superpowers' `verification-before-completion`, which guards against claiming without proof, while this one guards against continuing after proof. Whether the two compose cleanly in one stack is a question for that skill's measured eval, not a reason to queue this one separately.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [verify-and-stop](https://github.com/JuliusBrussee/caveman/tree/main/skills/verify-and-stop) | skill | Proves acceptance criteria with the smallest sufficient check set, then stops without adding scope | Agents over-verify, polish and expand scope after the work is already proven done | verification-before-completion |
