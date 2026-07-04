# Plan 009: Generalize the token-savings protocol into per-signal measurement protocols (Correctness, Speed) and a Test-design template block

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- evaluations/TEMPLATE.md evaluations/token-savings-protocol.md CLAUDE.md audit-evals.py`
> On drift, re-verify "Current state" first.

## Status

- **Priority**: P1 (highest-leverage methodology change)
- **Effort**: M (documentation + template; no mass eval rewrite)
- **Risk**: LOW
- **Depends on**: none
- **Category**: direction (methodology)
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The repo evaluates tools against five quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency — `CLAUDE.md:9`) but has a **measurement protocol for exactly one**: Cost, via `evaluations/token-savings-protocol.md` (fixed corpus + fixed tokenizer + with/without A/B + honest recording). The other four are recorded as `{+/-/neutral}` + one sentence (`TEMPLATE.md:50-57`) even in evals stamped MEASURED — so "MEASURED" spans everything from a rigorous multi-variant A/B (skill-creator: 6/6 broken-skill oracle) to an n=1 smoke run (beads: one dependency chain, no baseline). The badge doesn't communicate rigor, comparative bake-offs have no metric to rank on, and graduation (REVIEW→MEASURED) has no defined bar for anything but token savings. This plan writes the missing protocols for the two measurable signals and adds a required Test-design block to the template.

## Current state

- `evaluations/token-savings-protocol.md` (read at 4cc412e) — the pattern to generalize. Its four moves: **fix a corpus** (real, disclosed artifact), **fix the tokenizer** (`tiktoken cl100k_base`, deterministic), **measure with/without**, **record honestly** (claimed X% vs measured Y%; "A tool that underdelivers is recorded as such"). A passing verification "graduates that tool's eval REVIEW → MEASURED and lets tier-stack.py promote it toward STACK Tier 1." Companion detector: `--savings-claims` makes the backlog "a number to shrink."
- `evaluations/TEMPLATE.md` (read in full):
  - Evidence definitions at :19-25 — `MEASURED` = "ran it hands-on **and** captured metrics (token deltas, latency, A/B accuracy, counts)"; `RUN` = "executed it hands-on, but no formal metrics".
  - Skill-eval protocol at :31-33 (blockquote) — two dimensions: Triggering (`skill-creator/scripts/run_eval.py` / balanced should-shouldn't prompt set) and Output quality (with-skill vs baseline A/B).
  - Quality-signals table at :50-57 — `| Signal | Impact {+/-/neutral} | Evidence {one sentence} |`.
- Verdict-evidence gate (detector K, `CLAUDE.md`): ADOPT/KEEP must be run-backed or disclaimered — the *presence* of a run is gated; its *design* is not.
- Convention: methodology docs live in `evaluations/` as protocol files (token-savings-protocol.md is itself an eval-shaped file with Evidence MEASURED); `CLAUDE.md` documents them; TEMPLATE changes affect future evals only (no retroactive rewrite).

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Sync | `./sync-plugin-docs.sh` | exit 0 |
| Fabrication detector (guards template wording) | `python3 audit-evals.py --fabrication` | OK |

## Scope

**In scope**:
- `evaluations/measurement-protocols.md` (create — the per-signal protocol index)
- `evaluations/TEMPLATE.md` (add the Test-design block; tighten the quality-signals table's instructions; keep every existing section)
- `CLAUDE.md` (one bullet referencing the protocols next to the token-savings bullet)
- `plugin/` via sync; `plans/README.md`

**Out of scope**:
- Rewriting ANY existing eval (protocols apply to new/graduating evals)
- Changing the Evidence taxonomy tokens (MEASURED/RUN/REVIEW/SOURCE-ONLY are load-bearing across detectors B/K, backfill, tier-stack — see maintenance note re. finding 7's "rigor tier" idea, deliberately deferred)
- New detectors (a `--measurement-design` detector is a follow-up once protocols exist)
- Maintainability/Safety protocols (judgment-heavy; see Step 1 for how they're handled honestly)

## Steps

### Step 1: Write evaluations/measurement-protocols.md

Structure (~120-160 lines):

1. **Preamble**: what this is — the generalization of `token-savings-protocol.md`'s method to the other signals; the four moves (fix the task, fix the measure, run with/without, record honestly) stated once.
2. **Correctness protocol**: fix a small task set (3-5 tasks with binary pass/fail oracles — the skill-creator eval's pattern: N variants with known-correct answers, report pass-rate with vs without the tool). Define: task set must be disclosed in the eval; oracle must be mechanical (test passes, output matches, linter accepts); report as `k/N with vs k/N without`.
3. **Speed protocol**: fix the same task set; measure wall-clock and/or agent-turn count with vs without, same harness/model, N≥3 runs, report median + range. Tokens-in/out per task where the harness reports them.
4. **Maintainability & Safety — honest rubric, not fake numbers**: these stay qualitative BY POLICY; the protocol is a named-criteria rubric (Maintainability: does it reduce file size/coupling/duplication in the diff it produces — cite the diff; Safety: permissions requested, network calls made, sandbox compatibility — cite observations). One paragraph each. State plainly: a rubric judgment is not a measurement and never alone justifies MEASURED.
5. **What qualifies as MEASURED** (restating TEMPLATE :20 with the new teeth): at least one signal measured under its protocol — a with/without delta on a disclosed task set. An n=1 smoke run with no baseline is RUN, not MEASURED.
6. **Worked pointers**: token-savings-protocol.md (Cost), `evaluations/skill-creator.md` (Correctness A/B), `evaluations/caveman.md` (deterministic token A/B).

**Verify**: file exists; `grep -c "with vs without\|with/without" evaluations/measurement-protocols.md` ≥ 3; it cites the three worked examples.

### Step 2: Add the Test-design block to TEMPLATE.md

Insert after the honesty-rule blockquote (:29) and before the skill blockquote (:31), a required section:

```markdown
## Test design

> Required for MEASURED evals; recommended for RUN. See evaluations/measurement-protocols.md.

- **Task/corpus:** {the fixed, disclosed input}
- **Baseline:** {what "without the tool" means here}
- **Metric:** {pass-rate / wall-clock / tokens / counts — per the protocol}
- **Reproduce:** {the command(s) to re-run this measurement}
```

Also amend the MEASURED definition line (:20) to append: "…counts) **under a protocol from measurement-protocols.md — a with/without delta on a disclosed task, not an n=1 smoke run**."

**Verify**: `grep -n "Test design" evaluations/TEMPLATE.md` → present between the honesty rule and the skill blockquote; `python3 audit-evals.py --fabrication` and `--selftest` still OK (the classifier parses TEMPLATE-shaped evals — confirm no detector chokes on the new section: run `make check`).

### Step 3: Document in CLAUDE.md and sync

Add a bullet next to the token-savings-protocol reference: "`evaluations/measurement-protocols.md` — per-signal measurement protocols (Correctness/Speed measured with-vs-without on a disclosed task set; Maintainability/Safety as named-criteria rubrics); the bar an eval must clear to claim MEASURED." Run `./sync-plugin-docs.sh`.

**Verify**: `make check` → exit 0.

## Test plan

No unit surface — the verification is `make check` (detector suite parses the modified TEMPLATE and any protocol file without new findings) plus the greps above. The real test is the first eval that uses it: plan 011's pilot bake-off runs under these protocols.

## Done criteria

- [ ] `evaluations/measurement-protocols.md` exists with the 6 parts above
- [ ] TEMPLATE.md has the Test-design block; MEASURED definition names the protocol bar
- [ ] CLAUDE.md references it; plugin synced
- [ ] `make check` → exit 0
- [ ] `plans/README.md` updated

## STOP conditions

- Any detector fails after the TEMPLATE edit (the eval parser in `audit-evals.py` may pin section order — check `--selftest` output; if the parser needs a code change to tolerate the new section, that's in-scope only if it's a one-line pattern addition; otherwise STOP).
- You're tempted to add numeric scoring to Maintainability/Safety — don't; the honest-rubric stance is the decision here (fake precision is the failure mode this repo exists to fight).

## Maintenance notes

- Deliberately deferred: splitting the MEASURED badge into rigor tiers (e.g. MEASURED-AB vs MEASURED-smoke). The Evidence tokens flow through detectors B/K, `backfill-evidence.py`, `tier-stack.py`, and COMPARISON — a token change is a multi-artifact migration. Revisit after ~10 evals have used the Test-design block; the block itself already records the rigor distinction as data.
- The tightened MEASURED definition makes some *existing* MEASURED evals retroactively generous (e.g. n=1 runs). Do not relabel them in this plan; the staleness/watchlist machinery (plans 006/008) will cycle them through re-verification naturally.
- Reviewer: the protocol doc must not promise what an agent can't honestly do unattended — every metric is mechanical-oracle-based by design.
