# Plan 002: Make COMPARISON's Summary report the real evaluation funnel (Validated %, not 100%)

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- COMPARISON.md reconcile-counts.py audit-evals.py catalog_lib.py test_automation.py`
> On any in-scope change since 4cc412e, compare "Current state" excerpts
> against the live code first; on a mismatch, STOP.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED (three coupled artifacts — summary generator, detector G, tests — must change in lockstep)
- **Depends on**: plans/001-fix-stale-counts.md (same files; avoid merge conflicts)
- **Category**: docs
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

`COMPARISON.md`'s Summary table reports every stage "Evaluated 100%" — but the file's own Legend defines `discovery-log` as "*not a verdict*: surfaced in triage but never exercised." 473 of 582 rows are discovery-log. The real validated share is ~19% (109/582 rows carry a genuine verdict). The headline metric that should drive prioritization instead reports the backlog as empty. This plan splits the Summary into honest columns so "what to evaluate next" (plan 005) has a true number to shrink.

## Current state

- `COMPARISON.md` Summary block (verified at 4cc412e, near the bottom of the file):

  ```
  ## Summary

  | Stage | Tools | Evaluated | Adoption rate |
  |-------|-------|-----------|---------------|
  | Plan | 54 | 54 | 100% |
  ...
  | **Total** | **582** | **582** | **100%** |
  ```

- `COMPARISON.md` Legend (lines 5-10) — the verdict vocabulary (ADR 0001, `docs/decisions/0001-verdict-vocabulary.md`): ADOPT/KEEP/CONDITIONAL/SKIP/DEFER are real verdicts; **discovery-log** is "a catalogued *lead*, not a verdict … Excluded from verdict-sync (D) and verdict-evidence (K)."
- Verdict distribution (verified 2026-07-03): ADOPT 25, KEEP 9, CONDITIONAL 14, SKIP 58, DEFER ~5, discovery-log ~473 (of 582 rows). ADOPT/KEEP per stage: Plan 6, Skills&Plugins 4, Reference 4, Implement 4, Review 3, Reflect 3, Verify 2, Outer Loop 2, Memory&Context 2, MCP Servers 2, Ship 1, Research&Discovery 1.
- The Summary is **generated** by `reconcile-counts.py` → `fix_comparison(text, C)` at line 45 (with inner `fix_sec` at line 50) — never hand-edit it.
- It is **gated** by detector G → `audit_comparison(ctx)` at `audit-evals.py:824`: the per-stage summary must sum to the body rows and Total must equal the CATALOG entry count.
- Both behaviors are **pinned** by `test_automation.py` (temp fixtures). Row parsing lives in `catalog_lib.py` (`validate_comparison_rows`, verdict-row parsing centralized per commits `1a18a12`/`747413f`).
- Repo invariant: `make check` runs all of these; any change must land in the same commit across generator + detector + tests or CI goes red.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Full gate | `make check` | exit 0 |
| Regenerate summary | `python3 reconcile-counts.py` | exit 0 |
| Detector G alone | `python3 audit-evals.py --comparison` | "OK", exit 0 |
| Unit tests | `python3 -m unittest -q test_automation` | OK |
| Plugin sync | `./sync-plugin-docs.sh` | exit 0 |

## Scope

**In scope**:
- `reconcile-counts.py` (`fix_comparison` — new summary shape)
- `audit-evals.py` (`audit_comparison` — gate the new shape)
- `catalog_lib.py` ONLY if a verdict-classification helper ("is this token a real verdict?") belongs there — it likely does, since the Legend's split is a domain rule (check first whether one already exists: `grep -n "discovery-log\|ADOPT" catalog_lib.py`)
- `test_automation.py` (update pinned fixtures/assertions)
- `COMPARISON.md` (regenerated Summary — via the script, never by hand)
- `plans/README.md` (status row)

**Out of scope**:
- The Legend text and ADR 0001 (the vocabulary itself doesn't change)
- Body rows / verdict values (no verdict is edited)
- `README.md`/`STACK.md`/`CLAUDE.md` totals (plan 001)
- Detectors other than G

## Git workflow

- Branch: `advisor/002-honest-funnel-metric`
- One commit for generator+detector+tests+regenerated file together (lockstep), e.g. `feat(comparison): split Summary into Catalogued/Validated/Recommended (#<issue>)`

## Steps

### Step 1: Decide the target shape (fixed here — do not redesign)

New Summary columns:

```
| Stage | Tools | Validated | Recommended | Validated % |
```

- **Tools** = body-row count per stage (unchanged semantics).
- **Validated** = rows whose Evaluated cell is a real verdict: ADOPT, KEEP, CONDITIONAL, SKIP, or DEFER (per the Legend; discovery-log excluded).
- **Recommended** = ADOPT + KEEP.
- **Validated %** = Validated/Tools, integer percent.
- Total row keeps bold formatting. The word "Evaluated" leaves the summary header; detector G's "CATALOG == COMPARISON" total check must still compare **Tools** total to the CATALOG count.

### Step 2: Add/locate the verdict classifier in catalog_lib.py

If `catalog_lib.py` lacks a helper, add `REAL_VERDICTS = {"ADOPT","KEEP","CONDITIONAL","SKIP","DEFER"}` and `def is_real_verdict(token) -> bool`. Reuse the existing verdict-row parsing (centralized there) — do not re-parse rows with new regexes in reconcile.

**Verify**: `python3 -c "import catalog_lib; print(catalog_lib.is_real_verdict('discovery-log'), catalog_lib.is_real_verdict('ADOPT'))"` → `False True`

### Step 3: Update fix_comparison in reconcile-counts.py

Rewrite the summary builder to emit the Step-1 shape, computing Validated/Recommended per stage from parsed body rows via the `catalog_lib` helpers.

**Verify**: `python3 reconcile-counts.py` → exit 0, and `grep -A16 "^## Summary" COMPARISON.md` shows the new columns with Total `**582**` Tools and Validated ≈ **109** (exact number comes from the data; it must equal the sum of real-verdict rows, NOT 582).

### Step 4: Update detector G (audit_comparison) to gate the new shape

The detector must now verify: per-stage Tools sums to body rows; per-stage Validated equals the recomputed real-verdict count; Total Tools == CATALOG count. Keep its finding messages' file:line style.

**Verify**: `python3 audit-evals.py --comparison` → OK. Then a negative test: temporarily hand-edit one Validated cell in `COMPARISON.md`, re-run → non-zero exit naming the row; revert (`git checkout -- COMPARISON.md`, then re-run `python3 reconcile-counts.py`).

### Step 5: Update pinned tests

Update `test_automation.py` fixtures/assertions for the new summary shape (both the reconcile side and the detector-G side — locate via `grep -n "Adoption\|Evaluated\|audit_comparison\|fix_comparison" test_automation.py`). Add one case proving discovery-log rows are excluded from Validated.

**Verify**: `python3 -m unittest -q test_automation` → OK.

### Step 6: Sync plugin copies and run the full gate

`./sync-plugin-docs.sh` then `make check`.

**Verify**: `make check` → exit 0.

## Test plan

- Updated pinned tests for `fix_comparison` and `audit_comparison` (Step 5), including a discovery-log-exclusion case and a drift-detection negative case.
- Manual negative test in Step 4.

## Done criteria

- [ ] `grep -A3 "^## Summary" COMPARISON.md` shows `| Stage | Tools | Validated | Recommended | Validated % |`
- [ ] Summary Total: Tools **582**, Validated < 582 (real count), no "100%" on any stage that contains discovery-log rows
- [ ] `python3 audit-evals.py --comparison` → exit 0; hand-corrupting a cell makes it exit non-zero
- [ ] `python3 -m unittest -q test_automation` → OK
- [ ] `make check` → exit 0
- [ ] `plans/README.md` status row updated

## STOP conditions

- `fix_comparison`/`audit_comparison` no longer match the line numbers/shape above (refactor landed — re-locate, and if parsing moved further into `catalog_lib`, adapt rather than duplicating).
- Changing the shape breaks a consumer you didn't anticipate (grep first: `grep -rn "Adoption rate" --include="*.py" --include="*.sh" .` — if anything besides reconcile/detector G/tests reads the summary, STOP and report).
- The Validated total you compute differs from ~109 by more than ±10 — your classifier probably mis-handles a verdict token (e.g. dual verdicts like "KEEP/installed"); report what tokens you found.

## Maintenance notes

- Plans 005/006 consume "Validated %" as the gap weight — keep column names stable.
- Reviewer: check the lockstep — generator, detector, tests, and the regenerated COMPARISON.md must be one commit.
- Deferred: surfacing Validated % in README (plan 007's front-door page will do it).
