# Evaluation: CLIProxyAPI

**Repo:** [router-for-me/CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI)
**Stars:** 37,921 | **Last updated:** 2026-06-20 (pushed) | **License:** MIT | **Language:** Go
**Dev loop stage:** Dev Workflow (infrastructure — API gateway in front of coding-agent CLI accounts)
**Layer:** Infrastructure (proxy server; local or multi-account)

---

## What it does

CLIProxyAPI is a **proxy server that exposes OpenAI / Gemini / Claude / Codex / Grok-compatible API endpoints in front of coding-agent CLI accounts**. You log in once via OAuth (Claude Code, OpenAI Codex/GPT, Gemini, Grok), and CLIProxyAPI lets any OpenAI/Gemini/Claude-compatible client or SDK call those models through a standard HTTP API — including OpenAI Responses-style endpoints — using local or multi-account CLI access rather than a metered API key.

In effect it turns a CLI subscription (or several, load-balanced across accounts) into a generic, drop-in API surface that arbitrary tools, scripts, and SDKs can target.

## How we tested it

**Source-grounded inspection — not installed, not run.** No proxy started, no OAuth login performed, no model called through it. Behavior is taken from the repository README and metadata, not observed.

```bash
gh api repos/router-for-me/CLIProxyAPI --jq '{stars,license:.license.spdx_id,lang:.language,pushed:.pushed_at}'   # 37.9K, MIT, Go
gh api repos/router-for-me/CLIProxyAPI/readme --jq '.content' | base64 -d | head -60   # OpenAI/Gemini/Claude/Codex/Grok-compatible endpoints, OAuth, multi-account
```

## What worked

- **One compatibility surface over many CLIs.** Exposing OpenAI/Gemini/Claude/Codex/Grok behind a single OpenAI-compatible API means existing SDKs and tools work unchanged against whichever account you're authenticated to.
- **OAuth + multi-account.** Logging in via OAuth (no raw API key) and load-balancing across multiple accounts is genuinely useful for development throughput and for tools that only speak one provider's API.
- **Single Go binary**, MIT-licensed, very popular (~38K stars) and actively pushed.
- **Responses-endpoint support** and Codex/Claude-Code-via-OAuth coverage make it broad enough to slot under most agent tooling.

## What didn't work or surprised us

- **Squarely in ToS gray-area.** Re-exposing a subscription CLI (Claude Code, Codex, Gemini) as a general API that other clients consume can conflict with each provider's terms of service. The README is also wall-to-wall sponsored "relay"/account-reseller services, which signals the surrounding ecosystem is about cheap subscription arbitrage — a posture to weigh carefully.
- **Not part of a quality dev loop per se.** It's access/cost infrastructure, not a tool that improves correctness, review, or maintainability of the code you ship.
- **Operational + security surface.** Running an OAuth-holding proxy that brokers your model accounts is a credential and availability surface to secure and maintain.
- **Overlaps claude-code-router conceptually** but at a different layer — router customizes Claude Code's routing while inheriting upstream; CLIProxyAPI fronts CLI accounts as a generic multi-provider API.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Pure transport/compat layer — it doesn't change model outputs, only how they're reached. |
| Speed | neutral / + | Multi-account load-balancing can raise throughput / dodge per-account limits during heavy dev. |
| Maintainability | neutral / − | Single Go binary is simple, but it's another always-on service (and an OAuth/credential store) to run and patch. |
| Safety | − | ToS gray-area; holds OAuth credentials for model accounts and brokers them to arbitrary clients — a real governance/security surface. |
| Cost Efficiency | + / neutral | Reuses CLI-subscription access instead of metered API keys — the core appeal, subject to provider ToS. |

## Verdict

**CONDITIONAL** — CLIProxyAPI is a popular, MIT-licensed Go proxy that turns coding-agent CLI accounts (Claude Code, Codex, Gemini, Grok) into a single OpenAI/Gemini/Claude-compatible API via OAuth, with multi-account load-balancing. It's genuinely useful when you need to drive a CLI subscription from arbitrary SDKs/tools or pool several accounts for development throughput. But it sits in **provider-ToS gray-area** (re-exposing subscription access as a general API), its README ecosystem is dominated by subscription-arbitrage relay sponsors, and it adds a credential-holding always-on service rather than improving any quality signal of the code you ship. Adopt only with a clear, ToS-compatible reason; keep it out of the critical path of production work.

Compared to neighbors: **claude-code-router** customizes how you interact with Claude Code while inheriting upstream updates (a routing/extension layer on one agent); CLIProxyAPI is a **multi-provider API gateway fronting CLI accounts**. Both are access/infrastructure rather than dev-loop quality tools.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CLIProxyAPI](https://github.com/router-for-me/CLIProxyAPI) | tool | Go proxy exposing OpenAI/Gemini/Claude/Codex/Grok-compatible API endpoints over coding-agent CLI accounts via OAuth, with multi-account load-balancing (⚠️ provider-ToS gray-area) | Coding-agent CLI subscriptions are locked to their own clients; want to reach them from any SDK/tool through a standard API | claude-code-router |
