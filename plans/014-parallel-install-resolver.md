# Plan 014: Cut `make check` from ~34s to under 15s by resolving installs in parallel

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving to the
> next step. If anything in the "STOP conditions" section occurs, stop and
> report — do not improvise. When done, update the status row for this plan
> in `plans/README.md`.
>
> **Drift check (run first)**:
> `git diff --stat a388dd2..HEAD -- audit-evals.py Makefile test_automation.py`
> If any of those changed since this plan was written, compare the
> "Current state" excerpts against the live code before proceeding; on a
> mismatch, treat it as a STOP condition.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none (can run in parallel with 012, 013, 015 — different regions of
  different files; if 013 lands first, `main()` will look different but this plan does not
  touch `main()`)
- **Category**: perf
- **Planned at**: commit `a388dd2`, 2026-08-03

## Why this matters

`make check` is the gate every commit, every PR, every CI run, and every unattended routine
passes through. Measured at `a388dd2` on this repo:

- `make check` end to end: **33.6s**
- `python3 audit-evals.py --installs` (detector A) alone: **25.7s** — **76% of the total**

Detector A resolves **86 unique install targets** (52 npm, 26 PyPI, 6 GitHub, 2 crates)
strictly one at a time. Each npm check spawns a `npm view` subprocess; each PyPI/crates check
is a serial HTTP round trip. There is no dependency between any two lookups. The sibling
detector C (`audit_links`) already solves exactly this problem with a 24-worker
`ThreadPoolExecutor` for ~450 requests — detector A just never got the same treatment.

Two consequences beyond wall-clock: the slow gate discourages running `make check` locally
before pushing, and the resolver's subprocess calls have **no timeout**, so a hung `npm` or
`gh` process blocks the entire gate indefinitely with no diagnostic.

This plan parallelizes detector A, adds timeouts, and adds a `make check-offline` target for
the common case where you only want the offline gates.

## Current state

### Files

- `audit-evals.py` — detector A lives at lines 186-200; the parallel exemplar (detector C) at
  lines 253-261; the network helpers at lines 133-148.
- `Makefile` — `check` at lines 20-32; `audit-evals.py --installs` is line 31.
- `test_automation.py` — the unit suite; `TestIntegrityMakefile` (roughly lines 1603-1675)
  pins the `make check` gate set.

### Detector A today — `audit-evals.py:186-200`

```python
def audit_installs(ctx):
    files = ["STACK.md", "CATALOG.md"] + sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))
    seen, broken = {}, []
    checkers = {"pypi": pypi_exists, "crates": crates_exists, "npm": npm_exists, "gh": gh_repo_exists}
    for rel in files:
        if not os.path.exists(ctx.path(rel)): continue
        for kind, pkg in extract_installs(ctx.read(rel)):
            key = (kind, pkg)
            if key in seen:
                ok = seen[key]
            else:
                ok = checkers[kind](pkg); seen[key] = ok
            if not ok:
                broken.append((rel, kind, pkg))
    return broken
```

Note the shape: it already dedupes via `seen`, and it reports **per file occurrence** — one
`(rel, kind, pkg)` tuple per mention, so a broken package cited in three evals produces three
findings. **That output shape must not change.**

### The exemplar to copy — `audit-evals.py:253-261`

```python
def audit_links(ctx):
    import concurrent.futures
    slugs = catalog_lib.github_repos(ctx.catalog)
    problems = []
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        for slug, res in zip(slugs, ex.map(check_repo, slugs)):
            if res != "ok":
                problems.append((slug, res))
    return problems, len(slugs)
```

Note `import concurrent.futures` is **function-local** here. Match that — the module's
top-level import line is already long and this keeps the cost off every offline run.

### The network helpers — `audit-evals.py:133-148`

```python
def http_ok(url):
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "ai-tooling-audit"})
        with urllib.request.urlopen(req, timeout=TIMEOUT) as r:
            return r.status == 200
    except Exception:
        return False

def npm_exists(pkg):
    return subprocess.run(["npm", "view", pkg, "version"],
                          capture_output=True, text=True).returncode == 0

def gh_repo_exists(slug):
    return subprocess.run(["gh", "api", f"repos/{slug}", "--jq", ".full_name"],
                          capture_output=True, text=True).returncode == 0

def pypi_exists(pkg):   return http_ok(f"https://pypi.org/pypi/{pkg}/json")
def crates_exists(pkg): return http_ok(f"https://crates.io/api/v1/crates/{pkg}")
```

`TIMEOUT = 15` is defined at `audit-evals.py:123` and used by `http_ok` only. The two
`subprocess.run` calls pass **no `timeout=`** and do not handle `FileNotFoundError` (raised
when `npm` or `gh` is not installed — an uncaught traceback rather than a clear message).

### The Makefile — lines 18-32

```make
.PHONY: check fix

check:
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	python3 audit-evals.py --installs
	-python3 audit-evals.py --staleness
```

### Repo conventions that apply

- Python 3, **stdlib only**. `concurrent.futures` is stdlib — fine. No `asyncio`, no `httpx`,
  no `requests`.
- No type annotations. Match the surrounding code.
- The `Makefile` header (lines 8-10) says: "Keep this target in lockstep with the gate set: a
  gate added to integrity.yml must be added here (and test_automation.py's
  `TestIntegrityMakefile` pins that they stay in sync)." A **new target** is fine; removing or
  reordering a line in `check` is not.
- `CLAUDE.md` describes `--installs` as the network resolver and `--offline` as the offline
  set — this plan keeps that split and makes it directly runnable.

## Commands you will need

| Purpose | Command | Expected on success |
|---------|---------|---------------------|
| Detector A alone | `python3 audit-evals.py --installs` | exit 0, `OK — all checked install targets resolve` |
| Time it | `/usr/bin/time -p python3 audit-evals.py --installs` | see Step 4 |
| Offline gates | `python3 audit-evals.py --offline` | exit 0 |
| Unit suite | `python3 -m unittest -q test_automation` | exit 0 |
| Full gate | `make check` | exit 0 |
| New target | `make check-offline` | exit 0 (after Step 5) |

Detector A requires network access and `gh` auth. If neither is available in your
environment, STOP — this plan cannot be verified without them.

## Scope

**In scope** (the only files you should modify):

- `audit-evals.py` — `audit_installs`, `npm_exists`, `gh_repo_exists` only.
- `Makefile` — add one new target; do not modify `check` or `fix`.
- `test_automation.py` — add tests for the new target and for `audit_installs`' output shape.

**Out of scope** (do NOT touch, even though they look related):

- `extract_installs`, `PKG_CLEAN`, `PLACEHOLDER`, `NEGATION` — the *parsing* is correct and
  is a separate concern from the *resolving*. Changing a regex here silently changes which
  install commands get checked, which is a correctness change disguised as a perf change.
- The `check` target's existing lines, their order, or the `-` prefix on the staleness line.
  `TestIntegrityMakefile` pins all of it and those pins are correct.
- `.github/workflows/integrity.yml` — it calls `make check`, which is unchanged.
- `audit_links` / `check_archived` — already parallel or already opt-in; leave them.
- Caching resolver results to disk. Tempting, and a real speedup, but it introduces a
  staleness question (when does a cached "resolves" expire?) that needs a decision this plan
  does not have. Note it as a follow-up instead.

## Git workflow

- Branch: `advisor/014-parallel-install-resolver`
- Conventional commits, e.g. `perf(audit): resolve install targets in parallel`
- Do NOT push or open a PR unless the operator instructed it.

## Steps

### Step 1: Record the baseline

```sh
/usr/bin/time -p python3 audit-evals.py --installs 2>&1 | tail -4
/usr/bin/time -p make check 2>&1 | tail -4
```

Write both `real` numbers down — you will compare against them in Step 4.

**Verify**: both exit 0. `--installs` should be in the 15-40s range. If it is already under
5s, STOP — either the network is unusually fast or someone already fixed this, and the plan's
premise needs re-checking.

### Step 2: Add timeouts and missing-binary handling to the subprocess checkers

Replace `npm_exists` and `gh_repo_exists` with:

```python
def _run_ok(cmd):
    """True if `cmd` exits 0. A missing binary or a hung process is 'cannot verify', not
    'broken' — detector A gates CI, so a false BROKEN is worse than an unchecked target.
    Without the timeout a single wedged `npm view` blocks the whole gate indefinitely."""
    try:
        return subprocess.run(cmd, capture_output=True, text=True,
                              timeout=TIMEOUT).returncode == 0
    except (subprocess.TimeoutExpired, FileNotFoundError):
        return True

def npm_exists(pkg):
    return _run_ok(["npm", "view", pkg, "version"])

def gh_repo_exists(slug):
    return _run_ok(["gh", "api", f"repos/{slug}", "--jq", ".full_name"])
```

Returning `True` on timeout/missing-binary is deliberate and is a **behavior change**: today
a missing `npm` raises `FileNotFoundError` and crashes the run. Failing open here matches
`http_ok`'s intent (it swallows exceptions, but returns `False` — see the STOP condition
about that asymmetry) for the *specific* case of "the checker itself could not run". A real
404 still returns non-zero and is still reported BROKEN.

**Verify**: `python3 audit-evals.py --installs` → exit 0, same output as Step 1.

### Step 3: Parallelize `audit_installs`

Replace `audit_installs` with a two-pass version: collect every mention first, resolve the
unique targets concurrently, then map results back to mentions. This preserves the exact
output shape (one tuple per file occurrence, in file order).

```python
def audit_installs(ctx):
    """Detector A: every install command must point at a real artifact. Resolution is
    concurrent (86 unique targets, ~26s serial → a few seconds) — each lookup is
    independent, so this mirrors audit_links' ThreadPoolExecutor. Mentions are collected
    first so the reported order and per-occurrence shape are unchanged: a broken package
    cited in three evals is still three findings."""
    import concurrent.futures
    files = ["STACK.md", "CATALOG.md"] + sorted(glob.glob("evaluations/*.md", root_dir=ctx.root))
    checkers = {"pypi": pypi_exists, "crates": crates_exists, "npm": npm_exists, "gh": gh_repo_exists}
    mentions = []  # (rel, kind, pkg), in file order — the reported order
    for rel in files:
        if not os.path.exists(ctx.path(rel)):
            continue
        for kind, pkg in extract_installs(ctx.read(rel)):
            mentions.append((rel, kind, pkg))
    targets = sorted({(kind, pkg) for _rel, kind, pkg in mentions})
    with concurrent.futures.ThreadPoolExecutor(max_workers=24) as ex:
        results = ex.map(lambda t: checkers[t[0]](t[1]), targets)
        seen = dict(zip(targets, results))
    return [(rel, kind, pkg) for rel, kind, pkg in mentions if not seen[(kind, pkg)]]
```

`max_workers=24` matches `audit_links`. Do not raise it — PyPI and the npm registry rate-limit,
and a 429 would be reported as BROKEN.

**Verify**: `python3 audit-evals.py --installs` → exit 0 and **byte-identical output** to
Step 1. Confirm mechanically:

```sh
python3 audit-evals.py --installs > /tmp/a-after.txt 2>&1
git stash && python3 audit-evals.py --installs > /tmp/a-before.txt 2>&1 && git stash pop
diff /tmp/a-before.txt /tmp/a-after.txt
```

→ no output.

**If your environment forbids `git stash`** (it rewrites the working tree and other agents may
be sharing it), skip the stash and instead compare against the output you captured in Step 1
by eye — the "OK" line and any BROKEN lines must match exactly.

### Step 4: Measure the improvement

```sh
/usr/bin/time -p python3 audit-evals.py --installs 2>&1 | tail -4
/usr/bin/time -p make check 2>&1 | tail -4
```

**Verify**: `--installs` `real` is at most **half** the Step 1 baseline. If it is not, STOP
and report the numbers — either the bottleneck is not what this plan assumed, or the executor
is not actually running concurrently.

### Step 5: Add a `check-offline` target

Append to the `Makefile` (do not modify `check` or `fix`):

```make
# Everything in `check` except the network install resolver (A) — the fast local loop.
# `check` remains the canonical gate; this is for iterating without paying ~26s of
# network round trips on every run. CI always runs the full `check`.
check-offline:
	python3 audit-evals.py --offline
	python3 audit-evals.py --selftest
	python3 -m unittest -q test_automation
	python3 reconcile-counts.py --check
	python3 backfill-evidence.py --check
	python3 backfill-lastverified.py --check
	python3 tier-stack.py --check
	python3 triage.py --check
	python3 watchlist.py --check
	./sync-plugin-docs.sh --check
	-python3 audit-evals.py --staleness
```

Add `check-offline` to the `.PHONY` line (line 18), and add a line to the Makefile's header
comment block naming it and saying it is **not** the canonical gate.

**Verify**: `make check-offline` → exit 0, noticeably faster than `make check`, and its output
contains no `== A. install resolver ==` line.

## Test plan

Add to `test_automation.py`:

1. In `TestIntegrityMakefile`, add **`test_check_offline_omits_installs`** — parse the
   `check-offline:` target body the same way `_check_target_body` parses `check:` (generalize
   that helper to take a target name, or add a sibling; either is fine). Assert:
   - it does **not** contain `audit-evals.py --installs`
   - it contains every other entry of `GATES` except `audit-evals.py --installs`
   - `check:` itself still contains all of `GATES` (the existing
     `test_check_target_runs_every_gate` covers this — confirm it still passes)

2. A new **`TestInstallResolver`** class pinning `audit_installs`' output shape without any
   network access. Build a `DetectorContext` over a temp dir (the `#199` context seam — see
   how `TestWatchlist` and the other context-based tests do it) containing a `CATALOG.md`
   with the same fake package cited in two different files, monkeypatch the module's
   `pypi_exists` to a function returning `False`, and assert:
   - **`test_reports_every_occurrence`** — a broken package mentioned in two files yields
     **two** tuples, not one (this is the dedupe-vs-report distinction the rewrite must
     preserve).
   - **`test_resolves_each_unique_target_once`** — wrap the fake checker in a counter and
     assert it was called exactly once for a package mentioned twice.
   - **`test_ok_target_is_not_reported`** — a checker returning `True` yields an empty list.

   Restore the monkeypatched function in `tearDown` (or use `unittest.mock.patch.object`) so
   later tests are unaffected.

**Verify**: `python3 -m unittest -q test_automation` → exit 0, 4 more tests than before.

## Done criteria

Machine-checkable. ALL must hold:

- [ ] `python3 audit-evals.py --installs` exits 0 with output identical to the Step 1 baseline
- [ ] `/usr/bin/time -p python3 audit-evals.py --installs` `real` ≤ half the Step 1 baseline
- [ ] `make check` exits 0
- [ ] `make check-offline` exits 0 and its output contains no `== A. install resolver ==`
- [ ] `grep -n "check-offline" Makefile` shows it in both `.PHONY` and as a target
- [ ] `python3 -m unittest -q test_automation` exits 0 with the 4 new tests
- [ ] `git diff Makefile` shows **no change** to the `check:` or `fix:` recipe bodies
- [ ] `git status` shows only `audit-evals.py`, `Makefile`, `test_automation.py` modified
- [ ] `plans/README.md` status row for 014 updated

## STOP conditions

Stop and report back (do not improvise) if:

- Step 1 shows `--installs` already under 5s — the premise has drifted.
- Step 3's output differs from the baseline in *any* way other than ordering. Different
  findings means the rewrite changed detection, not just speed. Do not "fix" the baseline.
- Step 4 shows less than a 2× improvement.
- `--installs` starts reporting BROKEN targets it did not report before. That is most likely
  registry rate-limiting from the concurrency, not real breakage. Lower `max_workers` to 8,
  re-measure, and report what you found — do not accept the new BROKEN list as truth.
- You notice that `_run_ok` failing open (returning `True` on timeout) is inconsistent with
  `http_ok` failing closed (returning `False` on any exception, including a network timeout,
  which reports a real package as BROKEN when the network is down). That inconsistency is
  **real and pre-existing**. Report it; do not fix it here — changing `http_ok` changes what
  the gate reports on a flaky network, which is a policy decision for a human.
- Any pre-existing test in `test_automation.py` fails.

## Maintenance notes

For whoever owns this next:

- **What interacts with this**: `max_workers=24` is now duplicated in `audit_installs` and
  `audit_links`. If registry rate-limiting ever becomes a problem, both need the same
  treatment — consider hoisting it to a module constant at that point, not before.
- **What a reviewer should scrutinize**: that the per-occurrence output shape survived (a
  package cited in N files still produces N findings) and that `check:` in the Makefile is
  byte-identical to before. The whole risk of this plan is a silent detection change hiding
  inside a perf change.
- **Deliberately deferred**:
  - *Caching resolver results* between runs. Biggest remaining win (it would make the gate
    near-instant on unchanged files) but needs a TTL policy decision.
  - *Reconciling `http_ok`'s fail-closed with `_run_ok`'s fail-open.* See the STOP condition.
  - *Making `check-offline` the pre-commit hook's gate.* `.claude/hooks/audit-gate.sh`
    currently runs `audit-evals.py --offline` directly; pointing it at `make check-offline`
    would broaden what a commit is gated on, which is a scope decision, not a cleanup.
