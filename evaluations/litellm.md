# Evaluation: LiteLLM

**Repo:** [BerriAI/litellm](https://github.com/BerriAI/litellm)
**Stars:** 50,931 | **Last updated:** 2026-06-20 (pushed) | **License:** MIT | **Language:** Python (PyPI: `litellm`; YC W23)
**Dev loop stage:** Dev Workflow / infrastructure — LLM gateway/proxy (Implement)
**Layer:** Infrastructure (Python SDK + self-hosted Proxy Server)

---

## What it does

LiteLLM is **an open-source AI Gateway: "call any LLM in OpenAI format."** Two shapes: a **Python SDK** that normalizes 100+ providers (OpenAI, Anthropic, Bedrock, Vertex, Azure, Gemini, Ollama, and many more) to the OpenAI request/response format, and a self-hostable **Proxy Server (AI Gateway)** that puts a single OpenAI-compatible endpoint in front of all of them with **routing, fallbacks, retries, load-balancing, budgets and rate-limits, virtual keys, caching, and spend tracking/logging**. Enterprise tier and hosted proxy exist; core is MIT and self-hostable (Docker, Render/Railway one-click).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No proxy deployed, no providers routed.

```bash
gh api repos/BerriAI/litellm --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 50931, MIT, pushed 2026-06-20
gh api repos/BerriAI/litellm/readme --jq '.content' | base64 -d | head -45               # AI Gateway, 100+ LLMs, OpenAI format, proxy
```

## What worked

- **The de-facto LLM gateway.** 50K+ stars, YC-backed, used across the ecosystem; its absence from the catalog was a real gap. "One OpenAI-format API for everything" removes a huge amount of per-provider glue.
- **SDK *and* proxy.** Use the library in-process, or run the proxy as shared infra so every tool/agent hits one endpoint with centralized keys, budgets, and logging — the standard way teams add cost control + observability.
- **Operational features that matter at scale.** Routing, fallbacks, retries, rate-limits, virtual keys, caching, spend tracking — the things you otherwise build yourself once you have >1 provider or >1 consumer.
- **Self-hostable + open core.** MIT core, Docker deploy; no lock-in to start.
- **Massive provider coverage + active.** 100+ providers, pushed daily.

## What didn't work or surprised us

- **Infrastructure for LLM apps, not the coding loop directly.** It's a gateway your agents/apps call; relevant to this catalog as the multi-provider routing/cost layer, not a coding tool itself (peers: claude-code-router, CLIProxyAPI).
- **Operational surface.** Running the proxy in prod (HA, key management, DB for logs/budgets) is real infra; the SDK is lighter but the gateway is a service to operate.
- **Abstraction leak risk.** Normalizing 100+ providers to one format means provider-specific features sometimes need passthrough/escape hatches; broad surface = sharp edges on the long tail.
- **Open-core upsell.** Enterprise tier gates some features; core is MIT but the smoothest managed path is hosted.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't change model quality; consistent API + fallbacks reduce integration bugs. |
| Speed | + / neutral | One integration for all providers; caching helps; the proxy adds a network hop. |
| Maintainability | + | One OpenAI-format API + centralized keys/routing instead of per-provider code. |
| Safety | + | Virtual keys, budgets, rate-limits, and centralized logging give governance over LLM access. |
| Cost Efficiency | + | Spend tracking, budgets, caching, and routing/fallbacks directly control multi-provider cost. |

## Verdict

**CONDITIONAL** — LiteLLM is the **standard open-source LLM gateway**, and a clear catalog gap now filled. Adopt it whenever you call more than one provider (or want one consumer-facing OpenAI-format endpoint with centralized keys, budgets, routing, and spend tracking) — as a library for in-process normalization, or as the self-hosted Proxy Server for shared, governed, observable LLM access across your tools and agents. For *this* catalog it's CONDITIONAL because it's the multi-provider plumbing beneath agentic apps rather than a coding tool; for teams running agents against several models it's close to essential infrastructure. Budget for operating the proxy if you go that route.

Compared to neighbors: **claude-code-router** routes/customizes Claude Code specifically; **CLIProxyAPI** exposes coding-agent CLI accounts over a standard API (ToS gray-area). LiteLLM's distinguishing pitch is **a provider-agnostic OpenAI-format gateway for 100+ LLMs with routing, budgets, keys, and spend tracking.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [litellm](https://github.com/BerriAI/litellm) | tool | Open-source AI gateway (MIT, YC W23) — call 100+ LLM providers (OpenAI, Anthropic, Bedrock, Vertex, Azure, Ollama…) in unified OpenAI format via a Python SDK or self-hosted Proxy Server, with routing/fallbacks, retries, budgets/rate-limits, virtual keys, caching, and spend tracking | Multi-provider LLM apps/agents need one consistent API plus centralized routing, cost control, and observability instead of per-provider glue | claude-code-router, CLIProxyAPI |
