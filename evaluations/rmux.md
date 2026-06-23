# Evaluation: RMUX

**Repo:** [Helvesec/rmux](https://github.com/Helvesec/rmux)
**Stars:** 1,799 | **Last updated:** 2026-06-19 (pushed; created 2026-05-15) | **License:** MIT OR Apache-2.0 (dual; GitHub reports NOASSERTION because of the dual SPDX) | **Releases:** 10
**Dev loop stage:** Implement / Agent Orchestration (a programmable multiplexer for driving agents and CLIs)
**Layer:** Infrastructure (Rust multiplexer + typed Rust/Python SDKs)

---

## What it does

RMUX is a **modern async Rust terminal multiplexer** built for "local shells, long-running agents, typed automation, and browser-shared terminal sessions." It implements **90+ tmux commands natively across Linux, macOS, and Windows — no WSL needed** — and, crucially, ships a **public typed Rust SDK** (plus an official Python SDK, `librmux`) so you can **drive any CLI or TUI app from code**, not just from a keybinding.

Use it three ways: from the **CLI** (tmux-like), from **Rust/Python** (typed automation), or via **Web Share** — share a pane or session in a browser with **hybrid post-quantum end-to-end encryption**, while keeping terminal execution local. It has native **Ratatui** integration for building TUIs on top of it. The README's own demo list is agent-centric: "Multi Agents Orchestration," "Agent Broadcast Arena," "Terminal Automation," "Mini-Zellij." It carries an **OpenSSF Best Practices** badge and a restricted-`unsafe` policy.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No build, no session, no SDK call. Claims come from the repository (GitHub metadata, README, badges, demo descriptions, 10 releases) — the project's own documentation, not observed behavior.

```bash
gh api repos/Helvesec/rmux --jq '{stars,created_at,pushed_at,lang:.language}'   # license shows NOASSERTION (dual)
gh api repos/Helvesec/rmux/readme --jq '.content' | base64 -d   # SDK, web-share, 90+ tmux cmds, demos
gh api repos/Helvesec/rmux/releases --jq 'length'             # 10
```

## What worked

- **Typed SDK is the real differentiator.** Driving terminals/agents from Rust or Python with a typed API (rather than scripting `tmux send-keys` and scraping output) is exactly what programmatic multi-agent orchestration needs — closer to sandcastle's "control agent sessions from code," but at the multiplexer layer and language-native.
- **True cross-platform, no WSL.** Native Windows support for a tmux-equivalent is genuinely uncommon and valuable; 90+ tmux commands eases migration.
- **Web Share with post-quantum E2E encryption** is a thoughtful, security-forward take on remote/shared terminals while keeping execution local — useful for monitoring long-running agents.
- **Quality signals are strong.** OpenSSF Best Practices badge, restricted-`unsafe` policy, CI, multilingual docs, Rust + Ratatui — this reads as a serious, security-conscious project, not a weekend tool.
- **Permissive dual license** (MIT OR Apache-2.0) — clean for adoption.

## What didn't work or surprised us

- **Young, pre-1.0.** Created mid-May 2026, version ~0.6.1 — APIs (and the SDK surface you'd build against) may still churn; pin versions.
- **It's plumbing, not an agent.** RMUX orchestrates/drives terminals; it produces no code review, tests, or agent intelligence itself. Value is realized only when you build automation on top of it.
- **Adoption cost vs. incumbent tmux.** Teams deep in tmux/zellij configs need a reason to switch; the typed SDK and Windows-native support are that reason, but it's still a substrate change.
- **License auto-detection caveat.** GitHub reports NOASSERTION (because of the dual-SPDX expression); the actual grant is MIT OR Apache-2.0 per the LICENSE files — fine, but worth confirming in your own compliance scan.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Typed SDK makes agent-driving automation less error-prone than string-scraping `tmux send-keys`; doesn't affect agent output itself. |
| Speed | + | Programmatic, cross-platform orchestration of many sessions/agents from code; native (no WSL) on Windows. |
| Maintainability | + | Typed automation is more maintainable than shell-scraping multiplexer hacks. |
| Safety | + | Post-quantum E2E web sharing with local execution; OpenSSF Best Practices + restricted-`unsafe` policy. |
| Cost Efficiency | neutral | Free/OSS; infrastructure, not a token consumer. |

## Verdict

**CONDITIONAL** — adopt if you're **building** multi-agent or terminal automation and want to drive sessions from typed Rust/Python code rather than scripting tmux, especially if you need native Windows support or secure browser-shared terminals. The typed SDK + cross-platform (no-WSL) + post-quantum web-share + OpenSSF posture make it a standout *substrate* for agent orchestration. Hold off if you just want to *use* a multiplexer interactively (tmux/zellij already do that and are battle-tested) or need a stable 1.0 API — it's young and pre-1.0. This is a builder's tool: its payoff is in the automation you write on top of it.

Compared to neighbors: **dmux** is a lightweight worktree-based agent multiplexer (use-focused); **claude-squad** manages parallel agent sessions in a TUI; **sandcastle** orchestrates sandboxed agents programmatically in TypeScript. RMUX is the **language-native, typed multiplexer SDK** — the programmable terminal substrate you'd build a sandcastle-like or claude-squad-like orchestrator *on*, with first-class Windows and secure web sharing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [rmux](https://github.com/Helvesec/rmux) | tool | Async Rust terminal multiplexer (90+ tmux cmds, native on Linux/macOS/Windows, no WSL) with typed Rust/Python SDKs to drive any CLI/TUI from code, plus post-quantum E2E browser session sharing | Orchestrating long-running agents/terminals programmatically means brittle `tmux send-keys` scraping; want a typed, cross-platform SDK to drive sessions from code | dmux, claude-squad, sandcastle |
