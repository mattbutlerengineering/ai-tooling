# Evaluation: Agent of Empires (AoE)

**Repo:** [agent-of-empires/agent-of-empires](https://github.com/agent-of-empires/agent-of-empires)
**Stars:** 2,613 | **Last updated:** 2026-06-19 (pushed; created 2026-01-09) | **License:** MIT
**Dev loop stage:** Implement (a session manager that runs/monitors multiple coding-agent sessions; touches Review via in-TUI diff view)
**Layer:** Tooling (Rust TUI + web dashboard, tmux-backed)

---

## What it does

Agent of Empires is a **session manager for AI coding agents on Linux and macOS**, usable from a terminal TUI or any browser (a PWA-installable web dashboard). Each agent runs in its own **tmux session**, so sessions outlive the terminal — close the TUI, drop SSH, or crash your terminal and everything resumes where you left off (`Ctrl+b d` detaches back to the dashboard).

It supports a wide spread of agents — Claude Code, OpenCode, Mistral Vibe, Codex CLI, Gemini CLI, Antigravity CLI, Cursor CLI, Copilot CLI, Pi.dev, Factory Droid, Hermes, Kiro CLI, Qwen Code — and gives you one status column to see which are running, waiting for input, or idle. It sets up **git worktrees and multi-repo workspaces** so parallel agents work on different branches without colliding, with optional **Docker/Podman/Apple-Container sandboxing** (shared auth volumes). The web dashboard (beta) renders a "structured view" of agent state via the Agent Client Protocol — plan panels, tool-call cards, swipe-to-approve — or flips to raw tmux terminal rendering. Press `R` in the TUI to expose the dashboard over HTTPS with QR + passphrase auth via Tailscale Funnel or Cloudflare Tunnel, for **phone/tablet access**. Also ships a CLI + HTTP API to drive sessions from external orchestrators, an in-TUI diff view, session resume, and sound/push notifications.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No binary installed, no session created. Claims come from the repository (GitHub metadata, README feature list, topics) — the project's own documentation, not observed behavior.

```bash
gh api repos/agent-of-empires/agent-of-empires --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/agent-of-empires/agent-of-empires/readme --jq '.content' | base64 -d   # feature list, install, how-it-works
gh api repos/agent-of-empires/agent-of-empires/releases --jq 'length'               # 30
```

## What worked

- **tmux as the persistence substrate is the right primitive.** Backing each session with tmux means agents genuinely survive disconnects/crashes/reboots — a real durability win over wrapper TUIs that hold sessions in their own process.
- **Broadest multi-agent support seen in the category.** 13 agent CLIs, not just Claude Code — useful if you mix harnesses or want one dashboard over a heterogeneous fleet.
- **Worktrees + container sandboxing built in.** Parallel branches and optional Docker/Podman/Apple-Container isolation are exactly the coordination layer multi-session agent work needs, configured for you.
- **Genuine remote/mobile access.** One-key HTTPS exposure with QR + passphrase auth over Tailscale/Cloudflare tunnels, plus a PWA and push notifications, is an uncommon and practically useful capability for babysitting long runs away from the desk.
- **Scriptable.** CLI + HTTP API means it can sit under an external orchestrator rather than being a dead-end GUI; actively iterating (30 releases, Homebrew/Nix install).

## What didn't work or surprised us

- **Web dashboard is explicitly beta** ("stabilization in progress") — the mobile/browser path, a headline feature, is not yet stable.
- **Linux/macOS only, tmux required.** No Windows; tmux is a hard prerequisite, so it's a terminal-native tool, not a standalone app.
- **Crowded niche.** It competes directly with claude-squad (lean TUI), Nimbalyst (visual Electron workspace), superset, and gastown — the differentiation is breadth of agent support + tmux durability + remote access, not a new category.
- **Remote exposure is a real attack surface.** Exposing a terminal-driving dashboard over a public HTTPS tunnel is powerful but security-sensitive; QR + passphrase auth is the only gate described.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | In-TUI diff view + structured plan/tool-call cards with swipe-to-approve add a human review checkpoint; doesn't change agent output quality itself. |
| Speed | + | Parallel sessions across worktrees with at-a-glance status removes the "which agent is stuck?" babysitting tax. |
| Maintainability | neutral | Affects workflow/session management, not your codebase structure. |
| Safety | + / − | Docker/Podman sandboxing isolates agents (+); public HTTPS tunnel exposure of a terminal dashboard is an added attack surface (−). |
| Cost Efficiency | neutral | Free/MIT; spends your own provider tokens. |

## Verdict

**CONDITIONAL** — adopt if you run several coding agents in parallel from a terminal-centric Linux/macOS setup and want tmux-grade session durability, broad multi-agent support, and real phone/tablet remote access. It's actively developed, MIT-licensed, and the tmux-backed persistence + remote tunnel combo is genuinely differentiated. Hold off if you want a stable GUI today (web dashboard is beta), need Windows, or are already happy in claude-squad — AoE is the more feature-dense, more remote-capable cousin of the same TUI session-manager idea.

Compared to neighbors: **claude-squad** is the minimal TUI session manager; **Nimbalyst** is the maximal visual Electron workspace; **AgentsMesh** scales horizontally to a fleet of machines. AoE sits between claude-squad and Nimbalyst — terminal-native like the former, but with web/mobile reach and the widest agent-CLI support.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-of-empires](https://github.com/agent-of-empires/agent-of-empires) | tool | tmux-backed session manager for 13+ coding agents — TUI + web/PWA dashboard, git worktrees, Docker sandboxing, remote phone access | Running 5 agents across branches becomes a babysitting job; need durable sessions, at-a-glance status, and remote access | claude-squad, Nimbalyst, AgentsMesh, superset |
