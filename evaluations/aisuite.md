# Evaluation: aisuite

**Repo:** [andrewyng/aisuite](https://github.com/andrewyng/aisuite)
**Stars:** 14,755 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (library for building AI applications)
**Layer:** Infrastructure

---

## What it does

A lightweight Python library providing a unified Chat Completions API across 23 LLM providers plus a first-class Agents API with tools, toolkits, MCP support, tool policies, and state persistence. Model names use `<provider>:<model-name>` format — swap providers by changing one string. Built by Andrew Ng (Stanford, deeplearning.ai).

The library has three layers: (1) Chat Completions API for multi-provider LLM calls, (2) Agents API with `Agent`/`Runner` classes, built-in toolkits (files, git, shell), tool policies, and state stores, (3) OpenCoworker desktop app (a reference harness built on aisuite). MCP tools are first-class — any MCP server can be passed as a tool spec without boilerplate.

## How we tested it

**Evidence:** REVIEW

Architecture review based on repo structure, README, provider implementations, and agent/toolkit APIs. Did not hands-on install or run — aisuite is an application-building library, not a Claude Code extension.

```bash
gh api repos/andrewyng/aisuite --jq '.description, .stargazers_count, .updated_at, .license.spdx_id'
gh api repos/andrewyng/aisuite/git/trees/main:aisuite/providers --jq '.tree[].path'
gh api repos/andrewyng/aisuite/git/trees/main:aisuite/toolkits --jq '.tree[].path'
```

Reviewed: 23 provider adapters, 3 built-in toolkits (files, git, shell), Agents API with Runner/Agent/Tool policies, MCP integration, state store persistence (in-memory, file, Postgres).

## What worked

- **23 provider adapters** covering every major LLM provider including self-hosted (Ollama, LMStudio) — broadest provider support of any lightweight library
- **Tool calling abstraction** with `max_turns` is genuinely simpler than raw SDK tool loops — auto-generates schemas from Python function signatures
- **MCP as first-class citizen** — pass MCP server specs directly as tools, no wrapper code needed
- **Tool policies** (RequireApprovalPolicy, allow/deny lists) address the safety gap most agent libraries ignore
- **State stores** for persisting and resuming agent runs across processes — production-ready pattern

## What didn't work or surprised us

- **Not a coding agent tool** — this is a library for building AI-powered applications, not a tool that enhances your dev workflow. You'd use it to build something like Claude Code, not to extend Claude Code
- **OpenCoworker desktop app** (app-v0.1.1) is the first harness built on it, but it's a general productivity tool, not a coding agent
- **No Claude Code integration** — no plugin, skill, MCP server, or hook. It lives entirely outside the dev loop
- **Library release stale** — the Python library's last release was v0.1.7 in December 2024 (~18 months ago), though the repo is actively developed on main

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Library for building apps, not for improving code quality |
| Speed | neutral | Doesn't affect development speed within Claude Code |
| Maintainability | neutral | No integration with dev workflow tools |
| Safety | neutral | Tool policies are well-designed but apply to apps built with aisuite, not your dev workflow |
| Cost Efficiency | neutral | Provider-swapping enables cost optimization in apps you build, not in your agent sessions |

## Verdict

**SKIP**

aisuite is an excellent library for building multi-provider AI applications — the unified API, tool policies, and MCP integration are well-engineered. But it's a building block for AI products, not a tool that improves your development workflow. It doesn't write code, review PRs, manage context, or integrate with any coding agent. In this catalog's framework (tools that move quality signals in the dev loop), it has no surface area. Use it when building AI-powered applications; it doesn't belong in a dev workflow stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aisuite](https://github.com/andrewyng/aisuite) | framework | Simple unified interface to multiple generative AI providers | Switching between AI providers requires different SDKs and APIs | — |
