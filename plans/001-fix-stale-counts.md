# Plan 001: Fix stale prose counts and bring the eval count under reconcile-counts.py

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- STACK.md README.md CLAUDE.md reconcile-counts.py test_automation.py`
> If any in-scope file changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: docs
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

This repo's credibility rests on its numbers being derived, not hand-maintained ("Never hand-edit counts" — `CLAUDE.md`). Yet `STACK.md:147` says "**497 tools** are cataloged" while `STACK.md:3` on the *same page* says 582, and "471 evaluations" appears in three places while 487 eval files exist. A reader who spots 497 vs 582 stops trusting every other number. The tool count IS reconciled by `reconcile-counts.py`; the "497" and the eval count sit outside its substitution patterns and drifted.

## Current state

- `reconcile-counts.py` — the count propagator. Key functions (verified at commit 4cc412e): `catalog_count()` at line 27, `fix_total_strings(text, C)` at line 40 (rewrites tool-total strings across README/CLAUDE/STACK/plugin), `fix_comparison(text, C)` at line 45, `main()` at line 64. It currently reconciles the **tool** count only.
- Stale strings, verified 2026-07-03:
  - `STACK.md:147`: `- **497 tools** are cataloged in [CATALOG.md](CATALOG.md) — this page is the curated subset` (actual: 582)
  - `STACK.md:3`: `The ~25 tools worth installing on every project, distilled from 582 catalog entries and 471 evaluations.` (471 is stale; actual eval count: 487)
  - `README.md:29`: `- [STACK.md](STACK.md) — the ~25 tools worth installing, distilled from 471 evaluations`
  - `README.md:31`: `- [evaluations/](evaluations/) — 471 evidence-based evaluations with verdicts (ADOPT/CONDITIONAL/SKIP)`
  - `CLAUDE.md:15` says "~20 tools" while `README.md:29` and `STACK.md:3` say "~25 tools" — pick ~25 (matches the actual STACK size) and align CLAUDE.md.
- Eval count ground truth: `ls evaluations/*.md | wc -l` → 488 files, minus `evaluations/TEMPLATE.md` = **487** evals. (`audit-evals.py` reports "487/487 evals declare Evidence".)
- Repo conventions: root files are authoritative; `plugin/CLAUDE.md` and `plugin/docs/` are synced copies — never edit them directly, run `./sync-plugin-docs.sh`. `test_automation.py` pins reconcile behavior with temp fixtures; new substitution behavior needs a pinned test (model after the existing reconcile tests in `test_automation.py` — find them with `grep -n "reconcile" test_automation.py`).

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Full gate | `make check` | exit 0 |
| Reconcile (apply) | `python3 reconcile-counts.py` | prints updated file list, exit 0 |
| Reconcile (check) | `python3 reconcile-counts.py --check` | "OK — … consistent", exit 0 |
| Unit tests | `python3 -m unittest -q test_automation` | OK, exit 0 |
| Plugin sync | `./sync-plugin-docs.sh` | "Synced: …", exit 0 |

## Scope

**In scope** (the only files you should modify):
- `reconcile-counts.py` (add eval-count substitution)
- `test_automation.py` (pin the new behavior)
- `STACK.md`, `README.md`, `CLAUDE.md` (one-time correction of the stale strings)
- `plugin/CLAUDE.md`, `plugin/docs/STACK.md` (via `./sync-plugin-docs.sh` / reconcile only — never by hand)
- `plans/README.md` (status row)

**Out of scope** (do NOT touch):
- `COMPARISON.md` and its Summary block (plan 002's territory)
- `catalog_lib.py`, `audit-evals.py` (no detector changes needed here)
- Any count that is already derived correctly (the 582 tool totals)

## Git workflow

- Branch: `advisor/001-fix-stale-counts` off up-to-date `main`
- Conventional commits, e.g. `fix(counts): derive eval count in reconcile; correct stale 497/471 prose`
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Add an eval-count source and substitution to reconcile-counts.py

In `reconcile-counts.py`, add a function `eval_count(root=None)` next to `catalog_count()` (line 27) that counts `evaluations/*.md` files excluding `TEMPLATE.md`. Then extend the substitution logic (pattern of `fix_total_strings`, line 40) to rewrite the string `NNN evaluations` (regex like `\b\d+ evaluations\b`) and `NNN evidence-based evaluations` in `README.md` and `STACK.md` to the derived value. Match the file's existing style (module-level functions, `read`/`write` helpers at lines 24-25). Keep `--check` semantics: in check mode, report drift and exit non-zero instead of writing.

**Verify**: `python3 reconcile-counts.py --check` → exits non-zero, reporting the stale 471 strings (they haven't been fixed yet — this proves detection works).

### Step 2: Fix the stale prose strings

- `STACK.md:147`: change `**497 tools**` to `**582 tools**` — then immediately convert it to the derived form: confirm the string now matches the pattern `fix_total_strings` rewrites (compare with the already-derived `582` at `STACK.md:3`; run `python3 reconcile-counts.py` and confirm it leaves the line stable). If the pattern doesn't cover the "N tools are cataloged" phrasing, extend the regex in `fix_total_strings` so it does — the goal is this line can never drift again.
- `CLAUDE.md:15`: change `(~20 tools to actually install, with commands)` to `(~25 tools to actually install, with commands)`.

**Verify**: `python3 reconcile-counts.py` → exit 0; then `grep -n "497\|471 evaluations" STACK.md README.md` → no matches; `grep -n "487 evaluations\|487 evidence-based" README.md STACK.md` → the three corrected lines.

### Step 3: Pin the new behavior in test_automation.py

Add a test to `test_automation.py` (find the existing reconcile test class via `grep -n "class.*Reconcile\|reconcile" test_automation.py` and model after it — temp fixtures, never the real files): fixture with a fake `evaluations/` dir of K files + TEMPLATE.md and a README containing `999 evaluations`; assert reconcile rewrites it to K and that `--check` flags it before, passes after.

**Verify**: `python3 -m unittest -q test_automation` → OK.

### Step 4: Sync and run the full gate

Run `./sync-plugin-docs.sh`, then `make check`.

**Verify**: `make check` → exit 0.

## Test plan

- New unit test in `test_automation.py` (Step 3): eval-count derivation, substitution, and `--check` drift detection.
- Full-gate regression: `make check` exit 0.

## Done criteria

- [ ] `grep -rn "497 tools" STACK.md` → no matches
- [ ] `grep -rn "471 evaluations\|471 evidence-based" README.md STACK.md` → no matches
- [ ] `python3 reconcile-counts.py --check` → exit 0
- [ ] `python3 -m unittest -q test_automation` → OK (includes the new test)
- [ ] `make check` → exit 0
- [ ] Only in-scope files modified (`git status`)
- [ ] `plans/README.md` status row updated

## STOP conditions

Stop and report back (do not improvise) if:

- The strings at `STACK.md:3/147`, `README.md:29/31`, `CLAUDE.md:15` don't match the excerpts above (drift since planning).
- `reconcile-counts.py`'s structure differs materially from the function map above (a refactor landed — re-locate the seam before editing).
- Extending the substitution would require touching `catalog_lib.py` (that's a bigger refactor; report instead).
- `make check` fails on a detector unrelated to counts after your change.

## Maintenance notes

- Future eval additions/removals now auto-propagate the eval count — CI (`make check` → `reconcile --check`) will fail if someone hand-edits it.
- Reviewer should scrutinize: the regex for `N evaluations` must not accidentally rewrite unrelated numbers (e.g. issue references); the test fixture guards this.
- Deferred: bringing the "~25 tools" sizing under derivation (it's an approximation, low drift risk).
