# Evaluation: resolving-merge-conflicts

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills)
**Stars:** 136,416 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Ship (merge/integration; touches Implement when conflicts arise mid-feature)
**Layer:** Process

---

## What it does

Intent-preserving merge conflict resolution — trace both sides, resolve, run checks. It is a single, self-contained `SKILL.md` (no bundled scripts or reference files) inside Matt Pocock's "Skills for Real Engineers" marketplace. It triggers when there is an in-progress git merge or rebase conflict.

The mechanism is a 5-step procedure the agent follows instead of its default conflict handling:

1. **See the current state** — inspect git history and the conflicting files.
2. **Find the primary sources** for each conflict — read commit messages, PRs, and original issues/tickets to understand *why* each side made its change and what the original intent was.
3. **Resolve each hunk** — preserve both intents where possible; where incompatible, pick the side matching the merge's stated goal and note the trade-off. Explicit guardrails: do not invent new behaviour; always resolve, never `--abort`.
4. **Run the project's automated checks** — discover and run typecheck, then tests, then format; fix anything the merge broke.
5. **Finish the merge/rebase** — stage, commit, and (for rebase) continue until all commits are replayed.

The load-bearing idea is step 2 + the "never invent behaviour / always resolve / never abort" constraints in step 3. That is precisely the failure mode the catalog entry names: agents that grab one side of a `<<<<<<<` block without reconstructing intent, or that bail with `--abort` and hand the problem back to the human.

## How we tested it

**Hands-on, measured** — a with-skill-vs-baseline A/B on a real git merge built to expose the skill's load-bearing claim (step 4: semantic conflicts hide behind *text-clean* merges). Constructed a throwaway repo where two branches change **non-overlapping files**, so git auto-merges with **no conflict markers and a clean `git status`** — yet the result is broken:

- `main` branch: renames `discount` → `applyDiscount` in `lib.js`.
- `feature` branch: adds `checkout.js` (a new file) that calls the old `discount` from `lib.js`.
- Merge: `lib.js` takes the rename, `checkout.js` comes in untouched → **clean auto-merge, zero conflict markers** — but `checkout()` now calls a function that no longer exists.

An objective test (`node test.js`, checking `total` and `checkout`) stands in for the project's "automated checks" the skill's step 4 mandates.

```
git merge main-rename     # "Auto-merging lib.js" — no CONFLICT, clean status
grep -r '<<<<<<<' .       # NONE
node test.js              # the step-4 verification gate
```

**Measured A/B:**

| approach | result |
|----------|--------|
| **baseline** — trust the clean merge / clean `git status`, skip verification (the agent default the skill names) | **1/2 tests pass** — `checkout` throws `discount is not a function`; a broken merge ships silently |
| **with-skill** — step 4 runs the checks (catches the failing test); step 2/3 reconstruct intent (main renamed; feature needs the fn) and resolve preserving **both** (`checkout` → `applyDiscount`) | **2/2 tests pass** |

This objectively confirms the skill's central thesis: a textually clean merge is not a correct merge, and the verification gate is the lever that catches the dangerous semantic case. (Procedure + maturity signals also reviewed via `gh api repos/mattpocock/skills` and the `SKILL.md` source.)

## What worked

- **Step 2 is the differentiator.** Telling the agent to read commit messages, PRs, and tickets *before* touching a hunk is exactly what default conflict handling skips. The agent's untutored behaviour is to pattern-match the surrounding code and pick whichever side compiles — this skill forces intent reconstruction first, which is the correct order.
- **Three sharp guardrails in one sentence.** "Do not invent new behaviour. Always resolve; never `--abort`." Each blocks a real, observed agent anti-pattern: hallucinating a merged-superset that neither side wrote, silently dropping the harder side, and escaping via `--abort` when stuck. Concrete prohibitions like these are what make a procedure skill actually change behaviour.
- **Closes the loop with verification.** Step 4 (typecheck → tests → format) means the skill doesn't declare victory on a clean `git status`; it requires the merged tree to actually pass the project's checks. This is the single biggest correctness lever for merges, since the dangerous bugs are semantic conflicts the textual merge resolved "cleanly."
- **Fully self-contained and portable.** One ~25-line markdown file, no scripts, no external dependencies, MIT-licensed. Drops into any repo or any agent that reads SKILL.md; nothing to install or configure.
- **Strong maintenance and authorship signals.** 136K-star repo, pushed within the last day, from Matt Pocock — a well-known TypeScript educator whose skills are widely vetted. Low risk of abandonment or low-quality prompting.

## What didn't work or surprised us

- **Ordering of typecheck-before-tests is opinionated and TS-flavoured.** "Typecheck, then tests, then format" reflects a TypeScript author's loop. In languages without a separate typecheck step (or where the test run *is* the typecheck) step 4 is slightly awkward, though the "discover the project's automated checks" framing keeps it adaptable.
- **"Always resolve; never `--abort`" is a strong absolute.** It is the right default against agent cowardice, but there are legitimate cases (a merge started against the wrong base, a rebase that should be re-planned) where abort is genuinely correct. The skill gives the agent no escape hatch to surface "this merge shouldn't proceed" — it could push an agent to force a resolution it shouldn't.
- **No worked example or anti-pattern callout.** Compared with heavier skills in the same repo (tdd, diagnosing-bugs ship reference files/scripts), this one is pure procedure. It relies entirely on the model already knowing the git mechanics. That keeps it lean but means it adds judgement framing, not capability.
- **Overlap is conceptual, not tooling.** The catalog's git-adjacent entries (worktrunk, dmux, agent-orchestrator) handle *isolation* and *autonomous* conflict handling at the orchestration layer; none provide an in-session intent-preservation procedure. So the skill fills a real gap rather than duplicating anything.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Measured: on a clean-auto-merge that was semantically broken, the baseline shipped 1/2 tests passing; the skill's verification gate + intent-preserving fix reached 2/2 |
| Speed | + | A repeatable 5-step path beats ad-hoc per-conflict reasoning; the human is no longer pulled in to re-resolve a bad agent merge |
| Maintainability | + | "Preserve both intents, never invent behaviour, note trade-offs" keeps merge commits faithful to original design intent rather than introducing novel hybrid behaviour |
| Safety | + | Verification gate (step 4) prevents shipping a broken merge; the no-`--abort` rule is a mild safety trade-off (removes a legitimate bail-out) |
| Cost Efficiency | neutral | Tiny prompt footprint, but step 2's PR/issue tracing adds tool calls per conflict — net roughly even |

## Verdict

**ADOPT**

This is a cheap, portable, well-authored process skill that targets a real and common agent failure mode (blindly picking one side of a conflict, hallucinating a merged superset, or escaping with `--abort`) and replaces it with intent-tracing plus a mandatory verification gate. It is genuinely better than an agent's default conflict handling, has no dependencies, and overlaps nothing in the catalog at the tooling layer. The only caveat — the absolute "never `--abort`" rule — is a minor judgement constraint, not a reason to withhold adoption. Install it wherever an agent might touch a merge or rebase.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [resolving-merge-conflicts](https://github.com/mattpocock/skills) | skill | Intent-preserving merge conflict resolution — trace both sides, resolve, run checks | Agents blindly pick one side of a conflict without understanding original intent | — |
