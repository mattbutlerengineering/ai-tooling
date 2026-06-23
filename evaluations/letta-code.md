# Evaluation: Letta Code

**Repo:** [letta-ai/letta-code](https://github.com/letta-ai/letta-code)
**Stars:** 2,750 | **Last updated:** 2026-06-19 (pushed) | **License:** Apache-2.0 | **Language:** TypeScript (npm: `@letta-ai/letta-code`)
**Dev loop stage:** Agent Harnesses (stateful, self-improving coding agent)
**Layer:** Tooling/Infrastructure (CLI + desktop app + browser + messaging channels)

---

## What it does

Letta Code is a **stateful agent harness** from the creators of [MemGPT](https://arxiv.org/abs/2310.08560) and sleep-time compute ("dreaming"). Agents have **memory, identity, and a sense of experience over time**, and "learn and evolve over long horizons through rewriting their own memory, skills, prompts, and even the harness itself (through mods)." It runs interactively or as always-on/proactive agents, accessible from a local CLI, a desktop app (macOS/Windows/Linux), the browser/mobile at chat.letta.com, and Slack/Telegram/Discord/custom channels.

Distinctive features: **memory blocks** + **skill learning** for self-improvement, periodic `/sleeptime` "dreaming," `/doctor` memory-quality audits, `/palace` memory view, `/search` across all messages/agents, **MemFS** (all context git-tracked, syncable to a GitHub repo), global/project/agent-scoped skills, built-in subagents (general-purpose, forked, recall, history-analyzer), hooks, permissions, crons/heartbeats, and (with Constellation login) remote multi-environment execution + obfuscated secrets.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No agent created, no memory exercised, self-improvement not observed.

```bash
gh api repos/letta-ai/letta-code --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2750, Apache-2.0, pushed 2026-06-19
gh api repos/letta-ai/letta-code/readme --jq '.content' | base64 -d | head -90               # feature table, Constellation, skills install
```

## What worked

- **Memory is the harness, not a bolt-on.** Unlike plugins that add memory to a stateless agent, Letta Code is built around agent-owned memory (memory blocks, MemFS, dreaming) from a team with a research pedigree in exactly this.
- **Git-tracked context (MemFS).** Making all context — including memory blocks — versioned and syncable to GitHub is a genuinely auditable take on agent memory.
- **Self-configuring.** "Ask your agent to configure skills/hooks/permissions for you" lowers the setup cliff most harnesses have.
- **Broad access surface.** Same agent reachable from CLI, desktop, browser/mobile, and chat platforms — strong for always-on/proactive use.
- **Skill portability.** Installs skills from GitHub, ClawHub, and Hermes Skills Hub, so it plugs into the wider skills ecosystem.

## What didn't work or surprised us

- **It is a separate agent, not a Claude Code add-on.** This is its own CLI/harness (BYO LLM keys via `/connect`); adopting it means leaving the Claude Code surface, not enhancing it.
- **Constellation gating.** Remote multi-env and secrets require Constellation login (hosted) — the most "always-on" features lean on Letta's platform.
- **Self-rewriting harness is powerful but opaque.** Agents rewriting their own memory/skills/prompts (and harness mods) is a controllability/auditability surface; MemFS+`/doctor` help but governance matters.
- **Distinct from `letta` (the platform).** Easy to confuse with the existing catalog entry `letta` (the stateful-agents server/SDK); letta-code is the coding-agent harness built on that lineage.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Persistent memory + skill learning + dreaming keep relevant context and learned strategies available across sessions. |
| Speed | + / neutral | Recall avoids re-explaining; always-on agents work proactively. Setting up a new harness has switching cost. |
| Maintainability | neutral | MemFS git-tracking aids auditability; a self-rewriting agent is more to reason about than a static config. |
| Safety | neutral | Permissions/hooks and git-tracked context are good; self-modification + hosted Constellation features need governance. |
| Cost Efficiency | neutral | Apache-2.0, BYO model keys; memory reuse can cut re-derivation; dreaming/always-on consume tokens. |

## Verdict

**CONDITIONAL** — Letta Code is the most credible **memory-first agent harness** in the catalog: an Apache-2.0 CLI/desktop/browser agent from the MemGPT team where memory, identity, and self-improvement (memory blocks, MemFS, skill learning, dreaming) are the core architecture rather than an afterthought. Adopt it if you want a **standing, self-evolving agent** you interact with across CLI/desktop/chat and value git-tracked, auditable memory — and you're willing to run a separate harness (not Claude Code) and govern a self-modifying agent. The deepest "always-on" features (remote multi-env, secrets) require the hosted Constellation login. For Claude-Code-native persistence, `claude-mem`/`claude-subconscious`/OMEGA stay lighter; Letta Code is the choice when the *agent itself* should own and evolve its memory.

Compared to neighbors: **letta** is the platform/SDK for building stateful application agents; **phantom** gives an agent its own VM + durable memory; **ruflo** is a meta-harness with adaptive memory. Letta Code's distinguishing pitch is **a coding agent whose memory, skills, and prompts are git-tracked and self-rewritten over long horizons.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [letta-code](https://github.com/letta-ai/letta-code) | harness | Stateful agent harness from the MemGPT creators (Apache-2.0) — agents with memory blocks, identity, skill learning, sleeptime "dreaming", git-tracked MemFS, subagents, and multi-channel access (CLI/desktop/browser/Slack/Telegram) | Coding agents are stateless tools that forget and don't self-improve; want a harness where the agent rewrites its own memory, skills, and prompts over time | letta, claude-mem, ruflo, phantom, oh-my-openagent |
