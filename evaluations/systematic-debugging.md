# Evaluation: systematic-debugging

**Repo:** [obra/superpowers](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging)
**Stars:** 294,366 (the container, `obra/superpowers`; the skill has no count of its own) | **Last updated:** 2026-09-27 | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Verify (debug)
**Layer:** Process

---

## What it does

Superpowers' debugging discipline: no fix until a root cause is found. It is one skill inside `obra/superpowers` (`skills/systematic-debugging/`). skills.sh listed **280K installs** on 2026-10-02.

The Iron Law is `NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST`, enforced through four phases:

1. **Root cause investigation:** read the errors, reproduce consistently, check recent changes, trace data flow.
2. **Pattern analysis:** find working examples and diff against the reference.
3. **Hypothesis and testing:** "Form Single Hypothesis", test it minimally.
4. **Implementation:** failing test first, one fix. **"If 3+ fixes failed: question architecture"** and stop patching.

A Red Flags list and a Common Rationalizations table try to catch the agent in the middle of a shortcut. A "no root cause" exit makes you document what you investigated, and warns that "95% of 'no root cause' cases are incomplete investigation". The folder is larger than the SKILL.md:

- Three technique references: `root-cause-tracing.md` (walk backward up the call stack), `defense-in-depth.md` and `condition-based-waiting.md`, with a `.ts` example.
- `find-polluter.sh`, a bisection script that finds which test leaves unwanted files or state behind.
- `CREATION-LOG.md` and three `test-pressure-*.md` scenarios, kept as the skill's own pressure tests.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read `SKILL.md`, `CREATION-LOG.md` and the head of `find-polluter.sh` through the GitHub API, listed the folder, and compared it against the existing [diagnosing-bugs.md](diagnosing-bugs.md) eval. That eval already holds the detailed head-to-head, made against the installed superpowers 6.0.3 copy of this skill. I did not use it on a live bug, and none of the pressure-test scenarios were replayed.

```bash
gh api repos/obra/superpowers --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/obra/superpowers/contents/skills/systematic-debugging --jq '.[].path'
gh api repos/obra/superpowers/contents/skills/systematic-debugging/SKILL.md --jq .content | base64 -d
gh api repos/obra/superpowers/contents/skills/systematic-debugging/CREATION-LOG.md --jq .content | base64 -d
gh api repos/obra/superpowers/contents/skills/systematic-debugging/find-polluter.sh --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **Root-cause tracing is its real edge.** `root-cause-tracing.md` (walk back up the call stack to where the bad value started) plus Phase 2's "find a working example and diff it" are things [diagnosing-bugs](diagnosing-bugs.md) lacks. That eval says so directly: diagnosing-bugs is "thinner on 'where does the bad value originate'".
- **The 3-failed-fixes rule.** Treating repeated failed patches as a sign of an architecture problem is the right stop condition for an agent, which will otherwise keep patching forever.
- **It is tuned to catch rationalizing.** The Red Flags list, the "your human partner's signals you're doing it wrong" section and the rationalization table target what agents actually say when cutting corners. The skill ships its own pressure-test scenarios, an unusual degree of self-testing for a skill.
- **`find-polluter.sh`** is a concrete tool for one specific, painful class of bug: a test that leaks state into other tests.

## What didn't work or surprised us

- **Single-hypothesis anchoring.** "Form Single Hypothesis" is the one point where diagnosing-bugs (3–5 ranked, falsifiable hypotheses) is methodologically better. The diagnosing-bugs eval reaches the same conclusion.
- **It gates on understanding, not on an artifact.** "Reproduce consistently" is an instruction, not a deliverable. diagnosing-bugs' "no red-capable command, no Phase 2" is easier to check because it requires a pasted command and its output.
- **No cleanup phase.** Nothing tells the agent to tag or remove debug instrumentation afterwards, which is the failure mode diagnosing-bugs' `[DEBUG-xxxx]` convention addresses.
- **Two packs, one trigger.** A user running both `obra/superpowers` and `mattpocock/skills` (both settled ADOPT) gets two debugging playbooks on "debug this" with no rule for which one wins. That is a stack-composition question, not a property of either skill.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Root-cause-first, pattern diffing and test-before-fix all reduce symptom patches |
| Speed | + | The 3-failed-fixes stop rule ends patch loops early; the up-front investigation costs time on easy bugs |
| Maintainability | + | Fixes land at the source with a regression test, and defense-in-depth adds validation where it belongs |
| Safety | neutral | Process skill; `find-polluter.sh` runs your own tests, nothing else |
| Cost Efficiency | + | Fewer wrong-fix turns; larger reference set loaded on demand |
| Verifiability | neutral | Phases are checkable in a transcript, but the gate is "understood the cause", a judgement rather than an artifact |

## Verdict

**SKIP** — ships inside `obra/superpowers`. Installing the container settles it, since it is a component of that artifact and not a competitor to it.

The review above is kept as color. The real question about this skill is the head-to-head with diagnosing-bugs (`mattpocock/skills`), and [diagnosing-bugs.md](diagnosing-bugs.md) already covers it: about 70% overlap, with systematic-debugging stronger on root-cause tracing and escalation, and diagnosing-bugs stronger on loop-first artifacts, multiple hypotheses and cleanup. That is a choice between two settled containers, and only a measured A/B on real bugs could settle it. It does not need its own lead.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [systematic-debugging](https://github.com/obra/superpowers/tree/main/skills/systematic-debugging) | skill | Four-phase root-cause-first debugging discipline with call-stack tracing and a 3-failed-fixes stop | Agents patch symptoms and stack fixes without finding where the bad value originates | diagnosing-bugs |
