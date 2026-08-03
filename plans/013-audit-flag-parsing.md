# Plan 013: Make `audit-evals.py` flags compose, and reject typos instead of silently changing the gate set

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat a388dd2..HEAD -- audit-evals.py test_automation.py Makefile`
> If any of those changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: MED
- **Depends on**: none
- **Category**: bug
- **Planned at**: commit `a388dd2`, 2026-08-03

## Why this matters

`audit-evals.py` is the repo's detector engine and the first line of `make check`. Its
argument parsing has two silent failure modes, and both fail *open* — the tool prints
success while running fewer checks than the caller asked for.

1. **`--offline` plus any explicit flag disarms six of seven offline gates.**
   `python3 audit-evals.py --offline` runs 7 detectors (B, D, G, O, Q, J, K).
   `python3 audit-evals.py --offline --verdicts` runs **1** (D). Adding a flag *removed* six
   checks and exited 0. Anyone who edits the `Makefile` line to add a detector will silently
   delete the rest of the gate set, and nothing will tell them.

2. **Unknown flags are silently dropped.** `python3 audit-evals.py --ofline` (one missing
   `f`) does not error. The typo is filtered out, the argument list reads as empty, and the
   script runs the *full default set including the network install resolver* — the opposite
   of what was asked, at ~26 seconds of network cost, with exit 0.

Both were reproduced hands-on against a fixture tree (see Step 1). Neither is caught by any
test: `main()` is 194 statements with **zero** test coverage — `test_automation.py` tests the
detector functions directly and never invokes the CLI. A gate that can be disarmed by a typo,
in the one script CI depends on, is worth a morning.

## Current state

### Files

- `audit-evals.py` — the detector engine; `main()` starts at line 1048.
- `test_automation.py` — the unit suite. Has no CLI-level tests for `audit-evals.py`.
- `Makefile` — line 21 (`python3 audit-evals.py --offline`) and line 31
  (`python3 audit-evals.py --installs`) are the two production call sites.

### The flag matrix — `audit-evals.py:1048-1083`

```python
def main():
    args = sys.argv[1:]
    if "--selftest" in args:
        sys.exit(selftest())
    sel = [a for a in args if a in ("--installs", "--fabrication", "--links", "--archived", "--verdicts", "--comparison", "--drift", "--verdict-evidence", "--rows", "--bulk-triage", "--skills", "--skill-design", "--overlaps", "--workflow-drift", "--clusters", "--savings-claims", "--evidence", "--staleness", "--offline")]
    explicit = [a for a in sel if a != "--offline"]
    do_inst = (not explicit) or "--installs" in sel
    do_fab  = (not explicit) or "--fabrication" in sel or "--offline" in sel
    do_verd = (not explicit) or "--verdicts" in sel  # offline, fast
    do_comp = (not explicit) or "--comparison" in sel or "--offline" in sel  # offline gate
    do_drift = (not explicit) or "--drift" in sel or "--offline" in sel  # offline gate (#70)
    do_vev = (not explicit) or "--verdict-evidence" in sel or "--offline" in sel  # offline gate (#71)
    do_rows = (not explicit) or "--rows" in sel or "--offline" in sel  # offline gate (#198)
    do_bulk = (not explicit) or "--bulk-triage" in sel or "--offline" in sel  # offline gate
    do_links = "--links" in sel   # opt-in: ~450 network requests, slow
    do_archived = "--archived" in sel  # opt-in: ~450 gh-api calls; report-only
    do_skills = "--skills" in sel  # opt-in report (does not affect exit code)
    do_skill_design = "--skill-design" in sel  # opt-in report (does not affect exit code)
    do_overlaps = "--overlaps" in sel  # opt-in report (does not affect exit code)
    do_wf_drift = "--workflow-drift" in sel  # opt-in report (does not affect exit code)
    do_clusters = "--clusters" in sel  # opt-in report (does not affect exit code)
    do_savings = "--savings-claims" in sel  # opt-in report (does not affect exit code)
    do_evidence = "--evidence" in sel  # opt-in report (does not affect exit code)
    do_staleness = "--staleness" in sel  # opt-in report (does not affect exit code)
    if "--offline" in sel: do_inst = False
    if explicit:
        do_inst = "--installs" in sel
        do_fab  = "--fabrication" in sel
        do_verd = "--verdicts" in sel
        do_comp = "--comparison" in sel
        do_drift = "--drift" in sel
        do_vev = "--verdict-evidence" in sel
        do_rows = "--rows" in sel
        do_bulk = "--bulk-triage" in sel
```

**The bug in bug 1** is the `if explicit:` block at the bottom. The lines above it correctly
include `or "--offline" in sel`; the overwrite block drops that clause, so any explicit flag
alongside `--offline` resets the other seven to bare membership tests.

**The bug in bug 2** is `sel`'s membership filter: an argument that is not in the tuple is
discarded rather than rejected, so `explicit` reads as empty and every default turns on.

### Behavior to preserve exactly

Verified by running the script in a fixture tree at `a388dd2`:

| Invocation | Detectors that run today | Must still run after this change |
|---|---|---|
| (no args) | A, B, D, G, O, Q, J, K | same |
| `--offline` | B, D, G, O, Q, J, K (no A) | same |
| `--installs` | A only | same |
| `--verdicts` | D only | same |
| `--links` | C only | same |
| `--offline --verdicts` | **D only (bug)** | B, D, G, O, Q, J, K |
| `--ofline` (typo) | **A, B, D, G, O, Q, J, K (bug)** | exit 2, error message |

The default set is "detector A plus the seven offline gates". The opt-in reports
(`--links`, `--archived`, `--skills`, `--skill-design`, `--overlaps`, `--workflow-drift`,
`--clusters`, `--savings-claims`, `--evidence`, `--staleness`) are never in the default set
and never affect the exit code — that stays true.

### `--selftest`

`--selftest` is handled *before* `sel` is computed and exits immediately. It is not in the
`sel` tuple. Keep that early-exit shape; just make sure the new unknown-flag check does not
reject `--selftest`.

### Repo conventions that apply

- Python 3, **stdlib only** — do not introduce `argparse`. The dispatch below the flag matrix
  is a long series of `if do_X:` blocks that read the booleans; keep producing those same
  boolean names so the rest of `main()` is untouched.
- No type annotations anywhere in this codebase. Match that.
- Comments explain *why*. The existing per-flag comments (`# offline gate (#70)`,
  `# opt-in report (does not affect exit code)`) carry real information — preserve it.
- Tests go in `test_automation.py` against fixtures in a temp dir, never the real files.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Offline gates | `python3 audit-evals.py --offline` | exit 0, prints 7 detector headers |
| Selftest | `python3 audit-evals.py --selftest` | exit 0, prints `OK — … cases pass` |
| Unit suite | `python3 -m unittest -q test_automation` | exit 0 |
| Full gate | `make check` | exit 0 (detector A needs network + `gh` auth) |

## Scope

**In scope** (the only files you should modify):

- `audit-evals.py` — `main()`'s flag-parsing block only (lines 1048-1083 and the module-level
  constants you add above `main()`).
- `test_automation.py` — add a new test class.

**Out of scope** (do NOT touch, even though they look related):

- Every `audit_*` detector function. This plan changes *which* detectors run, never *what*
  any of them does. If you find a detector bug, report it; do not fix it here.
- The `if do_X:` dispatch blocks below the flag matrix in `main()`. They already read the
  booleans correctly. Rewriting them turns a small diff into an unreviewable one.
- `Makefile` — its two call sites (`--offline`, `--installs`) are already correct and their
  behavior is unchanged by this plan. `TestIntegrityMakefile` pins those exact strings.
- `.github/workflows/integrity.yml` — it calls `make check`; nothing to change.
- Adding new flags, renaming existing ones, or adding a `--help`. Out of scope.

## Git workflow

- Branch: `advisor/013-audit-flag-parsing`
- Conventional commits, e.g.
  `fix(audit): make --offline compose with explicit flags and reject unknown args`
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Reproduce both bugs in a throwaway fixture tree

Build the fixture outside the repo so nothing is mutated:

```sh
D=$(mktemp -d) && mkdir -p "$D/evaluations"
cp audit-evals.py catalog_lib.py "$D/"
printf '## Plan\n\n| Name | Type | One-liner | Problem | Overlaps with |\n|------|------|-----------|---------|---------------|\n' > "$D/CATALOG.md"
printf '# Tool Comparison\n\n## Plan\n\n| Tool | Type | Auto | Free | Evaluated | Evidence |\n|------|------|------|------|-----------|----------|\n' > "$D/COMPARISON.md"
printf '# Stack\n' > "$D/STACK.md"
printf '# Workflow\n' > "$D/WORKFLOW.md"
printf '# Stack Ledger\n' > "$D/STACK-LEDGER.md"
echo "$D"
( cd "$D" && echo "--- offline:"        && python3 audit-evals.py --offline | grep -c '^== ' )
( cd "$D" && echo "--- offline+verdicts:" && python3 audit-evals.py --offline --verdicts | grep -c '^== ' )
```

**Verify**: the first count is `7`, the second is `1`. That is bug 1. Then:

```sh
( cd "$D" && python3 audit-evals.py --ofline | head -2; echo "rc=$?" )
```

**Verify**: it prints `== A. install resolver ==` (the network detector) and does not error.
That is bug 2. Keep `$D` — the same tree is what the new tests will build.

If either reproduction does not match, STOP.

### Step 2: Add the flag constants above `main()`

Insert immediately above `def main():` in `audit-evals.py`:

```python
# ---------------------------------------------------------------- CLI flag sets
# The seven offline gates `--offline` selects. Keep in lockstep with the Makefile's
# `audit-evals.py --offline` line and with CLAUDE.md's list of gating detectors.
OFFLINE_GATES = ("--fabrication", "--verdicts", "--comparison", "--drift",
                 "--verdict-evidence", "--rows", "--bulk-triage")
# With no flags at all: the offline gates plus the network install resolver.
DEFAULT_GATES = OFFLINE_GATES + ("--installs",)
# Opt-in reports. Never in the default set; never affect the exit code.
REPORT_FLAGS = ("--links", "--archived", "--skills", "--skill-design", "--overlaps",
                "--workflow-drift", "--clusters", "--savings-claims", "--evidence",
                "--staleness")
DETECTOR_FLAGS = DEFAULT_GATES + REPORT_FLAGS
# Every argument main() accepts. An argument outside this set is a typo, and a typo
# used to be silently dropped — which turned `--ofline` into "run everything including
# the 26s network resolver" and still exited 0. Fail loudly instead.
KNOWN_FLAGS = DETECTOR_FLAGS + ("--offline", "--selftest")
```

**Verify**: `python3 -c "import importlib.util,os;s=importlib.util.spec_from_file_location('ae','audit-evals.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print(len(m.KNOWN_FLAGS))"`
→ prints `19`.

### Step 3: Replace the flag matrix with a union

Replace everything from `sel = [a for a in args …]` through the closing of the
`if explicit:` block (lines 1052-1083) with:

```python
    unknown = [a for a in args if a not in KNOWN_FLAGS]
    if unknown:
        print(f"audit-evals: unknown argument(s): {' '.join(unknown)}", file=sys.stderr)
        print(f"  known: {' '.join(sorted(KNOWN_FLAGS))}", file=sys.stderr)
        sys.exit(2)

    # Requested detectors are a UNION, so a flag can only ever ADD work. The old matrix
    # let `--offline --verdicts` run 1 detector where `--offline` alone ran 7 — adding a
    # flag silently deleted six gates and still exited 0.
    sel = set(a for a in args if a in DETECTOR_FLAGS or a == "--offline")
    want = set()
    if "--offline" in sel:
        want |= set(OFFLINE_GATES)
    want |= (sel - {"--offline"})
    if not want:
        want = set(DEFAULT_GATES)

    do_inst = "--installs" in want
    do_fab  = "--fabrication" in want
    do_verd = "--verdicts" in want          # offline, fast
    do_comp = "--comparison" in want        # offline gate
    do_drift = "--drift" in want            # offline gate (#70)
    do_vev = "--verdict-evidence" in want   # offline gate (#71)
    do_rows = "--rows" in want              # offline gate (#198)
    do_bulk = "--bulk-triage" in want       # offline gate
    do_links = "--links" in want            # opt-in: ~450 network requests, slow
    do_archived = "--archived" in want      # opt-in: ~450 gh-api calls; report-only
    do_skills = "--skills" in want          # opt-in report (does not affect exit code)
    do_skill_design = "--skill-design" in want   # opt-in report (does not affect exit code)
    do_overlaps = "--overlaps" in want      # opt-in report (does not affect exit code)
    do_wf_drift = "--workflow-drift" in want     # opt-in report (does not affect exit code)
    do_clusters = "--clusters" in want      # opt-in report (does not affect exit code)
    do_savings = "--savings-claims" in want # opt-in report (does not affect exit code)
    do_evidence = "--evidence" in want      # opt-in report (does not affect exit code)
    do_staleness = "--staleness" in want    # opt-in report (does not affect exit code)
```

Leave `args = sys.argv[1:]` and the `--selftest` early exit above it exactly as they are, and
leave everything below (`ctx = DetectorContext(ROOT)` onward) untouched.

**Verify**: `python3 audit-evals.py --selftest` → exit 0. Then, in the `$D` fixture tree from
step 1 (re-copy the edited `audit-evals.py` into it first):

```sh
cp audit-evals.py "$D/" && ( cd "$D" && python3 audit-evals.py --offline --verdicts | grep -c '^== ' )
```

→ prints `7`.

### Step 4: Confirm the whole behavior table

Re-copy the edited script into `$D` and check every row of the table in "Current state":

```sh
cp audit-evals.py "$D/"
cd "$D"
for f in "" "--offline" "--installs" "--verdicts" "--offline --verdicts"; do
  echo "[$f] -> $(python3 audit-evals.py $f 2>/dev/null | grep -c '^== ')"
done
python3 audit-evals.py --ofline; echo "typo rc=$?"
```

**Verify**: counts are `8`, `7`, `1`, `1`, `7` respectively, and the typo prints an error to
stderr with `typo rc=2`.

(The no-args and `--installs` cases hit the network; if that is unavailable in your
environment they may fail on the *resolution* rather than the flag parsing — a non-zero exit
with `== A. install resolver ==` in the output still confirms A was selected.)

### Step 5: Clean up the fixture tree

`rm -rf "$D"`.

## Test plan

Add a new class `TestAuditEvalsCLI` to `test_automation.py`, placed next to the other
subprocess-based classes. Model its structure on `TestWatchlist`'s `_fixture_tree` / `_run`
pair (roughly lines 2019-2026) — copy the pattern, do not import it.

The fixture tree copies `audit-evals.py` and `catalog_lib.py` and writes the five markdown
files from Step 1 plus an empty `evaluations/` directory (verified sufficient: the offline
detectors all pass on it).

Tests (all offline — **none may invoke `--installs` or the no-args default**, which hit the
network and would make the suite flaky):

1. **`test_offline_runs_all_seven_gates`** — `--offline` output contains exactly 7 lines
   starting with `== `, and includes the `B.`, `D.`, `G.`, `O.`, `Q.`, `J.`, `K.` headers.
2. **`test_offline_composes_with_explicit_flag`** — the regression test for bug 1.
   `--offline --verdicts` produces the same 7 headers as `--offline` alone. Assert set
   equality of the header lines, not just the count.
3. **`test_single_flag_runs_only_that_detector`** — `--verdicts` alone produces exactly 1
   header, containing `D.`. Pins that this plan did not turn every flag into "run everything".
4. **`test_unknown_flag_exits_2`** — the regression test for bug 2. `--ofline` returns 2, and
   stderr contains `unknown argument`.
5. **`test_unknown_flag_does_not_run_detectors`** — the same invocation produces no `== `
   header on stdout. (Exiting 2 *after* running the network resolver would still be a bug.)
6. **`test_selftest_still_works`** — `--selftest` returns 0 and is not rejected by the
   unknown-flag check.
7. **`test_report_flag_does_not_affect_exit_code`** — `--staleness` returns 0 on the fixture
   tree, confirming opt-in reports stayed non-gating.

**Verify**: `python3 -m unittest -q test_automation` → exit 0, 7 more tests than before.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python3 audit-evals.py --selftest` exits 0
- [ ] `python3 audit-evals.py --offline` exits 0 and prints 7 lines matching `^== `
- [ ] `python3 audit-evals.py --offline --verdicts` prints the **same 7** headers
      (`diff <(python3 audit-evals.py --offline | grep '^== ' | sort) <(python3 audit-evals.py --offline --verdicts | grep '^== ' | sort)` → no output)
- [ ] `python3 audit-evals.py --ofline; echo $?` prints `2` and no `== ` header
- [ ] `python3 -m unittest -q test_automation` exits 0 with the 7 new tests
- [ ] `make check` exits 0 (detector A network failure excepted)
- [ ] `git status` shows only `audit-evals.py` and `test_automation.py` modified
- [ ] `git diff --stat audit-evals.py` shows changes confined to the region above and inside
      `main()`'s flag block — no detector function touched
- [ ] `plans/README.md` status row for 013 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1's reproduction does not show `7` then `1` — the bug has already been fixed or the
  code has drifted, and this plan's diff would be wrong.
- After step 3, `python3 audit-evals.py --offline` runs a *different* number of detectors than
  7, or a different set. That means `OFFLINE_GATES` does not match the old matrix and you
  must reconcile before continuing — do not "fix" it by adding whatever makes the count match.
- Any pre-existing test in `test_automation.py` starts failing. Nothing in this plan should
  affect the detector functions those tests cover.
- You find a flag referenced somewhere in the repo (a hook, a doc, a workflow) that is not in
  `KNOWN_FLAGS`. Adding it to the tuple is correct — but check first that it is a real flag
  and not a doc typo, and say which you found. Run:
  `grep -rn "audit-evals.py " --include=*.md --include=*.sh --include=*.yml --include=Makefile . | grep -v '^./plans/'`
- The unknown-flag rejection breaks a caller you did not expect (for example a hook passing a
  file path as a positional argument). If any call site passes a non-flag argument, STOP —
  the check needs to allow positionals and this plan assumed there are none.

## Maintenance notes

For whoever owns this next:

- **The lockstep to watch**: `OFFLINE_GATES` now encodes "what `--offline` means" in one
  place. A new gating detector must be added there *and* to `CLAUDE.md`'s gating list *and*
  to `TestIntegrityMakefile.GATES` if it gets its own `make check` line. A new *report* goes
  in `REPORT_FLAGS` only.
- **What a reviewer should scrutinize**: that `want` is genuinely a union (a flag can only
  add), and that the 18 `do_*` names and their order match the old block exactly — the
  dispatch below reads them by name, and a typo there disables a detector silently, which is
  precisely the class of bug this plan exists to kill.
- **Deliberately deferred**: migrating to `argparse` (would give `--help` and typo rejection
  for free, but rewrites the whole block and the repo is deliberately stdlib-minimal — this
  is the smaller change that fixes the actual bugs), and adding CLI tests for the other
  generators (`triage.py`, `watchlist.py`, `tier-stack.py` all parse `--check` with a bare
  `in sys.argv` and share the same typo-tolerance, though none of them fails *open* the way
  this one did).
- **Coverage note**: `main()` had zero test coverage before this plan. The seven tests cover
  flag selection only — the dispatch bodies and the exit-code aggregation below them remain
  uncovered. That is the natural follow-up.
