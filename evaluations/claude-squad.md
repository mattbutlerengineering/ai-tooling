# Evaluation: Claude Squad

**Repo:** [smtg-ai/claude-squad](https://github.com/smtg-ai/claude-squad)
**Stars:** 7,890 | **Last updated:** 2026-06-23 (pushed 2026-06-17) | **License:** AGPL-3.0-only
**Last verified:** 2026-06-22
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Go TUI that manages multiple AI coding agents (Claude Code, Codex, Gemini CLI, Aider, Amp) in parallel terminal sessions. Each task gets its own tmux session and git worktree, so agents work on isolated branches without merge conflicts. The TUI shows all active sessions with a live diff preview, lets you attach/detach from any session, and has a one-key push-to-GitHub flow. An `--autoyes`/`-y` flag enables (experimental) fully autonomous operation across all sessions; `-p/--program` sets the agent binary to launch in each new instance.

The core architecture is simple: tmux for session isolation, git worktrees for code isolation, and a Go TUI (Bubble Tea) for visibility. No MCP, no plugins, no complex orchestration — just parallel agent management with a clean interface. The Homebrew formula installs the binary as `claude-squad` (not `cs`); the `cs` short name is created by the upstream `install.sh`.

## How we tested it

**Evidence:** RUN

**Installed and ran Claude Squad hands-on on 2026-06-22** (macOS arm64). Installed `claude-squad` **v1.0.19** plus its `tmux` runtime dependency via Homebrew (`brew install claude-squad tmux`, ~12 s wall, 4.9 MB self-contained Mach-O arm64 binary). I then enumerated the full command/flag surface from real `--help` output, exercised every non-interactive subcommand (`version`, `debug`, `reset`, `completion`) and captured their on-disk effects, and confirmed the runtime gate that makes the TUI undrivable headless. **The interactive Bubble Tea TUI and the live parallel-agent orchestration loop (spawning agent sessions across tmux + git worktrees, the diff preview, the push-to-GitHub flow) were NOT driven** — the binary requires a real TTY (`could not open a new TTY` when launched from a non-terminal, quoted below) and each session would launch a real coding agent, neither of which is drivable in this environment. What is measured below is the install, the CLI surface, the config/state mechanics, and the dependency/TTY checks — not generated-code quality from a parallel run.

```bash
# Install (Homebrew formula exists; binary lands as `claude-squad`, not `cs`)
brew install claude-squad tmux        # ~12 s; claude-squad 1.0.19 (AGPL-3.0-only), tmux 3.6b

claude-squad version                  # → claude-squad version 1.0.19
claude-squad --help                   # 4 subcommands (completion/debug/help/reset/version) + -y/-p flags

# debug — resolves and prints config paths + the effective config
claude-squad debug
#   Config: /Users/<me>/.claude-squad/config.json
#   { "default_program": ".../claude", "auto_yes": false,
#     "daemon_poll_interval": 1000, "branch_prefix": "<me>/" }
#   wrote logs to $TMPDIR/claudesquad.log

# reset — exercises the storage + tmux + worktree cleanup paths on a clean install
claude-squad reset
#   "Storage has been reset successfully"
#   "Tmux sessions have been cleaned up"
#   Error: failed to cleanup worktrees: ... open .../worktrees: no such file or directory
#   (writes ~/.claude-squad/state.json: {"help_screens_seen":0,"instances":[]})

claude-squad completion bash          # emits a valid bash-completion script (non-interactive generator)

# Launch headless (stdin from /dev/null, no TTY) to observe the runtime gate:
claude-squad < /dev/null
#   Error: could not open a new TTY: open /dev/tty: device not configured
#   → confirms the TUI needs a real terminal; the parallel-agent loop cannot run headless
```

**Install (measured).** The Homebrew formula resolves (`claude-squad: stable 1.0.19 (bottled)`, `License: AGPL-3.0-only`, ~6.8K installs/365d per brew analytics) and pours a single 4.9 MB arm64 binary in ~12 s alongside `tmux 3.6b`. The catalog's `brew install claude-squad` command is correct; the installed binary is `claude-squad`, and `cs` (referenced in upstream docs) is *not* created by the brew path — a minor but real discrepancy worth noting.

**Command surface (measured, from real `--help`).** Top-level help lists five subcommands — `completion`, `debug`, `help`, `reset`, `version` — and two persistent flags: `-y/--autoyes` (marked `[experimental]`, auto-accepts prompts in all instances) and `-p/--program` (the agent binary to run per instance, e.g. `aider --model ...`). With no subcommand it launches the TUI. This is a deliberately thin CLI: the product *is* the interactive TUI, and the subcommands are housekeeping.

**Config/state mechanics (measured).** `debug` resolved and printed `~/.claude-squad/config.json`, auto-detecting `default_program` to the user's installed `claude` binary and deriving `branch_prefix` from the username (`<me>/`), plus `daemon_poll_interval: 1000` ms — confirming the daemon-poll design the `daemon/` package implements. `reset` then ran the real cleanup path: it reset storage, reported "Tmux sessions have been cleaned up", wrote a fresh `state.json` (`{"help_screens_seen":0,"instances":[]}`), and surfaced an honest, observable edge — on a clean install with no `worktrees/` directory yet, worktree cleanup errors `no such file or directory` (a non-fatal `Error:` printed after the successful storage reset). That confirms reset's worktree-deletion path is wired but unguarded against a missing dir on first run.

**Runtime gate (measured).** Launched with stdin redirected from `/dev/null`, the binary fails fast with `could not open a new TTY: open /dev/tty: device not configured` and re-prints usage. This is the exact boundary that prevents driving the parallel-agent loop here: the TUI demands a controlling terminal, and TTY acquisition happens before any agent session is spawned (no tmux session was created — `tmux ls` reported none afterward, and no lingering sessions were left behind). `version` and `debug` return in <10 ms.

**Not exercised (disclosed).** The Bubble Tea TUI, parallel session spawning across tmux + git worktrees, the live diff preview, attach/detach, the one-key GitHub push, and `--autoyes` autonomous multi-agent operation were **not** run — they require an interactive terminal and live coding-agent sessions. The speed-multiplier claim (N tasks concurrently) and worktree-isolation behavior rest on the documented architecture plus the verified config/reset mechanics, not on an observed parallel run.

## What worked

- **Installs cleanly via Homebrew in ~12 s.** `brew install claude-squad tmux` pours a single self-contained 4.9 MB arm64 binary; the formula is real (`stable 1.0.19 (bottled)`, AGPL-3.0-only) with ~6.8K installs/year — the catalog install command is correct.
- **Thin, honest CLI surface.** Five subcommands, all of which I ran. `debug` and `reset` self-document and produce inspectable on-disk state (`~/.claude-squad/config.json`, `state.json`); `version`/`debug` return in <10 ms.
- **Sensible config auto-detection.** `debug` auto-resolved `default_program` to the installed `claude` binary and derived `branch_prefix` from the username — zero-config defaults that match the "just run it" pitch.
- **Reset cleanup is wired and visible.** `reset` reported storage + tmux cleanup explicitly rather than silently, and even its missing-`worktrees/`-dir edge surfaced as a clear `Error:` line — the mechanics fail loudly.
- **Simplicity is the feature.** tmux + git worktrees is the right abstraction level — no container/Docker overhead. The daemon-poll interval (1000 ms) in the resolved config confirms the lightweight background design.
- **Active maintenance.** v1.0.19 (2026-06-17), Homebrew core formula, 563 forks, 7.9K stars.

## What didn't work or surprised us

- **The TUI cannot run headless — the core loop is undrivable in CI/non-TTY contexts.** `could not open a new TTY` is a hard gate; you cannot script the parallel-agent flow without a real terminal. This is by design for an interactive tool but means the speed-multiplier value can't be verified non-interactively.
- **Binary is `claude-squad`, not `cs`, via brew.** Upstream docs reference `cs`; the Homebrew path installs `claude-squad` only. Anyone following `cs ...` from the README after a `brew install` hits `command not found`.
- **`reset` errors on a clean install.** Worktree cleanup is unguarded against a missing `~/.claude-squad/worktrees` directory, printing `Error: ... no such file or directory` even though the reset otherwise succeeded — cosmetically alarming on first use.
- **AGPL-3.0-only license.** More restrictive than MIT — organizations with copyleft concerns may not adopt it. Confirmed in both the GitHub API and the brew formula (`AGPL-3.0-only`).
- **tmux dependency.** Requires tmux installed separately (I had to `brew install tmux` — it was absent on this host). Not hard on macOS/Linux, but a real prerequisite.
- **No CI/PR feedback loop.** Unlike agent-orchestrator (CONDITIONAL), CI failures and review comments don't automatically route back to the agent; you triage manually via the diff preview.
- **50 open issues** suggest active use with rough edges (the worktree-cleanup edge above is a small instance).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Git worktree isolation prevents cross-agent contamination (architecture; the `reset` worktree-cleanup path is wired, observed firing). |
| Speed | ++ | Parallel agent execution — N tasks in the time of 1 (documented architecture; not measured headless since the TUI needs a TTY). |
| Maintainability | neutral | Doesn't affect code quality, just agent management. Config/state are small inspectable JSON files (verified on disk). |
| Safety | + | Isolated worktrees prevent accidental main-branch mutations; `branch_prefix` namespaces branches per user (verified in resolved config). |
| Cost Efficiency | + | Parallel sessions amortize context-loading cost across tasks (architecture); the daemon polls at 1 s (verified) rather than busy-waiting. |

## Verdict

**KEEP** (situational — in this repo's STACK for parallel multi-agent work)

The hands-on run confirms the install path, the (thin) CLI surface, and the config/state mechanics are real and behave as documented: `brew install claude-squad tmux` lands a working v1.0.19 binary in ~12 s, `debug` resolves a sensible zero-config setup, and `reset` exercises the storage/tmux/worktree cleanup visibly. Use it when you have 3+ independent tasks that can run in parallel — the tmux + git-worktree isolation is the right, low-overhead abstraction and the speed multiplier from concurrent agents is the draw. The verdict rests on a verified install + CLI/config surface plus the documented architecture, **not** on an observed parallel run: the Bubble Tea TUI requires a real TTY (`could not open a new TTY`) and live coding-agent sessions, so the parallel-agent loop, diff preview, and GitHub-push flow were not driven here. Two practical caveats the run surfaced: the brew binary is `claude-squad` (not the `cs` the README uses), and `reset` errors noisily on a clean install. agent-orchestrator (CONDITIONAL) remains the better pick when you need automated CI feedback loops; claude-squad wins on simplicity and manual oversight. The AGPL-3.0-only license may block adoption in some organizations.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-squad](https://github.com/smtg-ai/claude-squad) | tool | Manages multiple AI terminal agents in parallel with TUI, worktrees, and diff preview | Running one agent at a time is slow; need parallel sessions with visibility | agent-orchestrator, gastown, sandcastle |
