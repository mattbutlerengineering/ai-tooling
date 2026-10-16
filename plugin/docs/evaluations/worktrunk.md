# Evaluation: worktrunk

**Repo:** [max-sixty/worktrunk](https://github.com/max-sixty/worktrunk)
**Stars:** 6,292 | **Last updated:** 2026-08-05 | **License:** NOASSERTION <!-- repo-metadata.json reads NOASSERTION; the repo's root LICENSE file is a dual MIT / Apache-2.0 grant, and Cargo.toml reads `MIT OR Apache-2.0`. The earlier "proprietary" header was wrong. -->
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

CLI for managing git worktrees, designed specifically for parallel AI agent workflows. Creates, lists, switches between, and cleans up worktrees. Wraps `git worktree` commands into a streamlined workflow so you can run multiple agents on different branches simultaneously without git conflicts.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed the real artifact from crates.io (`cargo install worktrunk`, v0.80.0, binary `wt`) and ran a with/without A/B on a disclosed fixture, 3 runs per arm, scored by end-state assertions on the repo. Then ran five targeted safety probes on dirty and unmerged worktrees.

```
$ cargo install worktrunk --root /tmp/eval-worktrunk/inst   # rc=0, ~6 min compile
$ wt --version
wt 0.80.0

# A/B, 3 runs per arm, identical fixture; ARM lines are the script's own output
ARM=raw CMDS=24 CHARS=579 SECS=.144   main files: app.txt feature-a.txt feature-b.txt feature-c.txt   worktrees: 1  branches: main
ARM=wt  CMDS=12 CHARS=312 SECS=.617   main files: app.txt feature-a.txt feature-b.txt feature-c.txt   worktrees: 1  branches: main
(runs 2 and 3: CMDS/CHARS/end-state identical; SECS raw .123 / .121, wt .626 / .610)

# safety probes
S1 wt remove <dirty worktree>        -> "Cannot remove worktree: dirty has uncommitted changes", exit=1, wip.txt still on disk
S2 wt remove <committed, unmerged>   -> worktree removed, "Branch unmerged; to delete, run wt remove -D unm", branch kept
S3 git worktree remove <dirty>       -> "contains modified or untracked files, use --force", exit=128
   git branch -d <unmerged>          -> "not fully merged", exit=1
S5 wt remove d2 -f (dirty)           -> removed with --force, exit=0
```

## Test design

- **Task/corpus:** a fresh git repo with one commit (`app.txt`); three parallel "agent" tasks `a`, `b`, `c`, each = create an isolated branch + worktree, add one file (`feature-<n>.txt`), land it on `main`, clean up the worktree and branch. The file edit is the same in both arms and is not counted.
- **Baseline:** raw git — `git worktree add -b`, `git add -A`, `git commit`, `git merge`, `git worktree remove`, `git branch -d` (24 counted commands including `cd`).
- **Metric:** correctness oracle on the end state (`main` holds all four files, `git worktree list` has 1 entry, only `main` branch remains), counted commands, typed characters, wall-clock over the whole sequence.
- **Reproduce:** `cargo install worktrunk`; for the treatment arm run per task `wt -y switch --create feat-<n> --no-cd`, `cd ../repo.feat-<n>`, edit, `wt -y merge main`, `cd` back; assert the end state above.

## What worked

- **Correctness oracle passed in both arms, 3/3 runs each:** `main` ended with all four files, one worktree and one branch left. `wt merge` auto-stages the untracked file, commits, merges to `main` and removes the worktree and branch in one command.
- **Fewer steps:** 12 commands / 312 typed characters vs 24 / 579 for raw git (about half), identical in all three runs.
- **Safety guard on dirty worktrees:** `wt remove` refuses a worktree with modified or untracked files (S1) and names `--force` as the opt-in; this matches raw git's refusal (S3).
- **Unmerged work survives:** removing a worktree whose branch is unmerged keeps the branch and prints the exact `-D` command to delete it (S2).
- **`wt list`** shows per-worktree dirty state (`?`, `!?`, `+N` counts) in a single table, where `git worktree list` shows only path, sha and branch.
- **License is permissive:** the root LICENSE file grants MIT and Apache-2.0 dual terms. The previous eval's "proprietary" claim was wrong.

## What didn't work or surprised us

- **Slower in wall-clock:** 0.61 s vs 0.12 s for the three-task sequence (about 5x), though both are sub-second in absolute terms. Removal runs in the background, so the cost is mostly process startup per `wt` call.
- **`wt merge` uses a fallback commit message** (`Changes to feature-a.txt`) when no LLM command is configured; the quality of commit messages depends on setup that needs a model credential, and that path was out of scope here.
- **No shell integration in this sandbox:** every `wt switch` warned it cannot change directory, so the arm used an explicit `cd ../repo.feat-<n>`; with `wt config shell install` that step goes away and the command count would drop further.
- **Build cost:** the crate pulls a large dependency tree and took about 6 minutes to compile; the project also ships prebuilt binaries, which this run left untried.
- **Scope of the A/B:** it is a single-user, scripted lifecycle on a toy repo. Concurrent live agent sessions, `wt hooks`, CI status columns and the PR checkout path (`wt switch pr:N`) were left untested. The earlier eval's claim that `wt clean` discarded uncommitted changes is not reproduced: the command names are different in v0.80.0 (`wt remove`) and the dirty-worktree probe refused removal.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Oracle passed 3/3 runs: `main` held all merged files, 1 worktree and 1 branch left |
| Speed | + | Half the commands (12 vs 24) and 312 vs 579 typed characters; wall-clock itself is slower, 0.61 s vs 0.12 s |
| Maintainability | neutral | Operates on git state, no effect on code structure |
| Safety | + | Dirty worktree removal refused (exit 1); unmerged branch kept; `--force` required to discard |
| Cost Efficiency | neutral | No model calls on the paths exercised; free and open source |
| Verifiability | + | `wt list` surfaces dirty and ahead/behind state per worktree, making agent branch state easy to confirm; the commit messages were generic without an LLM hook |

## Verdict

**discovery-log — measured; promotion candidate** — ran clean 3/3 on a disclosed worktree-lifecycle fixture at half the commands of raw git, with a working dirty-worktree guard and a permissive MIT / Apache-2.0 license; would read ADOPT or CONDITIONAL (adopt-if: running 3+ parallel agent sessions) on human confirmation, which should also test live concurrent agent sessions and hooks.

## Triage note

Hands-on pass on 2026-10-16 (eval-runner lane). Replaces the 2026-08/09 watch posture: the license ground it rested on was false (the repo ships a dual MIT / Apache-2.0 LICENSE, which GitHub reported as NOASSERTION), and the safety claim about aggressive cleanup is not reproduced in v0.80.0. Left at `discovery-log` because a human owns the promotion.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [worktrunk](https://github.com/max-sixty/worktrunk) | tool | CLI for git worktree management, designed for parallel AI agent workflows | Need isolated git branches for multiple agents working simultaneously | dmux |
