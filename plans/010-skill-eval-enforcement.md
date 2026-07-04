# Plan 010: Enforce the skill-eval protocol — required section for skill evals plus a report-only detector

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- evaluations/TEMPLATE.md audit-evals.py CLAUDE.md test_automation.py`
> Plan 009 intentionally edits TEMPLATE.md — coordinate: land 009 first.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: plans/009-measurement-protocols.md (both edit TEMPLATE.md; 009 defines the Test-design block this plan's skill variant slots into)
- **Category**: direction (methodology)
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The repo documents a genuinely strong skill-evaluation protocol — two dimensions, Triggering (does the description fire on the right prompts?) and Output quality (with-skill vs baseline A/B), per `TEMPLATE.md:31-33` and closed issue #38 — and `evaluations/skill-creator.md` proves it works end-to-end. But it's an optional blockquote, and it shows: 3 of 9 ADOPT-verdict skills remain review-based with no measured A/B (verified 2026-07-03 via `audit-evals.py --skills`: agent-skills-addyosmani, cc-skills-golang, vercel-labs-agent-skills). Skills are this repo's highest-volume recommendation type; the guidance-vs-guardrail gap the repo flags in other tools applies to its own methodology. This plan turns the guidance into structure (a required section for skill evals) and visibility (a detector counting non-compliant skill evals), without gating.

## Current state

- `evaluations/TEMPLATE.md:31-33` (verified, read in full): the skill blockquote — "If the entry is a _skill_ … evaluate two dimensions: 1. **Triggering** — does the skill's `description` make it fire on the right prompts and *not* the wrong ones? … (`skill-creator/scripts/run_eval.py` measures this with `claude -p`; or judge a balanced should/shouldn't-trigger prompt set.) 2. **Output quality** — run a **with-skill vs baseline A/B** … A not-run skill review must still say so."
- Existing per-metric detector to model on: `--skills` (report-only) already lists ADOPT skills with/without measured backing — locate via `grep -n "def audit_skill" audit-evals.py`. This plan's detector is broader: ALL skill-type evals, checking for the structural section, not just ADOPT.
- Detector conventions: `DetectorContext` inputs (commit `7db411a`); report-only = opt-in flag + always-exit-0; documented in CLAUDE.md's detector list; characterization-tested in `test_automation.py`.
- After plan 009, TEMPLATE.md has a `## Test design` section (task/baseline/metric/reproduce).

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Existing metric | `python3 audit-evals.py --skills` | report |
| New detector | `python3 audit-evals.py --skill-design` | report, exit 0 |
| Tests | `python3 -m unittest -q test_automation` | OK |

## Scope

**In scope**:
- `evaluations/TEMPLATE.md` (promote the skill blockquote into a conditional required section)
- `audit-evals.py` (new opt-in report-only detector `--skill-design`)
- `CLAUDE.md` (detector list bullet)
- `test_automation.py` (characterization test)
- `plugin/` via sync; `plans/README.md`

**Out of scope**:
- Running the 3 backlog skill A/Bs (that's eval execution — it belongs to the NEXT-EVALS queue, plan 005; the eval-runner agent exists for it)
- Gating the detector (report-only first, same lifecycle as `--overlaps`)
- Backfilling existing skill evals with the new section

## Steps

### Step 1: Promote the blockquote in TEMPLATE.md

Replace the skill blockquote (:31-33) with a conditional section placed inside/adjacent to plan 009's Test-design block:

```markdown
### Test design — skills (required when Type is skill or plugin)

A skill's value is a *change in agent behaviour* — measure both dimensions (issue #38):

- **Triggering:** {should-fire prompts k/N; shouldn't-fire prompts k/N — via
  skill-creator's run_eval.py or a balanced hand-judged set. Skills tend to under-trigger.}
- **Output A/B:** {same prompt with skill on vs off; deltas (tokens/latency) + an
  explicit accuracy check. Deterministic skills: apply SKILL.md rules by hand + tiktoken.}
- **Not run?** say so plainly — the honesty rule above applies unchanged.
```

Keep every factual element of the original blockquote (run_eval.py pointer, under-trigger note, tiktoken/caveman pointer, issue #38 link).

**Verify**: `grep -n "Triggering" evaluations/TEMPLATE.md` shows the new section; `make check` → exit 0 (template still parses).

### Step 2: Add the --skill-design detector

`audit_skill_design(ctx)`: for every eval whose catalog Type is skill or plugin (reuse the Type lookup the `--skills` detector already does), report which lack BOTH a triggering result and an A/B (heuristic: absence of the section header AND absence of trigger-vocabulary — reuse/extend the detector-B regex style; keep the heuristic conservative to avoid false-flags). Output: compliant/total counts + the non-compliant list. Report-only, opt-in flag.

**Verify**: `python3 audit-evals.py --skill-design` → a count like "N/M skill evals record a triggering test or A/B" with a list; `evaluations/skill-creator.md` and `evaluations/caveman.md` are in the compliant set (they demonstrably contain A/B content); exit 0.

### Step 3: Document + test + sync

CLAUDE.md bullet (mirror `--skills` bullet style: "a tracked metric, not a gate"). `test_automation.py` fixture test: one fixture skill eval with a Triggering line → compliant; one without → flagged. `./sync-plugin-docs.sh`; `make check`.

**Verify**: `python3 -m unittest -q test_automation` OK; `make check` exit 0.

## Test plan

Step-3 fixture tests; manual compliant/non-compliant spot-checks in Step 2.

## Done criteria

- [ ] TEMPLATE.md has the required skills Test-design section (blockquote promoted, no content lost)
- [ ] `python3 audit-evals.py --skill-design` reports compliant/total + list, exit 0
- [ ] skill-creator and caveman classified compliant
- [ ] CLAUDE.md documents the flag; tests OK; `make check` exit 0
- [ ] `plans/README.md` updated

## STOP conditions

- Plan 009 hasn't landed and TEMPLATE.md has no Test-design block — either land this as a standalone section (acceptable; say so) or STOP if the template structure conflicts.
- The compliant-detection heuristic false-flags more than ~5 evals you can verify DO contain A/B content — the vocabulary needs widening (same rule as detector B's HONEST vocab: widen the regex, don't weaken the eval); if widening doesn't converge, STOP and report examples.

## Maintenance notes

- The 3 backlog skills (agent-skills-addyosmani, cc-skills-golang, vercel-labs-agent-skills) should surface near the top of NEXT-EVALS.md (plan 005) — ADOPT verdict + no measured backing is exactly what the queue exists for; verify that after both plans land.
- Gating `--skill-design` for *new* skill evals (not the backlog) is the natural follow-up once the count stabilizes.
- Reviewer: confirm the promoted section keeps the "not run? say so" escape hatch — enforcement must never pressure fabrication.
