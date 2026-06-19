# Evaluation: OpenHands

**Repo:** [All-Hands-AI/OpenHands](https://github.com/All-Hands-AI/OpenHands)
**Stars:** 77,739 | **Last updated:** 2026-06-19 | **License:** MIT (enterprise/ directory separate)
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Self-hosted developer control center for coding agents and automations. OpenHands Agent Canvas is a web UI that connects to one or more "agent backends" — local, Docker, VM, or cloud — and runs the OpenHands agent, Claude Code, Codex, Gemini, or any ACP-compatible agent. The platform includes an automation server for scheduled/webhook-triggered tasks (GitHub issue decomposition, Slack reports, dependency updates) and a multi-backend architecture that lets you switch between personal and shared agent servers from one frontend.

Originally "OpenDevin" (a Devin clone), it has evolved into an agent orchestration platform. The codebase is splitting: `OpenHands/software-agent-sdk` (agent + agent server) and `OpenHands/agent-canvas` (frontend + automation). The main repo now serves as the migration hub.

## How we tested it

Architecture review based on README, repo structure, AGENTS.md, release history, and the split-repo transition. Not hands-on tested — the platform is a full replacement for Claude Code, not a complement, so installing it would mean running a parallel agent environment.

```
gh api repos/All-Hands-AI/OpenHands --jq '.stargazers_count, .updated_at, .license.spdx_id'
gh api repos/All-Hands-AI/OpenHands/contents/AGENTS.md --jq '.content' | base64 -d
gh api repos/OpenHands/software-agent-sdk --jq '.stargazers_count, .description'
gh api repos/OpenHands/agent-canvas --jq '.stargazers_count, .description'
```

Assessed release cadence (v1.6.0 → v1.7.0 → v1.8.0 over 3 months), community size (9,879 forks, 328 open issues), and architectural evolution from single-agent to multi-backend platform.

## What worked

- **Multi-backend architecture** is genuinely novel: one UI connects to local, Docker, VM, or cloud agent servers. You can run personal agents on your laptop and shared review agents on a team server, switching between them from the same frontend.
- **ACP (Agent-Client Protocol)** support means it's not locked to one agent — Claude Code, Codex, Gemini, and custom agents all work through the same interface.
- **Automation server** with scheduled/webhook triggers fills a gap that pure CLI agents like Claude Code don't cover — e.g., daily dependency update agents, GitHub issue decomposition on creation.
- **Active development**: monthly major releases, 77.7K stars, MIT license, Linux Foundation backing through the OpenHands org.

## What didn't work or surprised us

- **Codebase in transition**: splitting across 3 repos (main, software-agent-sdk, agent-canvas) means the developer experience is fragmented. `agent-canvas` has only 86 stars — community hasn't followed the migration yet.
- **Full platform replacement**: this replaces your agent environment, not augments it. You can't use OpenHands features from within a Claude Code session. It's an either/or platform choice.
- **No built-in methodology**: unlike Claude Code + superpowers (TDD enforcement, verification gates, systematic debugging), OpenHands provides the runtime but not the engineering process. You'd need to build that yourself through skills or AGENTS.md.
- **Heavy infrastructure**: Docker sandbox mode requires Docker Desktop, project path mounting, and port management. The no-sandbox mode gives agents full filesystem access with a warning banner.
- **Enterprise license split**: the `enterprise/` directory has a separate non-MIT license, which means some features are commercially restricted despite the MIT branding.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Agent quality depends on the underlying model, not the platform |
| Speed | + | Multi-backend lets you run agents on faster hardware; automations run unattended |
| Maintainability | neutral | No methodology built in; you bring your own engineering process |
| Safety | +/- | Docker sandbox adds isolation; no-sandbox mode is dangerously permissive; no built-in guardrails like agentlint |
| Cost Efficiency | + | Self-hosted means no per-seat SaaS fees; but infrastructure costs replace them |

## Verdict

**CONDITIONAL**

Use OpenHands when you need a self-hosted agent orchestration platform with multi-backend support, automation triggers (scheduled/webhook), or ACP-compatible multi-agent management — especially for team environments where agents need to run on shared infrastructure. Choose Claude Code directly when you want the deepest ecosystem (skills, plugins, marketplace, hooks), structured methodology (superpowers, agent-skills), and the simplest setup (single CLI, no Docker required). Like goose and opencode, this is a platform choice, not a complement. Skills (SKILL.md format) are portable between platforms.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenHands](https://github.com/All-Hands-AI/OpenHands) | platform | Self-hosted agent control center — multi-backend, multi-agent, automations (77.7K stars) | Want a full AI dev platform with scheduled automations and team agent servers | claude-squad, goose, opencode |
