# Plan 008: Activate the staleness sweep — backfill Last-verified dates and gate the field

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- evaluations/ audit-evals.py backfill-evidence.py Makefile test_automation.py CLAUDE.md`
> On unexpected drift, re-verify "Current state" first.

## Status

- **State**: DONE (2026-07-03) — backfilled 455 evals; field gated in `make check`; sweep runs as a report trailer; 0 stale / 0 undated post-backfill.
- **Priority**: P2
- **Effort**: M (S logic + M mechanical backfill across ~455 files)
- **Risk**: LOW
- **Depends on**: none
- **Category**: tech-debt
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The repo's own docs say "A point-in-time eval rots — a harness can be wrong months after it was written" (`CLAUDE.md`, staleness bullet). The staleness sweep exists (`audit-evals.py --staleness`, thresholds in `STALENESS_DAYS` keyed by Type) but is structurally inert: it keys on `**Last verified:**`, which **455 of 487 evals don't have** — those are "reported as a count, not individually." The one mechanism designed to catch eval rot can't see 93% of evals. Fix: backfill the date from git history (an honest floor — the eval was last *true* no later than its last substantive edit), make the field mandatory going forward, and surface the sweep's output in `make check` as a report line.

## Current state

- `evaluations/TEMPLATE.md:5` (verified): `**Last verified:** {YYYY-MM-DD}  <!-- the date you last checked this eval against reality; staleness sweep (audit-evals.py --staleness) flags evals older than their category threshold -->` — present in the template but optional in practice.
- `python3 audit-evals.py --staleness` (verified 2026-07-03): "0 stale eval(s), 455 undated … (455 evals carry no `**Last verified:**` date yet — add one when you re-check them)".
- `STALENESS_DAYS` lives in `audit-evals.py` (grep for it): harnesses/MCP servers/frameworks ~120 days, tools/skills/plugins ~180, references ~365.
- Precedent for "field must exist" gating: `backfill-evidence.py --check` "exits non-zero if any eval lacks a field" — the Evidence field went through exactly this lifecycle (backfilled once, then gated; see `CLAUDE.md`'s backfill-evidence bullet). Model the approach on it, but note: Evidence is *derived* from content; Last-verified is a *date* derived from git.
- Git floor for each eval: `git log -1 --format=%as -- evaluations/<file>.md` (last commit date). This is a floor, not a claim of re-verification — the backfilled line must say so (see Step 1).
- Repo conventions: never edit `plugin/docs/` directly; `make check` gates; pinned tests in `test_automation.py`; conventional commits.

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Staleness | `python3 audit-evals.py --staleness` | report |
| Tests | `python3 -m unittest -q test_automation` | OK |
| Sync | `./sync-plugin-docs.sh` | exit 0 |

## Scope

**In scope**:
- `backfill-lastverified.py` (create — one-shot-able but idempotent backfiller with `--check`, modeled on `backfill-evidence.py`'s structure)
- ~455 files under `evaluations/` (the backfilled header line ONLY — no other content changes)
- `audit-evals.py` (staleness: add a "missing field" finding class; keep the sweep itself report-only but let `--check`-style field-presence gate via the backfiller, exactly like Evidence)
- `Makefile` (backfill `--check` into `check`; apply into `fix`), `CLAUDE.md` (update the staleness bullet), `test_automation.py` (+`TestIntegrityMakefile`)
- `plugin/docs/` via sync; `plans/README.md`

**Out of scope**:
- Making staleness *gating* (a stale eval failing CI) — it stays report-only; only field *presence* becomes gated
- Re-verifying any eval's content (the backfill is a dated floor, not a re-check)
- `evaluations/TEMPLATE.md` (already documents the field)

## Steps

### Step 1: Write backfill-lastverified.py

For each `evaluations/*.md` (excluding TEMPLATE.md) lacking a `**Last verified:**` line: insert `**Last verified:** <git-date>  <!-- backfilled from last git edit; not a hands-on re-check -->` immediately after the `**Stars:**`/header block (match where TEMPLATE.md places it, line 5 — after the Repo/Stars lines, before `**Dev loop stage:**`). Idempotent: files that have the field are untouched, including hand-set values (the never-overwrite rule from `backfill-evidence.py`). `--check` mode: exit non-zero listing files missing the field.

**Verify**: `python3 backfill-lastverified.py --check` → non-zero, ~455 files listed. Then `python3 backfill-lastverified.py` → "backfilled ~455 file(s)"; re-run `--check` → exit 0; spot-check one file (`grep -A1 "Stars" evaluations/beads.md | head -3`) shows the line with the backfill comment.

### Step 2: Surface the sweep and gate the field

- Makefile: `backfill-lastverified.py --check` joins the `check` recipe; apply-mode joins `fix` (position: alongside `backfill-evidence`); update `TestIntegrityMakefile`.
- `audit-evals.py --staleness` output: after backfill it will evaluate real dates — run it and record how many evals are now flagged stale (backfilled dates are old for early evals; expect a real number > 0). Add one line to the `check` target that RUNS `--staleness` but does not fail on stale entries (report-only; e.g. `-python3 audit-evals.py --staleness` with make's `-` prefix, or pipe `|| true` — match how Makefile handles any existing report-only step; if none exists, use the `-` prefix).

**Verify**: `make check` → exit 0 AND the staleness report is visible in its output.

### Step 3: Docs + tests

CLAUDE.md staleness bullet: update to reflect "field is mandatory (gated by backfill-lastverified --check); sweep runs in make check as a report". `test_automation.py`: fixture tests — (a) backfiller inserts after the header block; (b) never overwrites an existing hand-set date; (c) `--check` catches a missing field.

**Verify**: `python3 -m unittest -q test_automation` → OK.

### Step 4: Sync and commit

`./sync-plugin-docs.sh` (the ~455 changed evals sync to plugin/docs), `make check`.

**Verify**: `make check` → exit 0. `git diff --stat` shows evaluations/ + plugin/docs/evaluations/ + the script/Makefile/CLAUDE/test files and nothing else.

## Test plan

Step-3 fixture tests. Plus the end-to-end negative: delete the field from one temp-copied eval fixture → `--check` non-zero.

## Done criteria

- [ ] `python3 audit-evals.py --staleness` reports **0 undated**
- [ ] `python3 backfill-lastverified.py --check` exit 0; removing a field line → non-zero
- [ ] Existing hand-set dates unchanged (`git diff evaluations/token-savings-protocol.md` → empty; it has `**Last verified:** 2026-06-26`)
- [ ] `make check` exit 0 with the staleness report visible
- [ ] `python3 -m unittest -q test_automation` OK; `plans/README.md` updated

## STOP conditions

- More than ~40 evals lack the `**Stars:**`/header anchor the inserter targets — the header shape varies more than planned; report the variant shapes instead of guessing insert points.
- The number of *stale* evals after backfill exceeds ~200 — that's a policy moment (thresholds may be too tight for backfilled floors); report the count and the per-type breakdown, don't tune `STALENESS_DAYS` yourself.
- `backfill-evidence.py`'s structure has diverged from the description here — mirror whatever it currently does.

## Maintenance notes

- The backfilled comment distinguishes floors from real re-checks; when an eval is genuinely re-verified, replace the whole line (date + drop the comment).
- Expect the first honest stale-count to be embarrassing — that's the point; WATCHLIST (plan 006) gives it a home.
- Reviewer: scan a sample of the 455 diffs — the ONLY change per eval file is the one inserted line.
