# Evaluation: dmux

**Repo:** [standardagents/dmux](https://github.com/standardagents/dmux)
**Stars:** 1,655 | **Last updated:** 2026-05-25 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (also Ship — branch/merge/PR handling)
**Layer:** Tooling

---

## What it does

A dev agent multiplexer for git worktrees and coding agents. dmux is an interactive terminal UI (built on Ink/React) that sits on top of tmux and git worktrees. You run `dmux` inside a repo and it presents a keyboard-driven dashboard of "panes." Pressing `n` creates a new pane: you type a prompt, pick one or more agent CLIs (or none for a plain shell), and dmux provisions a dedicated git worktree + branch and launches the chosen agent(s) in their own tmux pane. Each pane is a full, isolated working copy, so several agents can run concurrently without stepping on each other's files.

The mechanism is: tmux supplies the multiplexed terminal surface (a pane per task), git worktrees supply the filesystem isolation (a branch + working dir per task), and dmux is the orchestration layer that wires them together and adds quality-of-life around the merge-back. When a task finishes, the pane menu (`m`) offers Merge (auto-commit, merge into main, clean up the worktree in one step) or Create GitHub PR (push the branch and file a PR). An optional OpenRouter key powers AI-generated branch names and commit messages. It is agent-agnostic — Claude Code, Codex, OpenCode, Cline, Gemini, Qwen, Amp, pi, Cursor, Copilot, and Crush CLIs are all supported — plus multi-project sessions, a built-in file/diff browser, pane visibility controls, macOS notifications when a background pane settles, and lifecycle hooks (worktree-create, pre-merge, post-merge).

## How we tested it

**Evidence:** REVIEW

Inspected the repo metadata, README, npm package manifest, and release history; did not install or run it (running it meaningfully requires tmux, Node 18+, and at least one agent CLI driving live worktrees, which is an interactive TUI session rather than a scriptable command). This is a repo/manifest/README review, not hands-on usage. No timing or throughput numbers are claimed.

```bash
gh api repos/standardagents/dmux --jq '{stars,license,description,pushed_at,language,open_issues}'
gh api repos/standardagents/dmux/readme --jq '.content' | base64 -d
gh api repos/standardagents/dmux/releases --jq '.[0:3] | .[] | {tag: .tag_name, date: .published_at}'
gh api "repos/standardagents/dmux/git/trees/main" --jq '.tree[].path'
gh api repos/standardagents/dmux/contributors --jq 'length'
npm view dmux version time.modified bin keywords dependencies --json
# Catalog overlap + worktrunk comparison:
grep -inE "worktrunk|dmux|worktree|multiplex|tmux|parallel agent" /Users/mbutler/github/ai-tooling/CATALOG.md
gh api repos/max-sixty/worktrunk --jq '{stars,language,pushed_at}'
```

## What worked

- **The topology is exactly right for the stated problem.** tmux pane per task + git worktree per task is the proven, low-magic way to isolate parallel agents. dmux doesn't reinvent isolation; it composes two battle-tested primitives and adds a UI. That's a sound design choice and the lightest credible way to get true filesystem isolation between concurrent agents.
- **Genuinely agent-agnostic.** Eleven supported agent CLIs, multi-select per prompt, and a "no agent / plain terminal" option. You are not locked into Claude Code, and you can run, e.g., Claude Code and Codex side by side on the same task for comparison — a real differentiator versus single-vendor harnesses.
- **Closes the loop back to main.** One-step Merge (auto-commit + merge + worktree cleanup) and Create-GitHub-PR directly address the part of worktree workflows people get wrong by hand — orphaned worktrees and forgotten branches. Lifecycle hooks (create/pre-merge/post-merge) let you wire in checks before a merge lands.
- **Mature for its category.** v5.9.0 on npm, a steady release cadence (v5.8.0 → v5.8.1 → v5.9.0 within weeks), 15 contributors, 1.6K stars, MIT, hosted docs at dmux.ai, and a self-hosted "dmux-on-dmux" dev loop. This is well past the prototype stage that several Agent-Orchestration catalog peers are stuck in.
- **Thoughtful operator ergonomics.** Built-in file/diff browser, pane hide/isolate controls, per-pane base-branch and explicit branch-name overrides (useful for ticket-named branches), and native macOS attention notifications when a background pane needs you — the details that matter when you're juggling several long-running agents.

## What didn't work or surprised us

- **Not validated hands-on here.** Everything above is from the README, manifest, and release history. Claims about merge smoothness and the TUI's responsiveness are the project's, not observed in this environment.
- **tmux + macOS-flavored.** Hard requirement on tmux 3.0+ (no native non-tmux mode), and the notification feature is macOS-specific. Fine for a terminal-native macOS/Linux workflow; a non-starter for anyone not living in tmux.
- **README points at a different issues repo.** The README's Issues/Documentation links go to `formkit/dmux` while the canonical repo is `standardagents/dmux` (no GitHub `source` redirect). Likely an org rename/move; minor, but a maintenance signal worth noting and a small friction for filing issues.
- **Heavier than worktrunk for the pure-CLI crowd.** dmux is an opinionated interactive TUI (Ink/React, and it even pulls in `vue` as a dependency for its frontend/file browser). If you want scriptable, composable worktree commands rather than a dashboard, this is more surface area than you need (see comparison).
- **Optional cloud dependency for the nice-to-haves.** AI branch names and commit messages need an OpenRouter API key — a third-party metered service. The core worktree/merge flow works without it, but the "AI naming" headline feature does not.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Isolation prevents agents from corrupting each other's files, but dmux doesn't add verification gates — correctness still depends on the agents and your hooks |
| Speed | + | Multiple agents run truly in parallel in isolated worktrees instead of one-at-a-time; one-step merge/cleanup removes manual worktree churn |
| Maintainability | + | Worktree-per-task keeps branches clean and mergeable; lifecycle hooks + AI-generated branch/commit names keep history tidy; one-step cleanup avoids orphaned worktrees |
| Safety | + | Filesystem isolation contains a misbehaving agent to its own worktree/branch; pre-merge hooks can gate before anything lands on main |
| Cost Efficiency | neutral | Free/MIT and adds no token cost itself; running N agents in parallel multiplies underlying agent spend, and AI naming adds a small OpenRouter cost |

## Verdict

**SKIP** — redundant with [`claude-squad`](https://github.com/smtg-ai/claude-squad) (STACK, `RUN`). Both are terminal session managers over git worktrees: launch
several coding agents, watch them, switch between them, merge the work back. That is one job, and
the incumbent has been run.

The delta the evaluation identifies is merge-back ergonomics and a broader agent roster. Real, but
an ergonomic improvement on a job already covered is what this band eliminates — and the evaluation
itself scopes the audience out from under it: *"if you work with a single agent at a time, don't
use tmux, or want scriptable/composable worktree commands rather than a TUI, the lighter
`worktrunk` (or plain `git worktree`) is a better fit."*

Adoption decides the tie. dmux is ★1.7K against claude-squad's ★8.1K, and the catalog's answer to
"I want a *better* session manager than the incumbent" is `herdr` (★24K, Apache-2.0, pushed today),
which this same pass left open as a head-to-head. dmux is not that challenger.

Re-open if worktree merge-back specifically becomes the friction that makes the incumbent unusable.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dmux](https://github.com/standardagents/dmux) | tool | Dev agent multiplexer for git worktrees and coding agents | Need lightweight worktree-based agent isolation without full orchestration | worktrunk, claude-squad |
