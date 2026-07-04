# Plan 003: Reconcile WORKFLOW.md with STACK.md and add a drift report so they can't silently diverge

> **Executor instructions**: Follow this plan step by step. Run every
> verification command and confirm the expected result before moving on.
> On any STOP condition, stop and report. When done, update this plan's
> status row in `plans/README.md`.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- WORKFLOW.md STACK.md audit-evals.py Makefile test_automation.py`
> On drift, re-verify the "Current state" excerpts before proceeding.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: none (textual overlap with 001/002 is in different files/sections)
- **Category**: docs
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

`README.md:55` sends readers to WORKFLOW.md as "the full operating manual," and STACK.md is the install list. They disagree: STACK's Plan-stage picks are context7, GSD, feature-dev, github-mcp-server, codegraph, **markitdown**; WORKFLOW's Plan stage lists graphify, codegraph, context7, codebase-design, domain-modeling, github-mcp-server — `markitdown` (a Tier-1 MEASURED pick) appears **zero** times in all of WORKFLOW.md. A newcomer gets two different answers to "what do I use for planning." Detector J gates STACK against the verdict data, but nothing gates WORKFLOW against STACK. This plan (a) reconciles today's drift by hand, (b) adds a *report-only* cross-reference check so future drift is a visible number.

## Current state

- `STACK.md` Plan section (lines ~44-51, verified): table rows for context7, GSD, feature-dev, github-mcp-server, codegraph, markitdown — each with install command and Signal column.
- `WORKFLOW.md` Plan stage (lines ~38-52, verified): three-layer table (Process/Tooling/Infrastructure) listing graphify, codegraph, context7, codebase-design, domain-modeling, github-mcp-server. GSD, feature-dev, markitdown absent from this stage. `grep -c "markitdown" WORKFLOW.md` → **0**.
- Note the docs have *different jobs*: WORKFLOW maps options per stage (including non-STACK CONDITIONAL tools like graphify — fine); STACK is the curated picks. The invariant to enforce is one-directional: **every STACK tool must appear in WORKFLOW at some stage** (the manual must at least mention every pick). The reverse is NOT required.
- Existing detector pattern to model after: detector J (`audit_stack_drift(ctx)` at `audit-evals.py:360`) — offline, reads two files, emits findings. Report-only detectors follow the pattern of `--overlaps`/`--staleness` (opt-in flags, listed in `CLAUDE.md`'s detector table).
- Detectors take inputs via `DetectorContext`, not global ROOT (commit `7db411a`); characterization tests live in `test_automation.py`.
- Tool identity: STACK rows link `[name](https://github.com/owner/repo)`; WORKFLOW also uses markdown links. Match on the **github URL slug** (owner/repo), not display name — display names vary ("GSD" links to obra/superpowers).

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| New detector | `python3 audit-evals.py --workflow-drift` | report, exit 0 |
| Unit tests | `python3 -m unittest -q test_automation` | OK |
| Sync | `./sync-plugin-docs.sh` | exit 0 |

## Scope

**In scope**:
- `WORKFLOW.md` (add missing STACK picks to appropriate stages)
- `audit-evals.py` (new opt-in, report-only detector `--workflow-drift`)
- `CLAUDE.md` (one bullet documenting the new detector, in the existing detector list style)
- `test_automation.py` (characterization test for the new detector)
- `plugin/docs/` via `./sync-plugin-docs.sh` only
- `plans/README.md`

**Out of scope**:
- STACK.md content (it is gated by detector J; treat it as the source of truth)
- Making the new detector *gating* — it starts report-only; gating is a later human decision (mirrors `--overlaps` precedent)
- Restructuring WORKFLOW.md's three-layer format

## Git workflow

- Branch: `advisor/003-workflow-stack-drift`
- Commits: `docs(workflow): add missing STACK picks to stage tables` then `feat(audit): report-only WORKFLOW↔STACK drift detector`

## Steps

### Step 1: Enumerate today's drift

Extract STACK tool slugs: `grep -oE "github\.com/[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+" STACK.md | sort -u`, same for WORKFLOW.md; `comm -23` the two lists. Record the missing set (expect at minimum microsoft/markitdown; likely obra/superpowers-as-GSD and anthropics/claude-plugins-official-as-feature-dev are present elsewhere in WORKFLOW — verify).

**Verify**: the diff list is written to your scratch notes; `microsoft/markitdown` is in it.

### Step 2: Add each missing STACK pick to the right WORKFLOW stage table

For each missing tool, add a Tooling-layer row in the stage where STACK places it (markitdown → Plan stage; its STACK one-liner: "Converts PDF/Office/images/audio/HTML to clean Markdown so agents can actually read binary docs", Signal "Correctness, Cost Efficiency"). Match the existing row format exactly: `| | [name](url) — description ([eval](evaluations/name.md)) | Signals |`. Link the eval file if it exists (`ls evaluations/markitdown.md`).

**Verify**: re-run the Step-1 comm → empty missing set.

### Step 3: Add the --workflow-drift detector

New function `audit_workflow_drift(ctx)` in `audit-evals.py`, modeled on `audit_stack_drift` (line 360): parse STACK slugs and WORKFLOW slugs (reuse any existing link-parsing helper in `catalog_lib.py` — check `grep -n "github.com" catalog_lib.py` before writing a new regex), report each STACK slug absent from WORKFLOW with the STACK line number. Wire an opt-in `--workflow-drift` flag; **report-only** (always exit 0 from this detector) — print a count so it's "a number to shrink". Do NOT add it to the gating set or Makefile.

**Verify**: `python3 audit-evals.py --workflow-drift` → "0 missing" (after Step 2). Temporarily delete the markitdown row from WORKFLOW.md, re-run → reports 1 missing with location; restore.

### Step 4: Document + test + sync

Add a CLAUDE.md bullet in the detector list (match the style of the `--overlaps` bullet: name, what it checks, "report-only, not a gate"). Add a `test_automation.py` characterization test with temp fixtures (a STACK with 2 slugs, WORKFLOW with 1 → detector reports 1). Run `./sync-plugin-docs.sh`.

**Verify**: `python3 -m unittest -q test_automation` → OK; `make check` → exit 0.

## Test plan

- Characterization test (Step 4): fixture-based, one missing slug detected, zero after fix.
- Manual negative test in Step 3.

## Done criteria

- [ ] `grep -c "markitdown" WORKFLOW.md` ≥ 1
- [ ] Step-1 comm of STACK-slugs minus WORKFLOW-slugs → empty
- [ ] `python3 audit-evals.py --workflow-drift` → exit 0, "0 missing"
- [ ] CLAUDE.md documents the flag; `python3 -m unittest -q test_automation` OK; `make check` exit 0
- [ ] `plans/README.md` updated

## STOP conditions

- The Step-1 missing set exceeds ~8 tools — the drift is bigger than planned; report the list for a human placement decision instead of guessing stages.
- A STACK pick has no plausible WORKFLOW stage (e.g. a meta-tool) — report rather than inventing a section.
- `audit-evals.py`'s detector registration pattern differs from the `DetectorContext` shape described (another refactor landed) — adapt to the current pattern, and if unclear, STOP.

## Maintenance notes

- The detector is one-directional by design (STACK ⊂ WORKFLOW). If someone later wants the reverse check, that's a new decision — WORKFLOW legitimately lists non-STACK options.
- Gating `--workflow-drift` in `make check` is a candidate follow-up once it's been quiet for a few weeks (the `--overlaps` → detector-O path is the precedent).
- Reviewer: confirm added WORKFLOW rows link evals where they exist and carry honest Signal values from STACK, not new claims.
