# Evaluation: tdd

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd)
**Stars:** 203,610 (repo-metadata.json, fetched 2026-08-04; the live API read 274,584 on 2026-10-02) | **Last updated:** 2026-09-17 (last commit touching `skills/engineering/tdd`, `d80fa0f`) | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Implement / Verify
**Layer:** Process

---

## What it does

Red-green loop with vertical tracer-bullet slices and tests through public interfaces. The
skill is three markdown files (no scripts): `SKILL.md` (559 words), `tests.md` (good vs bad
test examples: implementation-coupled, tautological) and `mocking.md` (mock only at system
boundaries; inject dependencies). Its frontmatter `description` fires on "build features or
fix bugs test-first", "red-green-refactor", or "integration tests". It is the most-installed
testing skill on skills.sh (~1M installs).

The mechanism is a reference the agent consults on every cycle:

1. **Seams first.** Name the public interface under test and *confirm the seams with the
   user* before writing any test.
2. **Anti-patterns.** No implementation-coupled tests, no tautological expected values, and
   no **horizontal slicing** (writing all tests, then all implementation).
3. **Rules of the loop.** Red before green; one seam, one test, one minimal implementation
   per cycle; no speculative code.
4. **Refactoring is explicitly *not* part of the loop.** The current `SKILL.md` moves it to
   the review stage (the `code-review` skill). The catalog one-liner it was catalogued under
   still says "red-green-refactor"; the skill no longer does the refactor step.

## How we tested it

**Evidence:** MEASURED

**Hands-on**, measured with-skill-vs-baseline A/B: 20 headless agent runs (2 tasks x 2 arms
x N=5) plus a 14-prompt triggering test, scored by three mechanical oracles that do not
depend on our judgement.

**Harness.** Each run is a fresh `claude -p` (Claude Code 2.1.287, `--model sonnet`) in an
empty directory holding only `SPEC.md`. Isolation was verified first: with
`--setting-sources project --disable-slash-commands` the agent reports no available skills
and none of the user-level CLAUDE.md rules (a control run without those flags *did* see the
user's "mandatory TDD" rule, which would have contaminated the baseline). Both arms get the
identical user prompt, which already asks for TDD, so the A/B isolates what the skill adds
over the model's own idea of TDD:

> Build the module described in SPEC.md using test-driven development. Put the
> implementation in `<file>.js` ... and your tests in `<file>.test.js` using node:test and
> node:assert. Run the tests with `node --test`. No npm dependencies. You are running
> non-interactively: you cannot ask questions, so make reasonable assumptions and finish.

The **with-skill** arm adds `--append-system-prompt-file` holding `SKILL.md` + `tests.md` +
`mocking.md` verbatim (skill commit `d80fa0f`). Tools were scoped to file edits plus
`Bash(node:*)` under `--permission-mode acceptEdits`.

**Tasks** (both pure Node, zero deps):

- **T1 `parseDuration(str)`**: 7 behaviours (units, ordered compound components,
  whitespace, decimals with `Math.round`, bare-integer ms, lowercase units, TypeError vs
  RangeError). The spec carries worked examples for most rules.
- **T2 `createCache({capacity, ttlMs, now})`**: an LRU with TTL and an injected clock;
  7 behaviours stated as prose with no examples (`has` is not a use, `get` does not extend
  life, `set` on an existing key restarts TTL without evicting, `size()` excludes expired,
  expired entries are dropped before a live one is evicted, etc.).

**Oracles:**

1. **Hidden acceptance suite** (30 tests for T1, 24 for T2), written against a reference
   implementation before any agent ran; k/N on the agent's implementation.
2. **Planted-mutant kill rate of the agent's own tests**: 16 hand-planted mutants of *our
   reference* implementation per task, each confirmed to be killed by the hidden suite. A
   mutant counts as killed only if a test that **passes on the reference** fails on the
   mutant, so a test encoding a different reading of the spec cannot kill mutants for free.
   Comparable across runs because every arm's tests face the same 16 bugs.
3. **Tool-order trace** from the `stream-json` transcript: test-file writes (T), impl
   writes (I), test runs (R), with permission-denied calls dropped. Counts T-to-I cycles
   (vertical slices) and whether a red run preceded the first implementation write.

Plus **Stryker-js 10.0.0** (command runner, `node --test`) on each agent's own tests vs its
own implementation, as a secondary test-quality score.

**Results, T1 `parseDuration`** (medians, range in brackets):

| metric | baseline (n=5) | with-skill (n=5) |
|---|---|---|
| hidden acceptance | **30/30 in 5/5** | **30/30 in 5/5** |
| planted mutants killed by own tests | 16/16 in 5/5 | 16/16 in 5/5 |
| Stryker score, own tests on own impl | 85.7% [83.6-86.8] | 87.8% [86.4-88.1] |
| T-to-I cycles (vertical slices) | 1 [1-1] | 4 [4-6] |
| red run before first impl write | 2/5 | 5/5 |
| impl non-blank LOC | 29 [25-40] | 24 [23-29] |
| agent turns | 7 [6-9] | 23 [20-33] |
| output tokens | 2,668 | 6,579 |
| wall-clock (s) | 21 [18-33] | 52 [46-74] |
| cost per run (USD) | 0.077 | 0.197 |

**Results, T2 `createCache`:**

| metric | baseline (n=5) | with-skill (n=5) |
|---|---|---|
| hidden acceptance | **24/24 in 5/5** | **24/24 in 5/5** |
| planted mutants killed by own tests | 13/16 [12-14] | 13/16 [11-15] |
| Stryker score, own tests on own impl | 89.1% [87.0-93.9] | 89.8% [89.0-91.5] |
| T-to-I cycles (vertical slices) | 1 [1-1] | 4 [3-5] |
| red run before first impl write | 0/5 | 5/5 |
| impl non-blank LOC | 64 [58-64] | 51 [45-62] |
| agent turns | 5 [5-5] | 22 [16-24] |
| output tokens | 3,963 | 7,577 |
| wall-clock (s) | 25 [24-28] | 58 [43-61] |
| cost per run (USD) | 0.084 | 0.205 |

Every baseline run wrote the whole test file in one shot and then the whole implementation
(`TIR` / `TRIR`): exactly the **horizontal slicing** the skill names as its anti-pattern.
Every with-skill run alternated test, red run, implementation, green run
(`TRIRTRIRTRIR...`), and every with-skill run in T2 stated the seam it assumed, for example
*"I couldn't confirm seams with you, so I assumed the only seam is the public
`createCache` API."*

**T2 mutant survivors** show what *neither* arm's tests pinned: M14 (`set` on an existing
key at capacity evicts another entry) survived in **10/10** runs; M06 (`delete` of an
expired entry returns `true`) survived in 5/5 baseline and 2/5 with-skill; M05 (`size()`
counts expired entries) in 2/5 baseline and 4/5 with-skill. One run per arm (base-1,
skill-1) asserted that `ttlMs: Infinity` must throw, which our reference accepts. That is a
genuine ambiguity in our spec ("positive number"), so those tests were excluded from the
mutant oracle per its rule, and it hit both arms equally.

**Triggering test.** The skill was installed as a project skill (`.claude/skills/tdd/`) in
an otherwise empty, isolated project, and each prompt was given to `claude -p` once, with
tools limited so the agent could invoke `Skill` but not edit. Scored on whether
`Skill(tdd)` was invoked:

| set | result |
|---|---|
| should fire (6): "using TDD", "red-green-refactor", "test-first: write a failing test", "add integration tests", "tests written before the code", "write the tests first" | **6/6 fired** |
| should not fire (6): rename a variable, explain a regex, README section, `.gitignore`, rebase vs merge, callback to async/await | **0/6 fired** |
| probes (2): "Implement a slugify function", "Fix the bug where paginate returns one item too many" (no test wording) | 0/2 fired |

```
# A/B arm (one run): T1 shown; T2 swaps SPEC.md / prompt / filenames
claude -p --setting-sources project --disable-slash-commands --strict-mcp-config \
  --model sonnet --permission-mode acceptEdits \
  --allowedTools "Read" "Write" "Edit" "Glob" "Grep" "Bash(node:*)" \
  --output-format stream-json --verbose \
  [--append-system-prompt-file skill-prompt.md]   # with-skill arm only
  "$(cat prompt.txt)" > transcript.jsonl

# oracles 1-3 over all runs of a task
python3 oracles.py t1 duration.js duration.test.js
python3 oracles.py t2 cache.js cache.test.js

# secondary: Stryker on each run's own code
npx stryker run   # stryker.conf.json: testRunner "command", commandRunner "node --test <file>.test.js"

# triggering: tdd installed at .claude/skills/tdd/, 14 prompts, once each
claude -p --setting-sources project --strict-mcp-config --model sonnet --max-turns 3 \
  --allowedTools "Skill" "Read" --disallowedTools "Write" "Edit" "Bash" \
  --output-format stream-json --verbose "<prompt>"
```

## Test design

- **Task/corpus:** two disclosed pure-Node tasks above (`parseDuration`, 7 behaviours with
  examples; `createCache`, 7 prose-only behaviours with an injected clock), each with a
  reference implementation, a hidden acceptance suite (30 / 24 tests) and 16 planted mutants
  (T1: wrong unit multipliers, ordering/duplicate checks removed, whitespace handling,
  `Math.floor` for `Math.round`, bare-number handling, case folding, empty-is-zero,
  wrong error class, no trim, `parseInt` for decimals, leading-dot and negative accepted;
  T2: `has` counts as use, `get` not a use, `get` extends life, expiry off-by-one, `size`
  counts expired, `delete` of expired returns true, `set` keeps old TTL, evict MRU, no
  purge before evict, `set` not a use, capacity off-by-one, no option validation, `set` of
  existing evicts, ignores `now`, `get` returns expired).
- **Baseline:** identical prompt (already asking for TDD) and harness, with no skill text;
  the user-level CLAUDE.md, user skills, plugins and MCP servers are excluded from both arms.
- **Metric:** hidden-suite k/N; planted-mutant kills of the agent's own tests; Stryker
  score; T-to-I cycles and red-before-green from the transcript; turns, output tokens,
  wall-clock and cost from the `result` event. N=5 per arm per task, medians + ranges.
- **Reproduce:** the commands above. Fixtures, the reference implementations, mutant
  generators (`make-mutants.py`), the oracle (`oracles.py`) and all 20 transcripts are kept
  in the session scratchpad (`scratchpad/evals/tdd/`), not committed to this repo.
- **Disclosed limits:** n=5 per cell is small and no significance test is claimed. One model
  (Sonnet) only. Both tasks are small pure functions; the skill's seam and mocking guidance
  matters most on code with real collaborators, which these tasks barely exercise (T2's
  injected clock is the only boundary). The skill text was injected via system prompt in the
  A/B rather than loaded through the `Skill` tool, so the A/B measures the content and the
  triggering test measures the loading. The project dir in the triggering test held only
  this skill, so it did not compete with superpowers' or agent-skills' own TDD skills.
  The A/B harness denied 1-2 Bash calls per with-skill run (heredoc writes outside
  `node:*`); agents recovered via the Edit tool, and denied calls are dropped from the order
  trace.

### Test design — skills (required when Type is skill or plugin)

- **Triggering:** should-fire **6/6**, shouldn't-fire **0/6** false positives, on a balanced
  hand-written 12-prompt set run once each via `claude -p` with `Skill(tdd)` detection in
  the transcript. Two ambiguous probes without test wording ("implement X", "fix bug Y")
  fired 0/2, which matches the description's scope ("test-first"), so a user who wants TDD
  must say so.
- **Output A/B:** with-skill vs baseline, same prompt, N=5 per arm on two tasks. Process
  changes sharply (vertical slices 1 to 4 cycles; red-first 2/10 to 10/10; ~17-20% smaller
  implementations). Output correctness and test strength do **not** move measurably
  (acceptance 100% in both arms; planted-mutant kills equal at the median; Stryker within
  ~1-2 points). Cost rises ~2.5x (turns ~3-4x, wall-clock ~2.3x).

## What worked

- **It eliminates horizontal slicing, every time.** 10/10 baseline runs wrote all tests then
  all code, even though the prompt said "test-driven development". 10/10 with-skill runs did
  genuine one-test-one-implementation cycles (median 4 per task) with a red run before
  every implementation write. That is the skill's headline claim, and it holds.
- **Smaller, less speculative implementations.** "Only enough code to pass it" showed up as
  ~5 fewer LOC on T1 and ~13 fewer on T2 at the median, with Stryker generating fewer
  mutants on the with-skill code (T2: 59-91 vs 82-100), without losing any hidden-suite
  behaviour.
- **Tests stayed on the public interface in both arms.** Every agent test file, in both
  arms, ran unchanged against our independently written reference (apart from the one
  `Infinity` ambiguity), so no run produced implementation-coupled tests. That is good, but
  it means the skill's anti-coupling guidance had nothing to fix on these tasks.
- **Triggering is clean.** 6/6 on explicit test-first wording, 0/6 false positives.
- **It degrades sensibly when it cannot ask.** The "confirm seams with the user" step has
  no user in headless mode; agents stated their assumed seam instead of stalling.

## What didn't work or surprised us

- **No measurable correctness or test-strength gain on small tasks.** Both arms passed
  100% of the hidden suites. On T2, where the spec is prose-only and tests had to be
  designed, planted-mutant kills were 13/16 median in both arms, and both arms missed the
  same subtle rule (M14: 10/10 survived). Doing TDD properly did not make the agent think
  of more behaviours to test; the skill changes *how* tests are written, not *which*.
- **~2.5x the cost and ~2.3x the wall-clock.** Each cycle is a write, a run, a write, a
  run: median 22-23 turns vs 5-7. On a task the model already gets right, that is pure
  overhead.
- **"Confirm seams with the user" is an interactive gate.** Unattended pipelines (routines,
  `claude -p`) cannot satisfy it; the skill gives no fallback rule, and the agent improvises
  one.
- **Catalog wording drift.** The catalog one-liner says "red-green-refactor", while the
  current `SKILL.md` says refactoring is *not* part of the loop and belongs to review.
- **Under-triggers on plain feature requests**, by design: "implement slugify" never loads
  it. If you want TDD by default you need a CLAUDE.md rule or an enforcing hook
  ([tdd-guard](tdd-guard.md)), not this description.
- **Three TDD skills compete.** obra/superpowers and addyosmani/agent-skills each ship a
  `test-driven-development` skill with overlapping descriptions; installing more than one
  makes which fires a coin flip. This test did not measure that contention.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Measured: hidden acceptance 100% in both arms on both tasks (20/20 runs); no delta to attribute |
| Speed | - | Measured: median wall-clock 21s to 52s (T1) and 25s to 58s (T2); turns 7 to 23 and 5 to 22 |
| Maintainability | + | Rubric (not a measurement): implementations ~17-20% smaller at the median with no lost behaviour; tests stay at the public interface |
| Safety | neutral | Pure prompt text; requests no tools or permissions of its own |
| Cost Efficiency | - | Measured: ~2.5x cost per task (USD 0.077 to 0.197; 0.084 to 0.205) and ~2x output tokens |
| Verifiability | + | Measured process change: every with-skill transcript shows auditable red-then-green cycles (10/10 vs 0/10 baseline vertical slicing), so "was this actually test-driven?" becomes checkable from the tool log; test strength itself (mutant kills, Stryker) was unchanged |

## Verdict

**CONDITIONAL** — adopt-if: you want the agent to actually *practise* vertical red-green TDD
(auditable test-first cycles, minimal implementations) and accept ~2.5x tokens and time per
task for it; do not adopt it expecting more correct code or stronger tests on its own.

Measured, it does exactly what it claims to the process and nothing measurable to the
outcome: 10/10 baseline runs horizontally sliced despite being asked for TDD, 10/10
with-skill runs did real one-test-at-a-time cycles, yet hidden-suite pass rates (100% vs
100%), planted-mutant kills (equal medians) and Stryker scores (within 2 points) did not
move on these two small tasks. MIT-licensed and from mattpocock/skills, already a STACK
source (resolving-merge-conflicts), so the licence and provenance bar is clear. Pick one TDD
skill (this one, superpowers' or agent-skills' `test-driven-development`), not several. If
you need TDD *enforced* rather than taught, pair it with tdd-guard. Re-test on a task with
real collaborators, where its seam and mocking guidance has room to matter.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tdd](https://github.com/mattpocock/skills/tree/main/skills/engineering/tdd) | skill | Red-green loop in vertical tracer-bullet slices, testing behaviour through public interfaces | Agents write implementation first, or bulk-write tests that pin implementation details | test-driven-development, tdd-guard, implement |
