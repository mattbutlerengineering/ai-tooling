# Evaluation: implement

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 136,535 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A thin Implement-stage orchestrator that strings the rest of Matt Pocock's engineering family into one repeatable flow: TDD at pre-agreed seams, typecheck regularly, review when done, commit. It lives at `skills/engineering/implement/SKILL.md`.

The mechanism is unusually literal — the entire skill is **six lines of body text**, and its frontmatter carries `disable-model-invocation: true`, meaning it never auto-triggers from a description match. It runs only when the user explicitly invokes `/implement` against a PRD or a set of issues. When invoked it instructs the agent to:

1. Implement the work described in the PRD/issues.
2. Use `/tdd` "where possible, at pre-agreed seams."
3. Run typechecking regularly, single test files regularly, and the full test suite once at the end.
4. Use `/review` to review the work once done.
5. Commit the work to the current branch.

So `implement` carries almost no method of its own. Its value is entirely as a **conductor**: it sequences three things that are individually well-developed elsewhere in the repo. `/tdd` (read in full) is a substantial skill — vertical-slice tracer-bullet TDD, an explicit anti-pattern section against horizontal slicing, a planning checklist that reads `CONTEXT.md`/ADRs and confirms the public interface with the user, plus three bundled reference files (`tests.md`, `mocking.md`, `refactoring.md`). `/review` (read in full) is a two-axis review skill that spawns parallel Standards and Spec sub-agents against `git diff <fixed-point>...HEAD`. `implement` is the 6-line wrapper that says "do TDD, then review, then commit" and leaves the depth to the skills it calls.

The load-bearing decisions are: (a) **seams, not blanket TDD** — "at pre-agreed seams" concedes that not all code is worth testing-first and pushes the agent to agree the testable boundaries with the user rather than reflexively TDD everything; (b) **a graded test cadence** — single files often, full suite once at the end, which is the cheap-feedback-loop discipline that keeps an implementation session fast; and (c) **review-then-commit as a non-optional tail**, so work doesn't land on the branch unreviewed.

## How we tested it

**Evidence:** REVIEW

Skill-mechanism review: read the full `implement/SKILL.md` source pulled from the repo, then read the two skills it composes (`tdd/SKILL.md` and `in-progress/review/SKILL.md`) to understand what the orchestrator actually delegates to and whether the family is self-contained. I did **not** install the plugin or run `/implement` end-to-end on a live PRD — this is a process/orchestration skill whose entire substance is the six instructions above, which are reproduced in full, and the decisive catalog question is composition + redundancy against the user's already-installed GSD and superpowers, which is a documentary comparison. I also confirmed `disable-model-invocation: true` in the frontmatter (it is an explicit slash command, not an auto-triggering skill) and checked the existing catalog entry (CATALOG.md line 142) and its stated overlaps.

```bash
gh api repos/mattpocock/skills --jq '{stars, license:.license.spdx_id, description, updated}'
gh api "repos/mattpocock/skills/git/trees/main?recursive=1" --jq '.tree[].path' | grep -iE "implement|tdd|review"
gh api repos/mattpocock/skills/contents/skills/engineering/implement/SKILL.md --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/engineering/tdd/SKILL.md       --jq '.content' | base64 -d
gh api repos/mattpocock/skills/contents/skills/in-progress/review/SKILL.md     --jq '.content' | base64 -d
# Catalog / competitor scan:
grep -inE "implement|GSD|superpowers|test-driven|executing-plans|subagent-driven" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Honest about being a conductor.** It doesn't reinvent TDD or review; it names two strong sibling skills and orders them. For anyone already committed to the mattpocock family, this is the missing "do the whole loop" entry point, and the delegation keeps each concern in its own well-developed file rather than bloating one mega-skill.
- **"TDD at pre-agreed seams" is the right amount of restraint.** It avoids the common over-prescription of "TDD everything." Pairing it with `/tdd`'s own planning checklist (confirm the interface and which behaviors matter *with the user* first) means the agent agrees the testable boundaries up front instead of reflexively writing tests for glue code.
- **The graded test cadence is the cheap-feedback-loop lever.** "Single test files regularly, full suite once at the end" is exactly the discipline that keeps an implementation session fast without skipping verification — run the narrow signal constantly, pay for the broad signal once.
- **Review-then-commit tail is non-optional.** Ending on `/review` (two-axis Standards + Spec in parallel sub-agents) before committing means work doesn't land unreviewed. That's a real correctness/maintainability gate baked into the default flow.
- **`disable-model-invocation: true` is a deliberate, correct choice.** An orchestrator that fired automatically on any "implement this" phrasing would hijack sessions and double-trigger against the user's GSD/superpowers loops. Making it an explicit `/implement` command scopes it cleanly.
- **Strong provenance.** 136K-star MIT repo, pushed today, Matt Pocock. Same credibility as the sibling skills already evaluated ADOPT/CONDITIONAL.

## What didn't work or surprised us

- **Almost no standalone value.** Stripped of `/tdd` and `/review`, the skill is "implement it, test sometimes, review, commit" — generic advice the model mostly does anyway. Its leverage is **conditional on having the rest of the family installed**. The catalog markets the plugin as 17 composable skills; `implement` is the clearest case of a skill that only pays off as part of the set.
- **Heavy overlap with the user's existing loops.** The user already runs **GSD** (Discuss→Plan→Execute→Verify→Ship with restricted-tool subagents and durable STATE.md/CONTEXT.md) and **superpowers** (`executing-plans`, `subagent-driven-development`, `test-driven-development`, `requesting-code-review`, `verification-before-completion`). Both already provide an implement-stage loop with TDD + review + commit/verify gates. GSD's `/gsd:execute-phase` and superpowers' `executing-plans` are *richer* orchestrators (state persistence, wave parallelization, explicit verification-before-completion). `implement` is the lightweight version of something the user already has two of.
- **Depends on `/review` from `skills/in-progress/`.** The review skill it calls is parked under `in-progress/`, signaling it's not yet stable. An orchestrator whose final gate points at an in-progress dependency carries that maturity risk.
- **Review needs project plumbing.** `/review` expects `docs/agents/issue-tracker.md` (run `/setup-matt-pocock-skills`) to fetch the spec axis; without it the Spec sub-agent degrades to "no spec available." So the tail gate is only fully effective in a repo set up the mattpocock way.
- **The cadence/typecheck step is TypeScript-flavored.** "Run typechecking regularly" assumes a separate typecheck phase; in languages where the test run *is* the typecheck, that instruction is slightly redundant — minor, but consistent with the TS lean noted in the sibling merge-conflict eval.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Bakes a graded test cadence and a mandatory `/review` (Standards + Spec) gate into the default implement flow before commit — but most of this comes from the delegated skills, not from `implement` itself |
| Speed | + | "Single files often, full suite once at the end" is the cheap-feedback-loop discipline; one `/implement` invocation chains the loop instead of the user driving each step |
| Maintainability | + | TDD-at-seams + review-then-commit keeps landed work tested and reviewed; relies on `/tdd`'s behavior-not-implementation philosophy to avoid brittle tests |
| Safety | neutral | Process skill, no new permissions or attack surface; commit-to-current-branch is a mild convenience, not a risk given the review gate precedes it |
| Cost Efficiency | + | Graded cadence avoids running the full suite every loop; tiny prompt footprint — but it adds little the user's existing GSD/superpowers loops don't already deliver |

## Verdict

**CONDITIONAL**

`implement` is a clean, well-authored, intentionally minimal Implement-stage orchestrator whose two best ideas — TDD at *pre-agreed seams* (not blanket TDD) and a graded test cadence (single files often, full suite once) capped by a mandatory review-then-commit tail — are genuinely good defaults. But it carries almost no method of its own: it is a 6-line conductor for `/tdd` and `/review`, so its value is **conditional on adopting the mattpocock family**, and it is additive only for someone *not* already running an implement loop. The user runs **two** richer ones (GSD's execute-phase and superpowers' executing-plans/test-driven-development/requesting-code-review), both of which already provide TDD + review + verify/commit gates with state persistence the thin `implement` lacks. Adopt it **only if you standardize on the mattpocock skill set** (so `/tdd` and `/review` are present and the issue-tracker plumbing is set up) — in which case it's the natural `/implement` entry point. Otherwise it is redundant with the user's existing GSD/superpowers stack; do not add it as a third competing implement loop.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [implement](https://github.com/mattpocock/skills) | skill | Thin orchestrator: TDD at seams, typecheck regularly, review when done, commit | Need a repeatable implementation flow that enforces quality gates | tdd, feature-dev, GSD (execute-phase), superpowers (executing-plans) |
