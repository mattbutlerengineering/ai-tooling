# Evaluation: herdr

**Repo:** [herdrdev/herdr](https://github.com/herdrdev/herdr) (moved from `ogulcancelik/herdr`)
**Stars:** 24,375 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0 | **Language:** Go/Rust (terminal app)
<!-- repo renamed; metadata refreshed 2026-08-04 (#280). Eval content not re-checked — see Last verified. -->
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Agent Orchestration — multi-agent terminal multiplexer
**Layer:** Tooling (terminal multiplexer, `curl | sh` install)

---

## What it does

herdr is **"an agent multiplexer that lives in your terminal."** It gives you **workspaces, tabs, and panes** for running many coding agents at once, **mouse-native** (click, drag, split), with **every agent at a glance** — blocked, working, or done. You can **detach and reattach** and the agents keep running. Its explicit anti-pitch: "no GUI app, no Electron, no mac-only native wrapper — you see the agent's own terminal, not someone's interpretation of it." Install via `curl -fsSL https://herdr.dev/install.sh | sh` (Homebrew and a Windows preview also available).

## How we tested it

**Evidence:** REVIEW

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

**discovery-log — tentative read** — herdr is a sharp, fast-growing **terminal multiplexer purpose-built for supervising many coding agents**: workspaces/tabs/panes, mouse-native, real terminals (no Electron), detach/reattach with agents alive. Adopt it if you routinely run several agents at once and want tmux-grade control with agent-aware status and pane ergonomics, in your terminal rather than a GUI. It's CONDITIONAL because the license is undeclared (resolve before team/redistribution use) and it's *supervision*, not *orchestration* — it shows and arranges agents but doesn't coordinate their work. Against claude-squad/dmux/rmux, its edge is mouse-native panes and the "see the real terminal" philosophy.

Compared to neighbors: **claude-squad** is a TUI for parallel agent sessions; **dmux**/**rmux** are tmux-based agent runners; **orca** is a worktree-isolated multi-agent ADE; **claude-fleet** is a read-only dashboard. herdr's distinguishing pitch is **a mouse-native, Electron-free terminal multiplexer that shows each agent's real terminal at a glance.**

## Triage note

Left at `discovery-log`, not SKIPped — and escalated as the one genuine head-to-head in this
cluster.

Its overlap with [`claude-squad`](https://github.com/smtg-ai/claude-squad) (STACK, `RUN`, AGPL-3.0, ★8.1K) is as direct as this band ever sees: supervise many coding agents from a
terminal, detach and reattach with them still running. Its evaluation is precise about the delta —
*"it's supervision, not orchestration"*, with mouse-native panes and a see-the-real-terminal
philosophy as the edge.

The reason that is an escalation rather than a SKIP is the comparison, which changed materially
during this pass. herdr reached the band with **no metadata record** (`license=None, stars=None`),
and the evaluation was written when the licence read as undeclared — the fact it treated as the
main blocker. A live fetch shows **Apache-2.0, ★24.4K, pushed today**, against an incumbent that is
AGPL-3.0, ★8.1K and last pushed 2026-06-17. The challenger is three times the adoption, more
permissively licensed, and more actively maintained than the tool it would replace. Those records
are now written to `repo-metadata.json`.

That is a replacement candidate, and a bulk lane may not conclude either way — a SKIP would dispose
the strongest entry in the cluster on stale facts. What a P0 read must settle: whether supervision
without orchestration is enough, and whether the pane ergonomics survive contact with a real fleet.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [herdr](https://github.com/herdrdev/herdr) | tool | Terminal agent multiplexer — workspaces/tabs/panes, mouse-native (click/drag/split), every agent's real terminal at a glance (blocked/working/done), detach/reattach with agents still running; no GUI/Electron | Running many coding agents at once, you can't see who's blocked or done without an Electron wrapper hiding the real terminal | claude-squad, dmux, rmux, orca, agent-of-empires |
