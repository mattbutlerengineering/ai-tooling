# Plan 004: Consolidate tool-scan intake on GitHub issues and index the dormant discovery/ logs

> **Executor instructions**: Follow step by step; verify each step. On any
> STOP condition, stop and report. Update this plan's row in `plans/README.md`
> when done.
>
> **Drift check (run first)**: `git diff --stat 4cc412e..HEAD -- discovery/ CLAUDE.md .github/`
> On drift, re-verify "Current state" before proceeding.

## Status

- **Priority**: P2
- **Effort**: S
- **Risk**: LOW
- **Depends on**: none
- **Category**: dx
- **Planned at**: commit `4cc412e`, 2026-07-03

## Why this matters

The repo has two parallel intake records for tool scans. `discovery/new-tools-loopN.md` files stopped at loop21 (last commit 2026-06-19: "loop 21 — coding-agent/ai-coding vector finds ~15 in-scope tools"), while live scans moved to GitHub issues — #189 (star sync, 2026-07-01) and #213 (skills scan, 2026-07-03) — with no back-link. `CLAUDE.md` still describes `discovery/` as the active path ("bulk discovery logs … from scanning sessions"). Agents and contributors following the documented path write to a dead directory; the live path is undocumented and unlabeled. One canonical path, documented, makes scan output queryable (issues are assignable/closeable — which plan 005's promotion queue builds on).

## Current state

- `discovery/` — 21 `new-tools-loopN.md` files, no README/index. `git log -1 --format="%ad %s" --date=short -- discovery/` → `2026-06-19 docs(discovery): loop 21 — …`.
- Live scans as issues: #189 "star sync — add 26 tools from 2026-07-01 scan" (closed by PR #191), #213 "Skills ecosystem scan: 4 new skills found (2026-07-03)" (closed by PR #214). Both used the `ready-for-agent` label; there is no `scan` label.
- `CLAUDE.md:19` (Structure): `- \`discovery/\` — bulk discovery logs (\`new-tools-loopN.md\`) from scanning sessions`. Also `CLAUDE.md` "Evaluations" section: "**Discovery logs** (`evaluations/new-tools-loopN.md`) are for bulk triage…" — note this line even cites the *wrong directory* (`evaluations/` instead of `discovery/`), an additional stale pointer to fix.
- Label vocabulary doc: `docs/agents/triage-labels.md` (default vocabulary `needs-triage`, `needs-info`, `ready-for-agent`, `ready-for-human`, `wontfix`).
- Repo convention: docs changes sync to plugin via `./sync-plugin-docs.sh`; `make check` is the gate.

## Commands you will need

| Purpose | Command | Expected |
|---------|---------|----------|
| Full gate | `make check` | exit 0 |
| Create label | `gh label create scan --description "Tool-scan intake (star sync, ecosystem scans)" --color 5319e7` | label created |
| Sync | `./sync-plugin-docs.sh` | exit 0 |

## Scope

**In scope**:
- `discovery/README.md` (create — index + deprecation pointer)
- `CLAUDE.md` (update the two stale descriptions)
- `docs/agents/triage-labels.md` (add the `scan` label to the vocabulary)
- GitHub: create the `scan` label; retro-label #189 and #213 (`gh issue edit 189 --add-label scan`, same for 213)
- `plugin/` via sync only
- `plans/README.md`

**Out of scope**:
- Deleting or rewriting the 21 existing loop files (they're historical record; the audit trail stays)
- Building the promotion queue itself (plan 005)
- An issue *template* for scans (nice-to-have; only add if trivial — a `.github/ISSUE_TEMPLATE/scan.md` with the #213 table shape — otherwise defer)

## Git workflow

- Branch: `advisor/004-discovery-intake`
- Commit: `docs(discovery): consolidate scan intake on labeled issues; index legacy loops`

## Steps

### Step 1: Create discovery/README.md

Contents: (1) one paragraph — this directory holds the historical bulk-triage logs, loops 1–21 (2026-06 era); (2) a table indexing the loop files (filename, date from git, one-line scope pulled from each file's first heading — `head -3 discovery/new-tools-loopN.md`); (3) a clearly-marked "Where scans live now" section: new scans are GitHub issues labeled `scan` (cite #189, #213 as exemplars), closed by the PR that catalogs their findings.

**Verify**: `ls discovery/README.md` exists; it names all 21 files (`grep -c "new-tools-loop" discovery/README.md` → ≥21).

### Step 2: Fix CLAUDE.md's two stale pointers

- Structure line: change to `- \`discovery/\` — historical bulk discovery logs (loops 1–21); new scans are GitHub issues labeled \`scan\` (see discovery/README.md)`.
- Evaluations section: fix `evaluations/new-tools-loopN.md` → `discovery/new-tools-loopN.md` and add the same "now issues labeled scan" pointer.

**Verify**: `grep -n "new-tools-loop" CLAUDE.md` shows only corrected text; no reference implies discovery/ is the active intake.

### Step 3: Create the label, retro-label, document the vocabulary

Run the `gh label create` command; `gh issue edit 189 --add-label scan`; `gh issue edit 213 --add-label scan`. Add `scan` to `docs/agents/triage-labels.md` in its existing format.

**Verify**: `gh issue list --state closed --label scan` lists #189 and #213.

### Step 4: Sync and gate

`./sync-plugin-docs.sh` then `make check`.

**Verify**: `make check` → exit 0.

## Test plan

No unit-testable surface. Verification is the per-step commands plus `make check` (guards the CLAUDE.md/plugin sync integrity).

## Done criteria

- [ ] `discovery/README.md` exists, indexes 21 loops, and points to the `scan` label
- [ ] `gh issue list --state closed --label scan` → #189, #213
- [ ] `grep -rn "evaluations/new-tools-loop" CLAUDE.md` → no matches
- [ ] `make check` → exit 0
- [ ] `plans/README.md` updated

## STOP conditions

- `gh label create` fails with permissions error → report; don't proceed with an undocumented label vocabulary.
- You find evidence the loop files are still actively written (a loop22+ exists or discovery/ has commits after 2026-06-19) — the "dormant" premise is wrong; report instead of deprecating.

## Maintenance notes

- Plan 005's promotion queue assumes scan findings arrive as `scan`-labeled issues whose tables carry star counts — this plan is its data-entry contract.
- Future scans should include the star count column (as #213 did); that's the queue's ranking input.
