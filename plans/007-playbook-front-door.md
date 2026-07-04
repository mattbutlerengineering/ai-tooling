# Plan 007: Create PLAYBOOK.md — the single front door that answers install / work / watch

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- README.md WORKFLOW.md STACK.md CLAUDE.md methodologies/ spikes/`
> Plans 001/003 intentionally touch README/WORKFLOW/STACK; verify their
> changes landed (or didn't) and adjust references accordingly.

## Status

- **Priority**: P1
- **Effort**: M
- **Risk**: LOW
- **Depends on**: plans/005-next-evals-queue.md, plans/006-watchlist.md (it links both; if they haven't landed, see STOP conditions)
- **Category**: docs
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The repo's stated purpose is "an operating manual for AI-assisted development" (`README.md:3`), but the answer to "how should I best use AI for development?" is federated across README (router) → WORKFLOW.md (434-line stage map) → STACK.md (install picks) → STACK-LEDGER (why-not) — while the two most prescriptive documents are orphaned: `methodologies/intent-to-production-recipe.md` (a runnable intent→PRD→issues→merged-PR pipeline) and `spikes/my-dev-workflow-assessment.md` (the maintainer's actual setup mapped to the loop, with named gaps) are linked from **nowhere** on the front door (0 grep hits in README/WORKFLOW/STACK, verified). This plan creates one canonical page that answers the three questions in order and routes to the depth docs, and wires the orphans in.

## Current state

- `README.md` (55 lines, read in full at 4cc412e): Install → Contents (flat list: WORKFLOW, CATALOG, COMPARISON, STACK, LEARNING, evaluations/) → Integrity → Quick Start (`/setup-workflow`) → The Workflow (two loops / three layers / five signals summary) → "See WORKFLOW.md for the full operating manual."
- The three questions and today's partial answers:
  - *What to install* → `STACK.md` (Quick Start install block at ~5-22, Evidence tiers at ~26-38, per-stage tables). Strongest existing answer.
  - *How to work* → `WORKFLOW.md` (process-prescriptive per stage) + `methodologies/intent-to-production-recipe.md` (the end-to-end recipe: `intent ─▶ /to-prd ─▶ PRD ─▶ brainstorming+writing-plans ─▶ /to-issues (+beads) ─▶ /implement-issue ─▶ merged PR ─▶ /triage` — verified this diagram exists at its line ~7-13).
  - *What to watch* → after plans 005/006: `NEXT-EVALS.md` + `WATCHLIST.md`. Before them: nothing.
- Orphans (verified): `grep -c "spikes/" README.md WORKFLOW.md STACK.md` → 0,0,0; same for `methodologies`.
- `workflows/README.md:17` promises "When a workflow here proves durable, fold it into WORKFLOW.md" — no fold-in tracking exists; this plan adds a lightweight promotion ledger there (finding: 30 daily logs, write-only).
- Conventions: docs sync to plugin (`./sync-plugin-docs.sh`; allowlist per `docs/adr/0001-plugin-docs-sync-allowlist.md`); counts are derived (never hand-write a tool/eval count in the new page — reference, don't restate); `make check` gates.

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Sync | `./sync-plugin-docs.sh` | exit 0 |
| Reconcile check | `python3 reconcile-counts.py --check` | exit 0 |

## Scope

**In scope**:
- `PLAYBOOK.md` (create, repo root)
- `README.md` (route to it; trim the duplicated "The Workflow" summary down to a pointer)
- `workflows/README.md` (add a "Promoted to WORKFLOW.md" ledger section — a table: date, pattern, where it landed; seed it empty or with any promotions you can verify from git history — do not invent entries)
- `CLAUDE.md` Structure list (one line for PLAYBOOK.md)
- `plugin/` via sync (add PLAYBOOK.md to the allowlist — user-facing; follow ADR-0001's amendment process if it specifies one)
- `plans/README.md`

**Out of scope**:
- Rewriting WORKFLOW.md or STACK.md content (003 handles their reconciliation)
- Moving `spikes/` or `methodologies/` files (link, don't relocate)
- Any hand-written count (tool totals, eval totals — link to the pages that carry derived numbers)

## Steps

### Step 1: Write PLAYBOOK.md (~80-120 lines, structure fixed here)

```markdown
# The Playbook — how to use AI for development, in one page

(one paragraph: who this is for; the three questions this page answers)

## 1. What to install
→ STACK.md — the curated ~25, tiered by evidence (Tier 1 measured / Tier 2 review-based).
(3-5 bullets naming the non-negotiable core with one-line whys, linking each
to its eval: context7, github-mcp-server, markitdown, claude-mem, beads — pull
the exact set from STACK's Quick Start, don't invent.)
Why a pick is/isn't here: STACK-LEDGER.md.

## 2. How to work
The loop: Plan → Implement → Verify → Review → Ship, Reflect feeding back (link WORKFLOW.md).
The runnable end-to-end recipe: methodologies/intent-to-production-recipe.md
(inline its pipeline diagram verbatim).
A worked example of assessing your own setup: spikes/my-dev-workflow-assessment.md.
Bootstrap any repo: /setup-workflow.

## 3. What to watch
NEXT-EVALS.md — the ranked evaluate-next queue (derived).
WATCHLIST.md — deferred verdicts, stale evals, flagged candidates, unverified claims (derived).
LEARNING.md — passive learning: channels, talks, references.
Scan intake: GitHub issues labeled `scan`.

## How this stays honest
(3 bullets: derived counts/reconcile, evidence taxonomy + honesty gates,
make check in CI — link CLAUDE.md's Integrity audit section.)
```

**Verify**: `ls PLAYBOOK.md`; every relative link resolves: `grep -oE "\]\(([^)h][^)]*)\)" PLAYBOOK.md | tr -d ']()' | while read f; do [ -e "$f" ] || echo "BROKEN: $f"; done` → no BROKEN lines.

### Step 2: Route README to it

Add PLAYBOOK.md as the FIRST entry in Contents with "**start here**"; replace the "The Workflow" section body with two sentences + a pointer to PLAYBOOK.md (keep the Install and Integrity sections untouched).

**Verify**: `grep -n "PLAYBOOK" README.md` → ≥2 hits (contents + pointer); `python3 reconcile-counts.py --check` still exit 0 (you didn't break a derived count string).

### Step 3: Add the promotion ledger to workflows/README.md

New section "## Promoted to WORKFLOW.md" with the table header and either verified rows (check `git log --oneline --grep="fold\|promote" -- WORKFLOW.md` for evidence) or an empty table + one line: "No promotions recorded yet — when a pattern from these logs proves durable, add a row here in the same PR that edits WORKFLOW.md."

**Verify**: section exists; no invented rows.

### Step 4: CLAUDE.md, sync allowlist, gate

Add PLAYBOOK.md to CLAUDE.md's Structure list (one line, style-matched). Add it to the sync allowlist per ADR-0001 (read `docs/adr/0001-plugin-docs-sync-allowlist.md` first — follow its amendment convention). Run `./sync-plugin-docs.sh`, then `make check`.

**Verify**: `make check` → exit 0; `ls plugin/docs/PLAYBOOK.md` exists (if the allowlist covers docs/) or the ADR-consistent alternative you chose is documented in the commit message.

## Test plan

No unit surface. Link-resolution check (Step 1), reconcile `--check` (Step 2), full gate (Step 4).

## Done criteria

- [ ] PLAYBOOK.md exists, answers install/work/watch in that order, zero broken relative links
- [ ] README Contents lists PLAYBOOK.md first as "start here"
- [ ] `spikes/my-dev-workflow-assessment.md` and `methodologies/intent-to-production-recipe.md` each reachable from PLAYBOOK.md (no more orphans)
- [ ] workflows/README.md has the promotion ledger
- [ ] No hand-written tool/eval counts in the new/changed text (`grep -nE "[0-9]{3} (tools|evaluations)" PLAYBOOK.md` → no matches)
- [ ] `make check` → exit 0; `plans/README.md` updated

## STOP conditions

- Plans 005/006 haven't landed (no NEXT-EVALS.md / WATCHLIST.md): write section 3 linking LEARNING.md + the `scan` label only, add a `<!-- TODO(plans 005/006): link NEXT-EVALS.md and WATCHLIST.md -->` comment, and note the reduced scope in your report — do NOT fabricate links to files that don't exist.
- The ADR-0001 allowlist process is unclear or the sync script rejects the addition — STOP; syncing conventions are load-bearing here (lockstep invariant in CLAUDE.md).
- STACK's Quick Start core set differs from the 5 tools named in Step 1's sketch — use what STACK actually says; if STACK has no Quick Start block anymore, STOP.

## Maintenance notes

- PLAYBOOK.md is hand-maintained prose — the one exception to derive-everything. Keep it a *router* (links + one-liners), never a data mirror; anything that can drift (counts, tiers, queues) must live in the derived pages it links.
- Reviewer: check the page reads in under 3 minutes and every claim is a link, not a restatement.
- Deferred: a `--playbook-links` detector verifying its links resolve (cheap follow-up if rot appears).
