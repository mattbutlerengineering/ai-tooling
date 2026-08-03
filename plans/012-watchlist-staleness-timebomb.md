# Plan 012: Stop `make check` from failing on a calendar date with zero commits

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat a388dd2..HEAD -- watchlist.py WATCHLIST.md test_automation.py audit-evals.py`
> If any of those changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `a388dd2`, 2026-08-03

## Why this matters

`make check` is this repo's single gate, and CI (`.github/workflows/integrity.yml`) runs
exactly it. One of its gates, `python3 watchlist.py --check`, byte-compares `WATCHLIST.md`
against a freshly rendered copy — and one section of that page is derived from
`datetime.date.today()`. On **2026-10-21** the staleness sweep goes from 0 stale evals to
**184**, so the rendered page will differ from the committed one and `watchlist.py --check`
will exit 1. Nothing will have been committed. CI goes red on every open PR, on `main`, and
inside every unattended routine run, purely because a date passed.

The daily discovery routine (`docs/agents/routines.md`) runs `make fix && make check` and
treats a red gate other than detector A as a blocker — so the first routine after that date
either halts or lands a 184-row `WATCHLIST.md` diff that has nothing to do with its lane.

This is not hypothetical and it is not far off: the cliff is **79 days** from this plan's
date, and further cliffs follow at +95, +96 and +98 days and on through the winter. The fix
is to stop *gating* on the
time-dependent section while still *rendering* it, so `make fix` keeps the page fresh and a
calendar date can never turn CI red.

## Current state

### Files

- `watchlist.py` — generates `WATCHLIST.md`; `--check` is a gate in `make check`.
- `WATCHLIST.md` — the generated page. Section 3 is the time-dependent one.
- `audit-evals.py` — hosts `audit_staleness(ctx, today=None)`, which `watchlist.py` calls.
- `test_automation.py` — the unit suite; `TestWatchlist` is the exemplar to extend.
- `Makefile` — line 29 gates `watchlist.py --check`; line 32 runs the staleness *report*
  with a leading `-` so it can never fail the build. These two lines contradict each other
  today; this plan resolves the contradiction in favor of line 32's intent.

### The time-dependent call

`watchlist.py:118-127` — note the docstring already claims determinism, and is wrong about
the consequence:

```python
def render(ctx):
    """The full WATCHLIST.md text. Fully regenerated each run (markers wrap the body
    so a future tool can locate the block). Deterministic: every value is derived from
    file content. The one time-dependent input is section 3's stale *set* (which evals
    have crossed their staleness threshold) — it changes only when a date crosses a
    threshold, at which point `make fix` regenerates the page; the ages themselves are
    not printed, so nothing drifts day-to-day."""
    defer_rows, defer_missing = deferred(ctx)
    flagged, _flag_lines = stack_flagged(ctx)
    stale, undated = ae.audit_staleness(ctx)
```

`audit-evals.py:264-281` — the detector, already injectable:

```python
def audit_staleness(ctx, today=None):
    """Detector L (#65, REPORT-ONLY): flag evals whose **Last verified:** date is older
    than its category threshold (STALENESS_DAYS, keyed by Type) — fast-moving harnesses/
    MCP servers rot sooner than stable references. `today` is injectable for tests.
    Returns (stale, undated) where stale is a list of (name, type, date, age_days,
    threshold) and undated is the count of evals carrying no last-verified date."""
    today = today or datetime.date.today()
```

Note the docstring says **REPORT-ONLY**. `watchlist.py --check` accidentally makes it gating.

### Section 3's render block

`watchlist.py:177-196`:

```python
    L += [
        "",
        f"## 3. Stale / undated evals ({len(stale)} stale)",
        "",
        "A point-in-time eval rots. The staleness sweep flags evals whose "
        "`**Last verified:**` date is older than its category threshold; ages are not "
        "printed so the page stays deterministic (`make fix` regenerates when a date "
        "crosses a threshold).",
        "",
        "| Eval | Type | Last verified | Threshold (days) |",
        "|------|------|---------------|------------------|",
    ]
    if stale:
        for name, typ, date, _age, threshold in stale:
            L.append(f"| {name} | {typ} | {date} | {threshold} |")
    else:
        L.append("| _none stale_ | | | |")
    L += [
        "",
        f"_{undated} eval(s) carry no `**Last verified:**` date "
        "(field presence is gated separately by `backfill-lastverified.py`)._",
    ]
```

### The byte comparison

`watchlist.py:229-256`:

```python
def main():
    check = "--check" in sys.argv[1:]
    ctx = ae.DetectorContext(ROOT)
    new, defer_missing = apply(ctx)
    ...
    current = open(WATCHLIST, encoding="utf-8").read() if os.path.exists(WATCHLIST) else None
    if check:
        if new != current:
            print("watchlist check: DRIFT — WATCHLIST.md is stale; run ./watchlist.py")
            sys.exit(1)
        print("watchlist check: OK — WATCHLIST.md matches the derived watchlist"); sys.exit(0)
    if new != current:
        open(WATCHLIST, "w", encoding="utf-8").write(new)
```

### The existing marker convention (follow it)

`watchlist.py:37`:

```python
WATCHLIST = os.path.join(ROOT, "WATCHLIST.md")
START, END = "<!-- WATCHLIST:START -->", "<!-- WATCHLIST:END -->"
```

`tier-stack.py` uses the same idea with `TIERS:START` / `TIERS:END` in `STACK.md`. Adding a
nested marker pair for the volatile section matches established repo convention — do not
invent a different mechanism (no JSON sidecar, no timestamp file, no `--as-of` flag).

### Repo conventions that apply

- Python 3, **stdlib only**. No new dependencies, no type annotations (the codebase has
  none), 4-space indent, comments that explain *why*.
- Every generator has a `--check` / apply pair and is wired into both `Makefile` targets.
- Tests live in `test_automation.py`, run against fixtures in a temp dir — **never** against
  the real `CATALOG.md` / `WATCHLIST.md`. See the module docstring at `test_automation.py:1-18`.
- `CLAUDE.md` documents the staleness sweep as *report-only*: "only *presence* is gated;
  making staleness itself gating is a later decision." This plan makes the code match that
  written decision.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Regenerate the page | `python3 watchlist.py` | exit 0 |
| Gate the page | `python3 watchlist.py --check` | exit 0, prints `watchlist check: OK` |
| Unit suite | `python3 -m unittest -q test_automation` | exit 0, no failures |
| Full gate | `make check` | exit 0 (needs network + `gh` auth for detector A) |
| Offline subset | `python3 audit-evals.py --offline` | exit 0 |

`make check`'s last real gate, `audit-evals.py --installs`, needs network access and `gh`
auth. If it fails with an auth/network error in your environment, that is **not** caused by
this change — note it and rely on the other commands.

## Scope

**In scope** (the only files you should modify):

- `watchlist.py`
- `WATCHLIST.md` (regenerated, never hand-edited)
- `test_automation.py`

**Out of scope** (do NOT touch, even though they look related):

- `audit-evals.py` — `audit_staleness` is already correct and already injectable. Do not
  change the detector, its thresholds, or its report.
- `Makefile` — line 29 stays a gate and line 32 stays `-`-prefixed. `TestIntegrityMakefile`
  pins both; changing either breaks tests that are correct.
- `backfill-lastverified.py` and every `**Last verified:**` date in `evaluations/` — do not
  refresh dates to dodge the cliff. That would assert re-verifications that never happened,
  which `CLAUDE.md` explicitly forbids.
- `STALENESS_DAYS` — do not raise the thresholds. That hides the problem instead of fixing it.

## Git workflow

- Branch: `advisor/012-watchlist-staleness-timebomb`
- Conventional commits, matching `git log` style, e.g.
  `fix(watchlist): stop gating WATCHLIST.md on the time-dependent staleness section`
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Reproduce the failure

Confirm the bug exists before changing anything. Run:

```sh
python3 - <<'PY'
import importlib.util, os, sys, datetime
ROOT = os.getcwd(); sys.path.insert(0, ROOT)
spec = importlib.util.spec_from_file_location("ae", os.path.join(ROOT, "audit-evals.py"))
ae = importlib.util.module_from_spec(spec); spec.loader.exec_module(ae)
ctx = ae.DetectorContext(ROOT)
for off in (0, 79, 95, 98):
    d = datetime.date.today() + datetime.timedelta(days=off)
    stale, undated = ae.audit_staleness(ctx, today=d)
    print(f"+{off}d ({d}): {len(stale)} stale")
PY
```

**Verify**: prints `+0d` with a small number (0 at the time of writing) and `+79d` with a
number in the high 100s (184 at the time of writing). If `+79d` is not dramatically larger
than `+0d`, STOP — the repo's
dates have changed and this plan's premise needs re-checking.

### Step 2: Wrap section 3 in its own marker pair

In `watchlist.py`, add a second marker pair next to the existing one at line 37:

```python
START, END = "<!-- WATCHLIST:START -->", "<!-- WATCHLIST:END -->"
# Section 3 is the one part of this page derived from `datetime.date.today()` rather
# than from file content. It is wrapped in its own markers so `--check` can exclude it
# from the byte comparison: the staleness sweep is REPORT-ONLY (see CLAUDE.md and
# audit_staleness's docstring), and gating on it would turn a calendar date into a red
# CI run with zero commits. `make fix` still refreshes the section.
STALE_START, STALE_END = "<!-- WATCHLIST:STALE:START -->", "<!-- WATCHLIST:STALE:END -->"
```

Then in `render()`, emit `STALE_START` immediately before the `## 3.` heading line and
`STALE_END` immediately after the trailing `_{undated} eval(s) …_` line, so the whole
section (heading, prose, table, and the undated footnote) sits between them.

**Verify**: `python3 watchlist.py && grep -c "WATCHLIST:STALE" WATCHLIST.md` → prints `2`.

### Step 3: Exclude the marked block from the `--check` comparison

Add a helper to `watchlist.py` above `main()`:

```python
def _without_stale_block(text):
    """The page with section 3 elided — the surface `--check` gates on. Section 3 is
    time-derived, so comparing it byte-for-byte would fail the gate on a calendar date
    with zero commits (184 evals cross a threshold on one day). Everything else on the
    page is derived purely from file content and stays gated."""
    if text is None:
        return None
    i, j = text.find(STALE_START), text.find(STALE_END)
    if i == -1 or j == -1:
        return text  # markers absent (e.g. a page written before this change) — gate it whole
    return text[:i] + text[j + len(STALE_END):]
```

In `main()`, change **only** the `--check` branch to compare the elided forms. The apply
branch keeps comparing and writing the full text, so `make fix` still refreshes section 3:

```python
    if check:
        if _without_stale_block(new) != _without_stale_block(current):
            print("watchlist check: DRIFT — WATCHLIST.md is stale; run ./watchlist.py")
            sys.exit(1)
        print("watchlist check: OK — WATCHLIST.md matches the derived watchlist"); sys.exit(0)
```

Do not change the apply branch's `if new != current:` condition.

**Verify**: `python3 watchlist.py --check` → exit 0, prints `watchlist check: OK`.

### Step 4: Correct the stale docstrings

Two docstrings currently assert the old, wrong reasoning. Update both.

In `render()` (`watchlist.py:118-124`), replace the sentence beginning "The one
time-dependent input is section 3's stale *set*…" with an accurate statement: section 3 is
time-derived, is wrapped in `STALE_START`/`STALE_END`, and is excluded from the `--check`
comparison because the sweep is report-only; `make fix` still refreshes it.

In `render()`'s section-3 prose string (`watchlist.py:180-182`), replace
"ages are not printed so the page stays deterministic (`make fix` regenerates when a date
crosses a threshold)" with wording that says this section is a report refreshed by
`make fix` and is not gated — ages are still not printed.

**Verify**: `grep -n "stays deterministic" watchlist.py` → no matches.

### Step 5: Regenerate the page

```sh
python3 watchlist.py && python3 watchlist.py --check
```

**Verify**: both exit 0. `git diff --stat WATCHLIST.md` shows only the two marker lines and
the reworded prose sentence added — no table rows added or removed.

## Test plan

Add to `test_automation.py`, inside the existing `TestWatchlist` class (it already has
`_fixture_tree` and `_run` helpers at roughly lines 2019-2026 — reuse them, do not
duplicate). Model the new tests on `test_check_catches_drift` (roughly lines 2027-2052),
which builds a minimal fixture tree and asserts return codes.

The fixture tree `_fixture_tree` copies `watchlist.py`, `audit-evals.py`, and
`catalog_lib.py`; the test then writes `CATALOG.md`, `COMPARISON.md`, `STACK.md` and
`STACK-LEDGER.md`. For these tests also write an `evaluations/` directory containing one
eval whose `**Last verified:**` date is far in the past (so it is stale) — that is what
makes section 3 non-empty.

Three new tests:

1. **`test_check_ignores_stale_section_drift`** — generate the page, then hand-edit only the
   text *between* `<!-- WATCHLIST:STALE:START -->` and `<!-- WATCHLIST:STALE:END -->`
   (e.g. delete a table row). Assert `--check` still returns 0. This is the regression test
   for the time bomb: it proves a changed stale set cannot fail the gate.
2. **`test_check_still_catches_drift_outside_stale_section`** — corrupt text outside the
   markers (the existing test already does this with `"what to revisit" -> "corrupted"`).
   Assert `--check` returns 1. This proves the fix did not disarm the gate wholesale.
3. **`test_apply_refreshes_stale_section`** — after the hand-edit from test 1, run apply mode
   and assert the deleted row is present again and `--check` returns 0.

**Verify**: `python3 -m unittest -q test_automation` → exit 0, with 3 more tests than before
(compare the count printed before and after your change).

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python3 watchlist.py --check` exits 0
- [ ] `python3 -m unittest -q test_automation` exits 0, and includes the 3 new tests
- [ ] `grep -c "WATCHLIST:STALE" WATCHLIST.md` prints `2`
- [ ] `grep -n "stays deterministic" watchlist.py` returns no matches
- [ ] Simulating the cliff no longer fails the gate. Run:
      `python3 -c "import re;s=open('WATCHLIST.md').read();i=s.find('<!-- WATCHLIST:STALE:START -->');j=s.find('<!-- WATCHLIST:STALE:END -->');open('WATCHLIST.md','w').write(s[:i]+'<!-- WATCHLIST:STALE:START -->\nBOGUS\n'+s[j:])"`
      then `python3 watchlist.py --check` → exit 0; then `python3 watchlist.py` restores the
      file and `git diff --stat WATCHLIST.md` shows no change beyond step 5's.
- [ ] `make check` exits 0 (detector A network failure excepted — see Commands)
- [ ] `git status` shows only `watchlist.py`, `WATCHLIST.md`, `test_automation.py` modified
- [ ] `plans/README.md` status row for 012 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1's reproduction does not show a large jump at +79 days — the premise has drifted.
  (The absolute date, 2026-10-21, is the stable fact; the day offset shrinks as time passes.)
- `watchlist.py`'s `main()` or `render()` no longer matches the excerpts above.
- Excluding the block causes `test_check_catches_drift` (the pre-existing test) to fail —
  that means the elision is too broad and is swallowing gated content.
- You conclude the right fix is to make staleness *gating* instead. That is a policy change
  `CLAUDE.md` explicitly defers ("making staleness itself gating is a later decision") and it
  is out of scope here; report it as a suggestion instead of implementing it.
- The fix appears to require editing `audit-evals.py`, the `Makefile`, or any eval's
  `**Last verified:**` date.

## Maintenance notes

For whoever owns this next:

- **What interacts with this**: any future page section derived from wall-clock time must
  either go inside the `STALE` markers or get markers of its own. The rule is: `--check`
  gates only what is derived from file content.
- **What a reviewer should scrutinize**: that the apply branch still writes the *full* text
  (so `make fix` keeps section 3 fresh), and that the elision markers wrap exactly section 3
  — one line too far in either direction silently un-gates real content.
- **Deliberately deferred**: making the staleness sweep gating, and refreshing the 184 evals
  that will cross their thresholds. Both are real work; both are policy decisions for a
  human. This plan only removes the false-failure mechanism. The underlying signal remains
  visible in `make check`'s `-`-prefixed report trailer and in `WATCHLIST.md` section 3.
- The sibling generator `triage.py` (`NEXT-EVALS.md`) is also `--check`-gated. It reads
  `**Last triaged:**` stamps and `repo-metadata.json`, not `today()`, so it has no equivalent
  cliff — but check for one before adding any date-derived field to it.
