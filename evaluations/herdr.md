# Evaluation: herdr

**Repo:** [ogulcancelik/herdr](https://github.com/ogulcancelik/herdr)
**Stars:** 6,412 | **Last updated:** 2026-06-20 (pushed) | **License:** see repo (no SPDX detected) | **Language:** Go/Rust (terminal app)
**Dev loop stage:** Agent Orchestration — multi-agent terminal multiplexer
**Layer:** Tooling (terminal multiplexer, `curl | sh` install)

---

## What it does

herdr is **"an agent multiplexer that lives in your terminal."** It gives you **workspaces, tabs, and panes** for running many coding agents at once, **mouse-native** (click, drag, split), with **every agent at a glance** — blocked, working, or done. You can **detach and reattach** and the agents keep running. Its explicit anti-pitch: "no GUI app, no Electron, no mac-only native wrapper — you see the agent's own terminal, not someone's interpretation of it." Install via `curl -fsSL https://herdr.dev/install.sh | sh` (Homebrew and a Windows preview also available).

## How we tested it

**Source-grounded inspection — not installed, not run.** No agents multiplexed.

```bash
gh api repos/ogulcancelik/herdr --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 6412, NOASSERTION, pushed 2026-06-20
gh api repos/ogulcancelik/herdr/readme --jq '.content' | base64 -d | head -30               # multiplexer, workspaces/tabs/panes, detach/reattach
```

## What worked

- **The right model for the "many agents" era.** As running 5–10 concurrent agents becomes normal, a terminal multiplexer purpose-built for them (status at a glance: blocked/working/done) is genuinely useful — it's tmux reimagined around agent supervision.
- **Mouse-native in the terminal.** Click/drag/split panes is a real ergonomics win over raw tmux for managing parallel agents.
- **Shows the real terminal.** Not an Electron reinterpretation — you see each agent's actual output, which matters for trust and debugging. The "no GUI/Electron" stance is a deliberate, defensible design.
- **Detach/reattach with agents still running.** Sessions survive disconnects — important for long-running/overnight agent work.
- **Cross-platform, easy install.** macOS/Linux + Windows preview; one-line install; 6.4K stars fast.

## What didn't work or surprised us

- **License unclear.** GitHub detects no standard SPDX license (NOASSERTION) — confirm terms before any non-personal/redistribution use.
- **Crowded multiplexer niche.** Overlaps claude-squad, dmux, rmux, agent-of-empires, and even claude-fleet/ping-island (observability angle). The wedge is mouse-native panes + "real terminal, no Electron," not a new capability.
- **Supervision, not orchestration.** It multiplexes/displays agents; it doesn't coordinate them (no shared task graph or handoffs) — pair with a work-ledger (beads) or orchestrator if you need coordination.
- **`curl | sh` install.** Standard for this class but a trust step; verify the script.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change agent output; seeing real terminals helps you catch problems sooner. |
| Speed | + | Manage many parallel agents from one view; spot blocked/done instantly instead of checking each. |
| Maintainability | neutral | Lightweight terminal tool; no project state. |
| Safety | neutral | `curl\|sh` install + unclear license are caveats; local-only otherwise. |
| Cost Efficiency | neutral | Free tool; doesn't affect token spend directly. |

## Verdict

**CONDITIONAL** — herdr is a sharp, fast-growing **terminal multiplexer purpose-built for supervising many coding agents**: workspaces/tabs/panes, mouse-native, real terminals (no Electron), detach/reattach with agents alive. Adopt it if you routinely run several agents at once and want tmux-grade control with agent-aware status and pane ergonomics, in your terminal rather than a GUI. It's CONDITIONAL because the license is undeclared (resolve before team/redistribution use) and it's *supervision*, not *orchestration* — it shows and arranges agents but doesn't coordinate their work. Against claude-squad/dmux/rmux, its edge is mouse-native panes and the "see the real terminal" philosophy.

Compared to neighbors: **claude-squad** is a TUI for parallel agent sessions; **dmux**/**rmux** are tmux-based agent runners; **orca** is a worktree-isolated multi-agent ADE; **claude-fleet** is a read-only dashboard. herdr's distinguishing pitch is **a mouse-native, Electron-free terminal multiplexer that shows each agent's real terminal at a glance.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [herdr](https://github.com/ogulcancelik/herdr) | tool | Terminal agent multiplexer — workspaces/tabs/panes, mouse-native (click/drag/split), every agent's real terminal at a glance (blocked/working/done), detach/reattach with agents still running; no GUI/Electron | Running many coding agents at once, you can't see who's blocked or done without an Electron wrapper hiding the real terminal | claude-squad, dmux, rmux, orca, agent-of-empires |
