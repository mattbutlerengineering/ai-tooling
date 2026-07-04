# Evaluation: DeerFlow

**Repo:** [bytedance/deer-flow](https://github.com/bytedance/deer-flow)
**Stars:** 71,529 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

ByteDance's open-source "super agent harness" — a ground-up v2.0 rewrite of what started as a deep-research framework. DeerFlow orchestrates sub-agents, sandboxed execution environments, persistent memory, skills, and MCP tools into a self-contained runtime for tasks spanning minutes to hours. Built on LangGraph and LangChain, it provides each task with its own filesystem view (uploads, workspace, outputs), isolated sub-agent contexts, aggressive summarization for long context management, and progressive skill loading. Model-agnostic — works with any OpenAI-compatible API including Claude (via OAuth), Codex CLI, GPT-5, DeepSeek, Qwen, and vLLM-hosted models.

The Claude Code integration is a skill (`claude-to-deerflow`) that lets you send research tasks to a running DeerFlow instance from Claude Code, but DeerFlow itself is a separate, standalone service — it doesn't enhance Claude Code directly the way superpowers or compound-engineering do.

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation based on README, repo structure, configuration examples, and the Claude Code integration skill. Did not run the full Docker deployment (requires Python 3.12+, Node.js 22+, Docker, and an LLM API key).

```bash
gh api repos/bytedance/deer-flow --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/bytedance/deer-flow/readme --jq '.content' | base64 -d
```

Examined: setup wizard flow (`make setup`), config.yaml model provider system (8+ provider types including CLI-backed), skill architecture (`/mnt/skills/public/` and `/mnt/skills/custom/`), sandbox modes (AioSandboxProvider vs LocalSandboxProvider), context engineering (isolated sub-agent contexts, summarization, strict tool-call recovery), long-term memory persistence, and embedded Python client.

## What worked

- **Genuine infrastructure, not a wrapper.** Full filesystem, sandboxed execution, sub-agent spawning with scoped contexts, and persistent memory. This is closer to a self-hosted Devin than a Claude Code plugin.
- **Model-agnostic with deep provider support.** Config-driven model selection covering OpenAI, Anthropic (OAuth), OpenRouter, Codex CLI, vLLM, and Responses API. CLI-backed providers read existing auth files (`~/.codex/auth.json`, `~/.claude/.credentials.json`).
- **Progressive skill loading.** Skills load only when needed, keeping context lean. Slash-activation (`/skill-name`) is clean. Skill archives with frontmatter metadata are accepted via the Gateway.
- **Context engineering is production-grade.** Sub-agent isolation, completed-task summarization, tool-call recovery for strict-validation models, and duplicate-deduplication in memory updates.
- **Massive community.** 71.5K stars, #1 on GitHub Trending, multi-language README (EN/ZH/JA/FR/RU), active development with v2.0 ground-up rewrite.

## What didn't work or surprised us

- **Heavyweight deployment.** Docker recommended, Python 3.12+, Node.js 22+, a `make setup` wizard, LangGraph backend, and optional PostgreSQL for checkpointing. Compared to `pip install superpowers` or `claude install-plugin`, this is a significant commitment.
- **Not a Claude Code enhancer.** The `claude-to-deerflow` skill sends tasks to a running DeerFlow instance — it doesn't make Claude Code itself better. You're running two systems (Claude Code + DeerFlow) rather than enhancing one.
- **ByteDance ecosystem pull.** README prominently features Volcengine "Coding Plan" and InfoQuest integrations. Recommended models are Doubao-Seed-2.0-Code, DeepSeek v3.2, and Kimi 2.5 — valid models, but the Claude/GPT support reads as afterthought despite being technically complete.
- **Not tested hands-on.** The Docker/Python/Node setup is too heavy for a quick evaluation pass. Architecture review only.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Sandboxed execution, sub-agent isolation, and strict tool-call recovery reduce error propagation |
| Speed | + | Parallel sub-agent execution and progressive skill loading optimize long-horizon tasks |
| Maintainability | neutral | Well-structured codebase but introduces a separate system to maintain alongside Claude Code |
| Safety | + | AioSandboxProvider for container isolation, host bash disabled by default, security-aware defaults |
| Cost Efficiency | neutral | Context summarization helps, but running a full backend service adds infra cost |

## Verdict

**CONDITIONAL**

Use when you need a self-hosted, model-agnostic super-agent platform for long-horizon tasks (research, report generation, multi-step analysis) that span minutes to hours. DeerFlow is genuinely impressive infrastructure — sandboxed execution, sub-agent orchestration, persistent memory, and 71K-star community support. However, it's a standalone platform that runs alongside Claude Code rather than enhancing it, and the deployment overhead (Docker + Python + Node + LangGraph) is substantial compared to plugin-based alternatives. Choose superpowers (ADOPT) or compound-engineering (CONDITIONAL) if you want to enhance Claude Code directly; choose DeerFlow if you need a full autonomous agent runtime with execution sandboxes.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deer-flow](https://github.com/bytedance/deer-flow) | harness | ByteDance's long-horizon super agent harness with sub-agents, sandboxes, memory, and skills (71K stars) | Need autonomous agent work beyond single-session scope with execution isolation and persistent memory | ralph-claude-code, superpowers, GSD |
