# Routines: unattended cloud agents

A **routine** is a scheduled Claude Code cloud agent that runs against this repo on its
own (the daily discovery-and-triage pass is the canonical one). Routines are defined
server-side at <https://claude.ai/code/routines> — nothing in this repo schedules them.
Their only in-repo lever is this file: every routine checks out the repo and reads
`CLAUDE.md`, which points here.

This doc is the branch-and-merge contract. For what a routine may *conclude*, see the
eliminate-only rule in `CLAUDE.md` and `NEXT-EVALS.md` — that is unchanged and
independent of anything below.

## The rule: a routine lands its own PR

**A routine merges its own PR into `main` once CI is green.** It does not park the PR
for human review.

The old posture — open a PR, then self-check-in every 30–60 minutes until a human
merges it — produced the exact failure it was meant to avoid. PR #291 (discovery
2026-07-31) sat open ~24h across roughly a dozen check-in cycles and merged at
2026-08-01T20:03Z; PR #293 (discovery 2026-08-01) was closed one minute later at
20:04Z. Two catalog PRs cannot coexist — they both rewrite `CATALOG.md`,
`COMPARISON.md`, `NEXT-EVALS.md` and `WATCHLIST.md` — so the second day's work was
discarded rather than merged. Landing each pass before the next one starts is what
keeps that from recurring.

Review still happens; it happens *after* the merge, on a small dated commit that is
trivial to revert, instead of *before* it, on a branch that rots while it waits.

## Sequence

1. **Start from fresh `main`.** `git fetch origin main && git checkout -b routine/<lane>-<YYYY-MM-DD> origin/main`.
   Branch name is `routine/<lane>-<date>` (e.g. `routine/discovery-2026-08-01`). Nothing
   keys on the prefix mechanically — it is a convention that makes the lane greppable in
   `gh pr list` and obvious in the log.

2. **Check the lane is clear first.** `gh pr list --state open --json number,headRefName`.
   If a PR from the same lane is still open, resolve it before opening a second one —
   land it if it is green, or close it if this run supersedes it. **Never leave two PRs
   from the same lane open at once.** This is the rule that would have saved #293.

3. **Do the work, then gate it.** `make fix && make check`.
   One expected exception in the cloud sandbox: detector A (the network install
   resolver) needs the `gh` CLI and cannot run there. A detector-A-only failure is not a
   blocker — note it in the PR body and continue. CI runs it with a token. **Any other
   red gate is a blocker.**

4. **Open the PR.** Conventional-commit title, body stating what changed and the gate
   result.

5. **Queue the merge.** `gh pr merge <n> --auto --squash --delete-branch`.
   `main` requires the `audit` check (`.github/workflows/integrity.yml`, which runs
   `make check`), so GitHub holds the merge until that check is green and then lands it.
   CI is the authority here, not the sandbox run. Prefer `--auto` over watching: the
   routine can exit instead of burning check-in cycles, and the wait is enforced
   server-side rather than by the agent's own judgment.

   Use `gh pr checks <n> --watch` only when the routine needs to *see* the result — for
   example to fix a red build in the same run.

6. **Reconcile with `main` if it moved.** Do not act on `mergeStateStatus` alone — a
   `main` that has moved flips it to `unknown` while GitHub lazily recomputes, which is
   not a conflict. Confirm with a trial merge:

   ```sh
   git merge-tree --write-tree origin/main origin/routine/<lane>-<date>
   ```

   On a real conflict: `git fetch origin main && git merge origin/main`, resolve,
   re-run `make fix && make check`, push. The queued auto-merge survives the push and
   re-waits on the new head.

7. **Confirm it landed** before ending the run — `gh pr view <n> --json state,mergedAt`.
   A queued auto-merge that never fires is a stuck lane, and step 2 of tomorrow's run
   will trip over it.

Protection on `main` is `enforce_admins: false`, so an admin token can still merge past
a red `audit`. That is deliberate — it keeps direct-to-main commits working for routines
that don't branch, and keeps the repo owner unblocked. It also means the required check
is a guardrail plus the mechanism that makes `--auto` wait, not an unbypassable gate for
an agent running with owner credentials. The do-not-merge list below is still binding.

## When a routine must NOT merge

Leave the PR open, comment on it with the reason, and notify. Do not merge if:

- **`make check` is red** on anything other than the detector-A network resolver.
- **CI is red.** Check whether it reproduces on `main` first: if it does, say so once in
  the thread and wait for recovery — it is not this PR's fault. If it is the PR's, fix
  and push.
- **A conflict is not mechanically resolvable** — anything needing a judgment call about
  which side wins.
- **The diff reaches outside the lane's declared scope.** A discovery pass touches
  `CATALOG.md`, `COMPARISON.md`, `evaluations/`, `NEXT-EVALS.md`, `WATCHLIST.md`,
  `discovery/` and the derived `plugin/` mirrors. A change to `Makefile`, `audit-evals.py`,
  `STACK.md`, a detector, or CI is out of scope for an unattended pass and needs a human.
- **The pass wrote an `ADOPT`/`KEEP`/`CONDITIONAL` verdict.** Detector Q gates this
  mechanically; if it somehow passes, self-merge is still off. Auto-merge changes how a
  routine's work *lands*, not what it is allowed to *conclude*.

## Reverting

Every routine merge is one squashed, dated commit. `git revert <sha>` undoes a bad pass
cleanly — that reversibility is the premise the whole policy rests on. If a merged pass
turns out to be wrong, revert it and file an issue; do not hand-patch main.
