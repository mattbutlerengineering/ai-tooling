# Evaluation: Agent Orchestrator

**Repo:** [AgentWrapper/agent-orchestrator](https://github.com/AgentWrapper/agent-orchestrator) (ComposioHQ)
**Stars:** 7,600 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A fleet management platform for parallel AI coding agents. Each issue or task gets its own agent spawned in an isolated git worktree with its own branch and PR. A central orchestrator agent uses the `ao` CLI to manage sessions while a web dashboard (`localhost:3000`) provides real-time visibility. The key differentiator is the **reaction system** — CI failures, review comments, and PR approvals are automatically routed back to the agent that owns the PR, without human intervention.

Agent-agnostic (Claude Code, Codex, Aider, Cursor, OpenCode, KimiCode, Grok), runtime-agnostic (tmux, ConPTY, Docker), and tracker-agnostic (GitHub, Linear, GitLab). Seven plugin slots with clean TypeScript interfaces: Runtime, Agent, Workspace, Tracker, SCM, Notifier, Terminal.

## How we tested it

**Evidence:** REVIEW

Architecture review via GitHub API — examined the monorepo structure (`packages/core`, 25 plugin implementations, `packages/web`), CLAUDE.md, ARCHITECTURE.md, and key source files (`lifecycle-status-decisions.ts`, `feedback-tools.ts`, `code-review-manager.ts`). Did not install and run locally.

```bash
gh api repos/AgentWrapper/agent-orchestrator --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api "repos/AgentWrapper/agent-orchestrator/contents/packages/plugins" --jq '.[].name'
gh api "repos/AgentWrapper/agent-orchestrator/contents/packages/core/src/lifecycle-status-decisions.ts" --jq '.content' | base64 -d | head -80
```

## What worked

- **Reaction system is real, not vaporware.** `lifecycle-status-decisions.ts` implements a state machine with `ProbeState` (alive/dead/unknown), CI status tracking, PR review decision routing, and retry logic (`DETECTING_MAX_ATTEMPTS = 3`, 5-minute escalation timeout). When CI fails, the agent gets logs and attempts a fix; when reviews are requested, the agent addresses comments; escalation to human happens after configurable timeout.
- **Plugin architecture is genuinely well-engineered.** 25 plugin implementations across 7 slots, all implementing clean TypeScript interfaces from `packages/core/src/types.ts`. Adding a new agent backend (e.g., Grok) or tracker (e.g., GitLab) is one interface implementation.
- **Production-grade infrastructure.** 3,288 test cases, Zod-validated config with JSON Schema, atomic file writes, dedup keys for feedback, hash-based directory namespacing, gitleaks secret scanning in hooks.
- **Worktree isolation per agent prevents the merge conflict problem.** Each agent works on its own branch in its own worktree — no shared state, no conflicts until PR merge time.

## What didn't work or surprised us

- **Not tested hands-on.** Architecture review only — no evidence of actual orchestration behavior, dashboard UX, or failure recovery in practice.
- **Heavy install footprint.** Requires Node.js 20+, Git 2.25+, `gh` CLI, tmux (macOS/Linux), and runs a Next.js 15 dashboard. That's a lot of infrastructure for orchestration.
- **961 open issues** suggests either rapid growth outpacing maintenance or scope creep. The repo was recently forked from ComposioHQ — the governance is still settling.
- **Last stable release v0.9.2 was May 23** — over 3 weeks old with many commits since. The nightly cadence suggests the stable channel lags significantly.
- **No auto-merge by default** (and good reason) — but the `approved-and-green.auto: true` config exists for brave users.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | CI failure reaction loop catches and fixes regressions automatically |
| Speed | ++ | Parallel agents on separate issues; reaction system eliminates human wait time for CI/review routing |
| Maintainability | neutral | Well-structured plugin system, but the platform itself is complex to maintain |
| Safety | +/- | Worktree isolation is good; autonomous CI fixing and review responses need careful trust calibration |
| Cost Efficiency | - | Runs multiple agents simultaneously; each agent session burns tokens independently |

## Verdict

**CONDITIONAL**

Use when you have 5+ parallel issues to work on and want automated CI-fix and review-routing feedback loops. The reaction system is the genuine differentiator — no other tool in the catalog closes the CI-fail → agent-fix → re-run loop automatically. Choose claude-squad (KEEP) for simpler parallel session management without the reaction system overhead. Choose superpowers (ADOPT) if you work one task at a time and want methodology, not fleet management.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-orchestrator](https://github.com/AgentWrapper/agent-orchestrator) | tool | Plans tasks, spawns parallel coding agents, handles CI fixes and merge conflicts autonomously | Need automated orchestration of multiple agents with conflict resolution | claude-squad, gastown |
