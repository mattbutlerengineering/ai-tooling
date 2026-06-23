# Evaluation: superset

**Repo:** [superset-sh/superset](https://github.com/superset-sh/superset)
**Stars:** 11,948 | **Last updated:** 2026-06-18 | **License:** Elastic License 2.0 (ELv2 — source-available, not OSI-open)
**Dev loop stage:** Implement (also Ship — branch/worktree/diff/merge handoff)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Code editor for the AI agents era — run an army of Claude Code, Codex, etc." Superset is a macOS **Electron desktop application** (React + Tailwind + Bun + Turborepo, source-available under ELv2) that orchestrates multiple CLI-based coding agents in parallel, each isolated in its own git worktree, behind a single GUI.

The mechanism: Superset does not replace or re-implement the coding agent. It launches existing agent CLIs — Claude Code, Codex, Cursor Agent, Gemini CLI, Copilot, OpenCode, Amp, Droid, Pi, Mastra, or "any other CLI agent" — as subprocesses inside an embedded terminal, one per "workspace." Each workspace is backed by a dedicated git worktree (its own branch + working directory), so several agents run concurrently without colliding on files. The app adds a desktop cockpit on top: a workspace sidebar (⌘1–9 to switch), a built-in terminal with split panes, a built-in diff viewer to inspect/edit agent changes, agent-status monitoring with "needs attention" notifications, one-click "open this workspace in your editor/terminal," and per-workspace setup/teardown scripts (`.superset/config.json` with `setup`/`teardown` arrays and `SUPERSET_WORKSPACE_NAME` / `SUPERSET_ROOT_PATH` env vars). In short: the same worktree-per-task + parallel-agents + review/merge topology as dmux and claude-squad, but delivered as a polished native desktop app rather than a terminal UI. Its tagline — "If it runs in a terminal, it runs on Superset" — captures that it is an agent-agnostic *host*, not a single-vendor agent.

## How we tested it

**Evidence:** REVIEW

Inspected the repository metadata, the full root README, the repo file tree, license, topics, contributor count, and release history via the GitHub API. **Did not install or run it.** Running it meaningfully requires downloading a macOS Electron desktop binary (no Windows/Linux builds; "Windows/Linux untested"), and the dev path requires Bun, Docker, jq, Caddy, and a local Postgres + Electric stack — an interactive GUI desktop session, not a scriptable command. This is a repo/README/manifest review, not hands-on usage. No timing, throughput, or "10x" numbers are claimed here; the "Code 10x Faster" and "Run 10+ agents" figures are the project's marketing, not observed.

```bash
gh api repos/superset-sh/superset --jq '{stars,license,description,pushed_at,created_at,language,homepage,open_issues,forks}'
gh api repos/superset-sh/superset/readme --jq '.content' | base64 -d
gh api repos/superset-sh/superset/contributors --paginate --jq '.[].login' | wc -l   # 69
gh api repos/superset-sh/superset/releases --jq '.[0:5] | .[] | {tag: .tag_name, date: .published_at}'
gh api "repos/superset-sh/superset/git/trees/main" --jq '.tree[].path'
gh api repos/superset-sh/superset/topics --jq '.names'
# Catalog overlap check:
grep -inE "superset|dmux|claude-squad|worktree|parallel agent|cc-switch|oh-my-openagent" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Right topology, GUI delivery.** Worktree-per-task + parallel agents + built-in diff/review is the proven isolation pattern (same as dmux/claude-squad). Superset's differentiator is that it ships this as a native macOS desktop app with a real diff viewer and editor, not a tmux/Ink TUI — a meaningfully different ergonomic for people who don't live in a terminal multiplexer.
- **Genuinely agent-agnostic, and it hosts Claude Code rather than replacing it.** Ten-plus named agent CLIs plus "any other CLI agent." It is a front-end that *orchestrates* your existing `claude` (and Codex/Cursor/Gemini/etc.) — your agent config, skills, and model choices are unchanged. This is the key distinction from "switch-to" tools (cc-switch, oh-my-openagent): Superset is additive to the Claude Code dev loop, not a fork or replacement of it.
- **Strong maturity for the category.** ~11.9K stars, 69 contributors, very active (pushed 2026-06-18), separate desktop (`desktop-v1.12.5`, plus `desktop-canary`) and CLI (`cli-v0.2.23`) release tracks, hosted docs at docs.superset.sh, Discord, and a named team. Well past the single-author prototype profile that several Agent-Orchestration peers are stuck in.
- **Operator ergonomics built in.** Per-workspace setup/teardown scripts automate env/dep bootstrapping for each worktree (a real pain when spinning up N isolated copies), status monitoring with attention notifications, one-click handoff to your own editor/terminal, and a full customizable keyboard-shortcut surface.
- **Privacy posture is reasonable.** "Source available" under ELv2 with explicit, opt-in connections to agents/providers; no mandatory cloud relay for the core local worktree flow (the cloud Postgres/Neon/Electric pieces are for the dev/sync backend, not a hard runtime dependency for local use).

## What didn't work or surprised us

- **Not validated hands-on here.** Everything above is from README, file tree, license, and release history. The "10x faster" / "10+ agents simultaneously" claims are the project's, not observed in this environment.
- **macOS-only, heavy footprint.** Only macOS binaries ship; "Windows/Linux untested." It is a full Electron desktop app — far more surface area than a CLI/TUI. Non-starter for Linux/Windows terminal-native developers, and overkill if you want a scriptable, composable worktree primitive (worktrunk) or a lightweight TUI (dmux).
- **Elastic License 2.0, not OSI-open.** ELv2 is source-available with use restrictions (notably: you may not provide it as a hosted/managed service to third parties, and may not circumvent license-key functionality). Fine for individual/team local use, but it is *not* MIT/Apache like dmux, happy, or claude-squad — a real difference for anyone who needs permissive licensing.
- **High open-issue count.** ~1,361 open issues against a ~8-month-old project — consistent with rapid growth and broad agent support, but a signal that stability/triage is still catching up.
- **Multiplies underlying agent spend.** Like all parallel-agent cockpits, running 10 agents at once runs 10 agents' worth of tokens. The app is free to run locally but the workflow it enables is the cost driver, not Superset itself.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Worktree isolation stops agents from corrupting each other's files, but Superset adds no verification gate — correctness still depends on the agents and your setup scripts |
| Speed | + | Multiple agents run truly in parallel in isolated worktrees instead of one-at-a-time; built-in diff/review and one-click editor handoff cut context-switching wall time |
| Maintainability | + | Branch/worktree-per-task keeps changes isolated and reviewable; per-workspace setup/teardown scripts standardize environment bootstrapping; built-in diff viewer aids review-before-merge |
| Safety | + | Filesystem isolation contains a misbehaving agent to its own worktree/branch; explicit opt-in connections; local-first core (no mandatory cloud relay) |
| Cost Efficiency | neutral | Free to run locally and adds no token cost itself; running N agents in parallel multiplies underlying agent spend |

## Verdict

**CONDITIONAL**

Adopt Superset when you (1) work on **macOS**, (2) regularly run **multiple coding agents in parallel** and want a polished **desktop GUI** — embedded terminal, diff viewer, editor handoff, status monitoring — rather than a terminal UI, and (3) are comfortable with the **Elastic License 2.0**. It is a mature (11.9K stars, 69 contributors, active dual-track releases), agent-agnostic cockpit that *orchestrates* Claude Code (and Codex/Cursor/Gemini/etc.) rather than replacing it, so it is additive to the Claude Code dev loop — not a "switch-to" front-end.

It is **not a SKIP**: unlike cc-switch or oh-my-openagent (config switchers / vendor front-ends you adopt instead of Claude Code), Superset runs your existing agent CLIs unchanged and adds genuine parallel-worktree + review value to the Implement/Ship stages. But it is not an unconditional ADOPT: macOS-only, an Electron-heavy footprint, a non-OSI license, and a high open-issue count make it a poor default for Linux/Windows users, terminal-native developers, single-agent workflows, or anyone needing permissive licensing.

**vs. dmux / claude-squad** (both in catalog, both MIT): all three implement the same core — worktree-per-task isolation, parallel agent execution, and merge/review back to main. The axis that separates them is the *surface*. claude-squad and dmux are **terminal UIs** (tmux/Ink), cross-platform, scriptable-adjacent, and lightweight. Superset is a **native macOS Electron desktop app** with a graphical diff viewer, embedded multi-pane terminal, editor handoff, and workspace presets — heavier, GUI-first, macOS-only, ELv2-licensed. Pick dmux/claude-squad for a terminal-native, cross-platform, permissively-licensed multiplexer; pick Superset for a desktop cockpit if you want a real GUI and a built-in editor/diff experience and you're on macOS. They occupy the same niche (parallel-agent managers) but at opposite ends of the TUI-vs-desktop-app spectrum — the catalog's "overlaps with claude-squad, dmux" is accurate, with desktop-app delivery as the differentiator.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [superset](https://github.com/superset-sh/superset) | tool | Code editor for the AI agents era — run an army of Claude Code, Codex, etc. | Want a macOS desktop GUI to run and review many CLI agents in parallel across worktrees | claude-squad, dmux |
