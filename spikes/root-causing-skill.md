# Spike: Best skill for root-causing an issue

**Issue:** [#119](https://github.com/mattbutlerengineering/ai-tooling/issues/119) ·
**Date:** 2026-06-23 · **Status:** complete (recommendation below) ·
**Evidence:** REVIEW — source-grounded (full read of all three `SKILL.md` files +
their supporting assets + license/provenance checks). **Not a measured A/B**: a
clean head-to-head of *process* skills run by the same agent is confounded
(the agent applies all three), so I did not fake a benchmark. A real measured test
is specified under "Recommended next steps."

> Spikes live outside `evaluations/` on purpose — they compare several tools and
> carry no single `## Verdict`, so they aren't parsed by the eval/verdict gates.
> Promoting a pick here into a catalog ADOPT verdict needs a real measured eval.

---

## The question

Issue #119 asks for the **best skill for root-causing an issue** and named three
diagnosis-loop candidates. This spike reads all three in full, applies the repo's
adoption + evidence bars strictly, and names a clear pick.

## TL;DR — strict recommendation

**Primary pick: `systematic-debugging`** (from `obra/superpowers`, **MIT**, catalogued).
It is the most complete and the most *root-cause-specific* of the three. Both it and the
runner-up are MIT and catalogued, so the choice is decided on **methodology, not provenance**.

| | Skill | Use it for | Adoptable? |
|---|---|---|---|
| **1 (primary)** | **systematic-debugging** | The default for root-causing — especially **multi-component/distributed bugs** and stopping **fix-thrashing** | ✅ MIT, catalogued via `obra/superpowers` (★-backed, maintained) |
| **2 (leaner alt)** | **diagnosing-bugs** | Single-process, **agent-runnable** bugs where a fast red/green loop is the whole game | ✅ MIT — `mattpocock/skills` (★143K); catalogued (COMPARISON: discovery-log / REVIEW, eval file exists) |
| **collapse** | **diagnose** | — | ❌ Older (2026-05-18), uncatalogued local copy; upstream `mattpocock/skills` now ships `diagnosing-bugs` instead → **deprecate/merge** |

**But take one thing from the runner-up:** graft `diagnosing-bugs`' **3–5 ranked
falsifiable hypotheses** and its **"red-capable loop before any hypothesis" gate**
onto `systematic-debugging`, whose Phase 3 forms a *single* hypothesis (a documented
anchoring weakness). That combination — systematic-debugging's root-cause gate +
supporting tracing techniques + diagnosing-bugs' loop-first + multi-hypothesis
discipline — is the strongest root-causing process available here.

---

## What each skill actually is (verified 2026-06-23)

### systematic-debugging — *root-cause-gate* · 296-line SKILL + supporting library
- **Philosophy:** the **Iron Law — "NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST."**
  Four gated phases: Root-Cause Investigation → Pattern Analysis → Hypothesis & Testing
  → Implementation. This is the skill literally built around *root-causing*.
- **Strengths:**
  - Dedicated **multi-component boundary evidence-gathering** (log what enters/exits each
    layer, find *where* it breaks before *why*) — the best fit for distributed/CI/pipeline bugs.
  - Ships a real **supporting-technique library**: `root-cause-tracing.md` (backward
    data-flow tracing to the origin), `defense-in-depth.md`, `condition-based-waiting.md`,
    `find-polluter.sh`.
  - **Hardened against agent rationalization** — red-flag list, anti-excuse table,
    "human-partner signals," and `test-pressure-1/2/3.md` scenarios that stress-test the skill.
  - **3-fixes-failed → question the architecture** rule (stops infinite fix loops).
  - Integrates with `superpowers:test-driven-development` and `verification-before-completion`.
- **Weakness:** Phase 3 says *"Form **Single** Hypothesis"* — single-hypothesis generation
  anchors on the first plausible idea. Reproduction is a checklist item, not the centerpiece;
  it's lighter on *building a fast deterministic feedback loop* than `diagnosing-bugs`.
- **Provenance/license:** **MIT** (`obra/superpowers`, Jesse Vincent); catalogued
  (`superpowers` is a catalog entry, and `systematic-debugging` is named as a conceptual
  peer in CATALOG.md's format note). **Verified.**

### diagnosing-bugs — *feedback-loop-first* · 134-line SKILL + `hitl-loop.template.sh`
- **Philosophy:** **"Phase 1 IS the skill"** — build a **tight, red-capable, deterministic,
  fast, agent-runnable** feedback loop before anything else. 6 phases: Build loop →
  Reproduce+**minimise** → Hypothesise → Instrument → Fix+regression-test → Cleanup+post-mortem.
- **Strengths (the two things it does better than systematic-debugging):**
  1. **Feedback-loop-first gate** — "no red-capable command (already run, paste it), no
     Phase 2." The loop is the single highest-leverage debugging move, and this enforces it.
  2. **3–5 ranked, falsifiable hypotheses** (each must state a prediction) — beats
     single-hypothesis anchoring.
  - Also: a **minimise** step (shrinks the hypothesis space), `[DEBUG-xxxx]`-tagged logs
    for clean teardown, a perf-regression branch, correct-seam analysis, and a post-mortem
    that hands off to `improve-codebase-architecture`.
- **Weaknesses:** No supporting-technique library (only the HITL helper); **less explicit**
  on multi-component boundary tracing — the exact thing systematic-debugging excels at.
- **Provenance/license:** **`mattpocock/skills`** (`https://github.com/mattpocock/skills`),
  **MIT**, ★143K, pushed 2026-06-18. **Catalogued** — `CATALOG.md` row + `COMPARISON.md`
  (discovery-log / REVIEW) + `evaluations/diagnosing-bugs.md`. License-clean and adoptable;
  the choice vs systematic-debugging is purely methodological. **Verified.**

### diagnose — older predecessor → collapse
- ~95% identical to `diagnosing-bugs` but **older** (2026-05-18 vs 2026-06-18) and **weaker**:
  it lacks the "tight loop that goes red" completion checklist and the Phase-2 **minimise**
  step. It is an **uncatalogued local copy**; upstream `mattpocock/skills` now ships
  `diagnosing-bugs` in its place. Same "synthesis vs dedup" situation as opencode/oh-my-pi in
  the GLM spike — **deprecate `diagnose`, keep `diagnosing-bugs`.**

---

## Decision rationale (why systematic-debugging wins, strictly)

1. **Matches the ask.** The ticket says *root-causing*. systematic-debugging is gated on
   root-cause-first and ships the only dedicated **backward root-cause-tracing** technique.
2. **Completeness.** It's the only candidate with a supporting-technique library and
   pressure-tested hardening — not just a single SKILL.md.
3. **Verifiable & adoptable.** Confirmed **MIT** and maintained in a **catalogued** plugin.
   `diagnosing-bugs` is *also* MIT + catalogued (`mattpocock/skills`), so provenance is a
   wash between the top two — the decision rests on completeness and root-cause specificity,
   not licensing. Only `diagnose` (uncatalogued local copy) is excluded on provenance.
4. **Coverage of the worst case.** Multi-component bugs (CI → build → sign; API → svc → DB)
   are where agents thrash hardest; only systematic-debugging gives an explicit
   boundary-evidence procedure for them.

The runner-up wins on **two mechanics** (loop-first gate; multi-hypothesis), so the
recommended end state is not "pick one and discard the rest" but **systematic-debugging
as the base, patched with those two mechanics.**

## Exclusions / non-picks

- **`diagnose`** — superseded by `diagnosing-bugs`; keeping both is duplication. Collapse.
- **Broader skills considered and set aside as not *root-causing***: `verification-before-completion`
  (confirms a fix, doesn't find the cause), `receiving-code-review` (different loop),
  `improve` / `improve-codebase-architecture` (post-fix prevention — systematic-debugging and
  diagnosing-bugs both *hand off* to it, which is the correct relationship).

## Evidence & limitations

- **REVIEW, not measured.** Conclusions are from reading the skills, not from a scored run.
- **Provenance now resolved** (post-spike follow-up): `diagnosing-bugs` is MIT and catalogued
  (`mattpocock/skills`); only `diagnose` remains an uncatalogued local copy. The earlier
  "license unconfirmed" caveat no longer applies to the runner-up.
- One mid-spike correction worth recording: the supporting library
  (`root-cause-tracing.md` et al.) belongs to **systematic-debugging**, *not* diagnosing-bugs
  (an initial mis-read, verified by `ls` per directory). The recommendation rests on the
  corrected facts.

## Recommended next steps

1. **Measured A/B** to graduate this to a catalog verdict: seed one **multi-component** bug
   and one **single-process** bug in a throwaway repo copy; run each skill cold (separate
   sessions to limit cross-contamination); score **time-to-root-cause**, **root-cause
   correctness**, and **false-fix rate**. Predicted result: systematic-debugging wins the
   multi-component case, diagnosing-bugs wins the single-process speed case.
2. **Graft** diagnosing-bugs' loop-first gate + 3–5 ranked hypotheses into systematic-debugging
   (or maintain a thin local overlay).
3. **Deprecate `diagnose`**; keep `diagnosing-bugs` as the leaner variant.
4. ~~Confirm `diagnosing-bugs` provenance/license~~ — **done**: MIT (`mattpocock/skills`),
   already catalogued (`evaluations/diagnosing-bugs.md`).

## Sources (read in full this session)

- `~/.claude/plugins/cache/claude-plugins-official/superpowers/6.0.3/skills/systematic-debugging/`
  (SKILL.md + `root-cause-tracing.md`, `defense-in-depth.md`, `condition-based-waiting.md`,
  `find-polluter.sh`, `test-pressure-*.md`) — license MIT per `superpowers` `plugin.json`
- `~/.claude/skills/diagnosing-bugs/SKILL.md` (+ `scripts/hitl-loop.template.sh`)
- `~/.claude/skills/diagnose/SKILL.md`
- `CATALOG.md` (superpowers row; systematic-debugging cited as a conceptual peer)
