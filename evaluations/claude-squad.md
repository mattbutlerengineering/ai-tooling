# Evaluation: Claude Squad

**Repo:** [smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)
**Stars:** 7,838 | **Last updated:** 2026-06-19 | **License:** AGPL-3.0
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Go TUI that manages multiple AI coding agents (Claude Code, Codex, Gemini CLI, Aider) in parallel terminal sessions. Each task gets its own tmux session and git worktree, so agents work on isolated branches without merge conflicts. The TUI shows all active sessions with a live diff preview, lets you attach/detach from any session, and has a one-key push-to-GitHub flow. An `--autoyes` flag enables fully autonomous operation across all sessions.

The core architecture is simple: tmux for session isolation, git worktrees for code isolation, and a Go TUI (Bubble Tea) for visibility. No MCP, no plugins, no complex orchestration — just parallel agent management with a clean interface.

## How we tested it

**Evidence:** REVIEW

Architecture review via GitHub API. Examined the repo structure (Go monorepo: `app/`, `session/`, `daemon/`, `ui/`, `keys/`, `config/`), README, configuration format, release cadence, and issue tracker. Not installed locally — requires tmux which is available but was not tested hands-on.

```bash
gh api repos/smtg-ai/claude-squad --jq '.stargazers_count, .license.spdx_id, .updated_at'
gh api repos/smtg-ai/claude-squad/releases --jq '.[0:5] | .[] | "\(.tag_name) \(.published_at)"'
```

## What worked

- **Simplicity is the feature.** tmux + git worktrees is the right abstraction level — no container overhead, no Docker dependency, no complex setup. `brew install claude-squad && cs` gets you running.
- **Agent-agnostic.** Profile system lets you switch between Claude Code, Codex, Aider, Gemini with a config change. No vendor lock-in.
- **Diff preview in TUI.** Tab between live output and git diff without attaching to the session — fast triage of what each agent produced.
- **Git isolation by default.** Each session gets its own worktree and branch, preventing the merge conflict chaos of parallel agents on the same branch.
- **Active maintenance.** 19 releases, v1.0.19 released yesterday, Homebrew formula, 559 forks. The Go binary is small and self-contained.

## What didn't work or surprised us

- **AGPL-3.0 license.** More restrictive than MIT — organizations with copyleft concerns may not adopt it.
- **tmux dependency.** Requires tmux installed separately. Not an issue on macOS/Linux, but adds a prerequisite.
- **No CI/PR feedback loop.** Unlike agent-orchestrator (CONDITIONAL), there's no reaction system — CI failures and review comments don't automatically route back to the agent. You check manually.
- **No built-in methodology.** Claude Squad manages sessions but doesn't enforce any development methodology (TDD, review gates). Compare with superpowers (ADOPT) which embeds process.
- **50 open issues.** Moderate issue count suggests active use but some rough edges (tmux session cleanup, worktree deletion).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Git worktree isolation prevents cross-agent contamination |
| Speed | ++ | Parallel agent execution — N tasks in the time of 1 |
| Maintainability | neutral | Doesn't affect code quality, just agent management |
| Safety | + | Isolated worktrees prevent accidental main-branch mutations |
| Cost Efficiency | + | Parallel sessions amortize context-loading cost across tasks |

## Verdict

**CONDITIONAL**

Use when you have 3+ independent tasks that can run in parallel — the speed multiplier from concurrent agents is real. Skip for single-task workflows where Claude Code alone suffices. Agent-orchestrator (CONDITIONAL) is the better choice when you need automated CI feedback loops; claude-squad is better when you want simplicity and manual oversight. The AGPL license may block adoption in some organizations.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-squad](https://github.com/smtg-ai/claude-squad) | tool | Manages multiple AI terminal agents in parallel with TUI, worktrees, and diff preview | Running one agent at a time is slow; need parallel sessions with visibility | agent-orchestrator, gastown, sandcastle |
