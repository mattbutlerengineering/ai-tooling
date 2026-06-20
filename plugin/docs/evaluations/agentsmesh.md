# Evaluation: AgentsMesh

**Repo:** [AgentsMesh/AgentsMesh](https://github.com/AgentsMesh/AgentsMesh)
**Stars:** 2,225 | **Last updated:** 2026-06-19 (pushed; created 2026-02-28) | **License:** BSL-1.1 (Business Source License — source-available, **not** OSI open source)
**Dev loop stage:** Implement (orchestration/control layer for running many agents; touches Ship via MR/PR tracking on tickets)
**Layer:** Infrastructure (self-hosted control plane + runner fleet across machines)

---

## What it does

AgentsMesh is a **self-hosted "AI agent workforce" platform** — a control layer for running *many* coding agents (Claude Code, Codex CLI, Gemini CLI, Aider) across your own machines and directing them from one console. Its thesis: the next 10x isn't a smarter agent, it's running a hundred agents at once and steering them like a team — and what's missing is the orchestration layer that schedules, isolates, keeps-alive, and lets them collaborate.

Core concepts:
- **AgentPod** — one agent's isolated execution environment: a PTY terminal, a Git worktree sandbox (`sandboxes/{pod}/workspace/`), private credentials, its own branch, and a real-time output stream.
- **Runner** — a self-hosted daemon you install on any number of machines; connects to the backend over gRPC+mTLS, advertises capacity (`max_concurrent_pods`), and spawns pods. Code never leaves your infra.
- **Autopilot** — a *control agent* watches a pod and sends the next instruction the moment it goes idle, with iteration caps, decision history, and human takeover/handback — self-healing unattended runs.
- **Mesh & Channel** — bind pods into a topology so they talk over channels with `@mentions`, with a live collaboration graph.
- **Ticket** — a Kanban unit of work bindable to a pod, with progress + MR/PR tracking.

Architecture is a **control-plane / data-plane split**: orchestration over gRPC+mTLS, terminal bytes over a stateless WebSocket **Relay** cluster, so the backend never touches a PTY byte and scales. Server is Go (Backend = Gin+GORM API/auth/PKI; Relay; Runner). Clients are Web, Desktop (Electron), and iOS (SwiftUI), all driven by the same Rust core.

## How we tested it

**Source-grounded inspection — not installed, not run.** No backend/runner deployed, no pods spawned. Claims come from the repository (GitHub metadata, README architecture tables, core-concepts list) — the project's own documentation, not observed behavior.

```bash
gh api repos/AgentsMesh/AgentsMesh --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language,topics}'
gh api repos/AgentsMesh/AgentsMesh/readme --jq '.content' | base64 -d   # problem framing, architecture, concepts
gh api repos/AgentsMesh/AgentsMesh/releases --jq 'length'               # 30
```

## What worked

- **Right architecture for the stated problem.** Control/data-plane split with a stateless Relay for PTY traffic is the standard scalable pattern; it directly answers "the backend bottlenecks on terminal bytes." This is real systems engineering, not a TUI wrapper.
- **Runner fleet = genuine horizontal scale.** Installing runners across many machines with capacity advertisement is the only tool in this neighborhood that actually addresses "100 agents won't fit on one laptop." Self-hosted; code stays on your infra.
- **Per-pod isolation is principled.** Dedicated git worktree sandbox + private credentials + own branch per pod is exactly what prevents concurrent agents from corrupting shared state.
- **Autopilot with guardrails.** Idle-detection control agent with iteration caps, decision history, and human takeover is a thoughtful answer to "long-running agents stall and silently die."
- **gRPC+mTLS with a backend-issued PKI** for runner certs is a serious security posture for a distributed system.

## What didn't work or surprised us

- **BSL-1.1 license, not open source.** This is the headline caveat: Business Source License is source-available with use restrictions (typically a non-compete grant that converts to an open license after a delay). It is **not** OSI-approved open source — adopters must read the license terms (and the README mentions billing/org/team, hinting at a commercial tier). Materially different from the MIT-licensed neighbors.
- **Massive operational surface for solo users.** A backend (API+PKI), a Relay cluster, and runner daemons across machines is a lot of infrastructure to stand up. The entire value proposition is *team scale*; a single developer running a few agents is far better served by claude-squad or agent-of-empires.
- **Young.** Created late Feb 2026; the distributed-systems ambition is high and longevity/stability under real load is unproven from the outside.
- **Multi-client (Web/Electron/iOS) is a lot of surface to keep coherent** — capability breadth that also widens the maintenance and bug surface.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Per-pod worktree+credential isolation prevents cross-agent state corruption; Autopilot decision history aids auditing. Doesn't change individual agent output. |
| Speed | + | Horizontal scheduling across a runner fleet + Autopilot keeping pods unblocked is the throughput story for many-agent teams. |
| Maintainability | neutral | Affects fleet orchestration, not your codebase. |
| Safety | + / − | mTLS + PKI + per-pod isolation are strong (+); a self-hosted distributed control plane exposing terminals is a large surface to secure, and BSL licensing constrains use (−). |
| Cost Efficiency | − / neutral | Free to self-host but heavy infra; spends your own provider tokens; possible commercial tier implied by billing components. |

## Verdict

**CONDITIONAL** — adopt if you are a **team** that genuinely needs to run dozens-to-hundreds of agents across multiple self-hosted machines and wants a real control plane (scheduling, isolation, Autopilot, mesh collaboration) rather than a session-manager TUI. The architecture is sound and uniquely addresses horizontal scale. **Skip for solo or small use**: the infra burden is large, the value only materializes at team scale, and the BSL-1.1 license means you must vet usage terms before depending on it — unlike its MIT-licensed neighbors.

Compared to neighbors: **claude-squad** and **agent-of-empires** manage parallel sessions on *one* machine (TUI-centric); **Nimbalyst** is a visual single-user workspace; **lobehub** is an agent-ops platform with scheduling/reporting. AgentsMesh is the distinct **multi-machine fleet / control-plane** end of the spectrum — the only one here built for horizontal scale, at the cost of operational weight and a non-OSS license.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AgentsMesh](https://github.com/AgentsMesh/AgentsMesh) | platform | Self-hosted control plane to run 100+ coding agents across your own machines — runner fleet, per-pod git-worktree isolation, Autopilot, mesh collaboration (BSL-1.1, not OSS) | One operator can't schedule, isolate, keep-alive, and steer a fleet of agents across many machines from one console | claude-squad, agent-of-empires, lobehub, OpenHands |
