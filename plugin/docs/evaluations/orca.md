# Evaluation: Orca

**Repo:** [stablyai/orca](https://github.com/stablyai/orca)
**Stars:** 5,540 | **Last updated:** 2026-06-20 (pushed; created 2026-03-17) | **License:** MIT | **Platforms:** desktop + iOS/Android
**Dev loop stage:** Agent Orchestration (an "ADE" — agent development environment)
**Layer:** Harness / platform (GUI app that hosts many coding agents)

---

## What it does

Orca is an **ADE (Agent Development Environment) for working with a fleet of parallel agents** — "run any coding agent with your own subscription," on desktop and mobile. It hosts **Codex, Claude Code, OpenCode, or Pi side-by-side**, each in its own git worktree, tracked in one place. Standout features:

- **Parallel worktrees** — fan one prompt across five agents, each in an isolated git worktree, then compare results and merge the winner.
- **Mobile companion** — monitor and steer agents from your phone; get notified when one finishes and send follow-ups from anywhere.
- **Terminal splits** — Ghostty-class WebGL terminals with infinite splits and scrollback that survives restarts.
- **Design Mode** — click any element in a real Chromium window to send its HTML/CSS + a cropped screenshot straight into the agent's prompt.
- **Native GitHub & Linear** — browse PRs, issues, and boards in-app and open a worktree from any task.

## How we tested it

**Source-grounded inspection — not installed, not run.** No desktop/mobile app installed, no agents launched. Features come from the README, docs links, and app-store listings, not observed usage.

```bash
gh api repos/stablyai/orca --jq '{stars,license:.license.spdx_id,created:.created_at,pushed:.pushed_at}'   # 5.5K, MIT
gh api repos/stablyai/orca/readme --jq '.content' | base64 -d | head -25   # ADE, parallel worktrees, mobile, design mode, GitHub/Linear
```

## What worked

- **Worktree fan-out + merge-the-winner is the right primitive.** Running one prompt across several agents in isolated worktrees and comparing/merging is exactly how to exploit parallel agents without them clobbering each other — and it's a first-class feature, not a bolt-on.
- **Agent-agnostic.** Hosting Codex, Claude Code, OpenCode, and Pi together (BYO subscription) means it's an environment, not a lock-in.
- **Genuinely novel surfaces.** Mobile steer-from-phone and Design-Mode (click a UI element → HTML/CSS/screenshot into the prompt) are differentiated capabilities the catalog's TUI tools don't offer.
- **Native GitHub/Linear + WebGL terminals** make it a plausible primary workspace, not just a monitor. MIT, ~5.5K stars, pushed daily.

## What didn't work or surprised us

- **Heavyweight GUI environment.** It's a desktop/mobile app you adopt as your workspace — a much bigger commitment than a TUI (claude-squad) or a read-only dashboard (claude-fleet). Switching cost is real.
- **Overlaps several catalog tools at once.** Parallel sessions (claude-squad), worktrees (worktrunk), multiplexing (dmux), monitoring (claude-fleet), mobile (happy) — Orca bundles all of it, so the question is whether you want the all-in-one ADE vs. composing lighter tools.
- **Vendor app + mobile + accounts.** A companion mobile app and in-app integrations widen the trust/permission surface; BYO-subscription is good, but it's a product you route work through.
- **Claims unverified.** Smoothness of worktree merge, Design Mode fidelity, and mobile reliability are unverified here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fan-out-and-compare lets you pick the best of N agent attempts rather than trusting one; Design Mode gives precise UI context. |
| Speed | + | Parallel worktrees + one workspace + mobile steering reduce context-switching and idle time across many agents. |
| Maintainability | neutral | Isolated worktrees keep parallel work clean; but adopting a whole ADE is a workflow commitment. |
| Safety | neutral / − | Worktree isolation is good; a GUI app + mobile companion + GitHub/Linear integrations is a broader trust surface. |
| Cost Efficiency | neutral / − | BYO subscription (no markup), but fanning one prompt across 5 agents multiplies token spend per task. |

## Verdict

**CONDITIONAL** — Orca is an ambitious, MIT, agent-agnostic **ADE for running a fleet of coding agents in parallel** — its worktree fan-out ("five agents, compare, merge the winner"), mobile steering, Design Mode, and native GitHub/Linear are genuinely differentiated. Adopt it if you regularly run several agents at once and want one workspace (desktop + phone) to launch, isolate, compare, and merge their work. The trade-off is weight: it's a GUI environment you commit to, overlapping a stack of lighter catalog tools (claude-squad, worktrunk, dmux, claude-fleet, happy) bundled together, and fan-out multiplies token cost. Pilot it as your workspace on a real multi-agent day before switching.

Compared to neighbors: **claude-squad** is a TUI for parallel sessions; **worktrunk** manages worktrees; **dmux** multiplexes; **claude-fleet** monitors; **happy** adds mobile. Orca's distinguishing pitch is the **all-in-one ADE** that unifies fan-out worktrees, multi-agent hosting, Design Mode, and mobile in one app.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [orca](https://github.com/stablyai/orca) | platform | Agent development environment (MIT) for a fleet of parallel agents — run Codex/Claude Code/OpenCode/Pi side-by-side, each in its own git worktree; fan one prompt across agents and merge the winner; WebGL terminals, click-to-context Design Mode, native GitHub/Linear, desktop + mobile companion | Running many coding agents in parallel is fragmented — no single place to launch, isolate, compare, steer (incl. from phone), and merge their work | claude-squad, worktrunk, dmux, claude-fleet, happy |
