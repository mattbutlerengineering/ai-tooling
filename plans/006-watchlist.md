# Plan 006: Generate WATCHLIST.md — one readable page of everything to revisit or watch

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- COMPARISON.md STACK.md STACK-LEDGER.md audit-evals.py Makefile test_automation.py`
> Plans 002/005 intentionally touch some of these — their changes are
> expected; anything else, re-verify "Current state" first.

## Status

- **Priority**: P2
- **Effort**: M
- **Risk**: LOW
- **Depends on**: plans/005-next-evals-queue.md (shares generator conventions; land 005 first and mirror it)
- **Category**: direction
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

"What should I watch / research next?" currently has no answer surface. The forward-looking signals exist but are scattered: DEFER verdicts live only as COMPARISON rows; "flagged for hands-on before promotion" candidates are buried in prose (`STACK.md:150` names code-on-incus and brooks-lint; `STACK.md` Integrate row names worktrunk "pending a hands-on eval — #188 Gap 4"); staleness and unverified-savings-claims are opt-in script outputs a human never sees; `LEARNING.md` carries "check current standings" notes. A maintainer wanting the watchlist must run four scripts and grep three files. One derived page fixes that.

## Current state

- DEFER rows: `grep -c "| DEFER |" COMPARISON.md` → ~5. The verdict's own definition (`evaluations/TEMPLATE.md:63`): "DEFER = promising but blocked by {reason}, re-evaluate after {trigger}" — each DEFER eval file should contain its re-evaluate trigger.
- Flagged-for-hands-on prose (verified at 4cc412e):
  - `STACK.md:150`: "Two fill genuine gaps and are flagged for a hands-on eval before any promotion — code-on-incus … and brooks-lint".
  - `STACK.md` Integrate row (~line 119): "worktrunk is a candidate pending a hands-on eval — #188 Gap 4".
  - `STACK-LEDGER.md` — machine-readable exclusion ledger; check whether it has a flagged/pending column (`head -20 STACK-LEDGER.md`).
- Script-only signals:
  - `python3 audit-evals.py --staleness` → stale evals + undated count (currently 0 stale / 455 undated).
  - `python3 audit-evals.py --savings-claims` → unverified token-savings headlines (the Optimize-cluster backlog).
  - `python3 audit-evals.py --skills` → ADOPT skills lacking measured backing (currently 3: agent-skills-addyosmani, cc-skills-golang, vercel-labs-agent-skills).
- Generator conventions: established by `tier-stack.py` and (after plan 005) `next-evals.py` — derive, markers, `--check`, Makefile wiring, pinned tests.
- NOT in scope conceptually: first-time evaluation priorities — that's NEXT-EVALS.md (plan 005). WATCHLIST is *revisit* signals: deferred, stale, flagged, unverified-claim, measurement-backlog.

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Generator | `python3 watchlist.py` | writes WATCHLIST.md |
| Check | `python3 watchlist.py --check` | exit 0 when fresh |
| Tests | `python3 -m unittest -q test_automation` | OK |

## Scope

**In scope**:
- `watchlist.py` (create; mirror `next-evals.py`/`tier-stack.py` structure; reuse detector functions from `audit-evals.py` — they take `DetectorContext`, import and call rather than shelling out, if the module structure allows; check how `test_automation.py` imports them for the pattern)
- `WATCHLIST.md` (generated only)
- `Makefile`, `CLAUDE.md` (document), `test_automation.py` (incl. `TestIntegrityMakefile` update)
- `plugin/` via sync; `plans/README.md`

**Out of scope**:
- Changing what any detector computes (consume their outputs as-is)
- The STACK prose asides themselves (they stay; the watchlist aggregates, it doesn't relocate)
- LEARNING.md restructuring

## Steps

### Step 1: Build the generator with four sections

`WATCHLIST.md` sections, each a table with a count in the heading:

1. **Deferred — re-evaluate when trigger fires**: DEFER rows from COMPARISON (via `catalog_lib` parsing) + the trigger sentence extracted from each eval's Verdict section (the text after "re-evaluate after" if present; else "trigger not recorded — add one").
2. **Flagged for hands-on before promotion**: parse `STACK-LEDGER.md` for pending/flagged entries if the ledger encodes them; else hardcode the extraction of the two known STACK prose patterns is NOT acceptable — instead grep STACK.md for the literal phrase `flagged for a hands-on eval` and `pending a hands-on eval` and list the linked tool slugs from those lines (fragile-but-honest; note the fragility in a comment).
3. **Stale / undated evals**: staleness detector output — stale list + the undated count as one line.
4. **Unverified claims & measurement backlog**: savings-claims output + the `--skills` backlog list.

Header states derivation + regenerate command + timestamp-free (no `Date.now` equivalents — derive everything from file content so `--check` is deterministic; the repo's scripts are deterministic by convention).

**Verify**: `python3 watchlist.py` → WATCHLIST.md exists; section 2 lists code-on-incus, brooks-lint, worktrunk; section 4 lists the 3 backlog skills.

### Step 2: --check mode, Makefile, docs, tests

Mirror plan 005 Step 2-3 exactly: `--check` diff mode; `make fix` regenerates, `make check` verifies; CLAUDE.md bullet; `test_automation.py` fixtures (a fixture COMPARISON with 1 DEFER row → section 1 has 1 entry; drift detection) + `TestIntegrityMakefile` update.

**Verify**: `make check` → exit 0; corrupt WATCHLIST.md → `--check` non-zero → regenerate.

### Step 3: Sync decision

Same as plan 005 Step 4 — add WATCHLIST.md to the plugin sync allowlist (ADR-0001) deliberately; it's user-facing.

**Verify**: `./sync-plugin-docs.sh` + `make check` → exit 0.

## Test plan

Fixture-based tests in `test_automation.py` per Step 2; never against real files.

## Done criteria

- [ ] `WATCHLIST.md` has the four sections with counts; known items present (code-on-incus, brooks-lint, worktrunk, 3 backlog skills)
- [ ] `python3 watchlist.py --check` exit 0; drift → non-zero
- [ ] `make fix` / `make check` wired; `TestIntegrityMakefile` green
- [ ] `python3 -m unittest -q test_automation` OK; `make check` exit 0
- [ ] `plans/README.md` updated

## STOP conditions

- Detector functions can't be imported cleanly (module-level side effects) and shelling out (`subprocess` + parse) is the only option — that's acceptable as fallback, but if BOTH are blocked, STOP.
- DEFER trigger extraction hits evals with no Verdict section (malformed) — list them in the output as "trigger not recorded" rather than crashing; if >10 are malformed, STOP and report (data problem, not a script problem).
- The STACK prose-grep in section 2 matches more than ~10 lines — the phrase pattern is too loose; STOP and report the matches.

## Maintenance notes

- Sections 2's prose-grep is deliberately fragile — the durable fix is encoding "flagged" in STACK-LEDGER.md as data (deferred; note it in the ledger's format docs when that happens).
- Plan 007 links WATCHLIST.md from the front door; keep the filename stable.
- When a watch item resolves (eval run, trigger fired), the source data changes and the page regenerates — nobody edits WATCHLIST.md by hand, ever.
