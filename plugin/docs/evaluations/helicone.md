# Evaluation: Helicone

**Repo:** [Helicone/helicone](https://github.com/Helicone/helicone)
**Stars:** 5,841 | **Last updated:** 2026-06-11 (pushed) | **License:** Apache-2.0 | **Language:** TypeScript (self-hostable + hosted)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Observability — AI gateway + LLM observability
**Layer:** Infrastructure (gateway + observability platform)

---

## What it does

Helicone is **an AI Gateway & LLM Observability platform for AI engineers.** Two halves: an **AI Gateway** (access 100+ models with one API key through the OpenAI API, with intelligent routing and automatic fallbacks) and **observability** added with **one line of code** — log all requests from OpenAI/Anthropic/LangChain/Gemini/Vercel AI SDK and more. Features: **agent/session tracing** (debug agents, chatbots, pipelines), **cost & latency analytics** (export to PostHog), a **playground** for iterating on prompts/sessions/traces, **prompt management** (version prompts on production data, deploy through the gateway without code changes), and **fine-tuning** via partners. SOC 2 + GDPR compliant; generous free tier (10k req/mo, no credit card); self-hostable or hosted.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No requests logged, no gateway configured.

```bash
gh api repos/Helicone/helicone --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 5841, Apache-2.0, pushed 2026-06-11
gh api repos/Helicone/helicone/readme --jq '.content' | base64 -d | head -40               # gateway + observability, one-line logging, sessions, prompts
```

## What worked

- **Gateway + observability fused.** It does what litellm (gateway) and langfuse/opik (observability) do, in one product — one OpenAI-format key for routing/fallbacks *and* one-line request logging with tracing and cost analytics. For teams that want both without stitching two systems, that's compelling.
- **One-line integration.** The headline ease ("one line of code to log all your requests") is a real adoption advantage over instrument-everything tracing.
- **Agent/session tracing + prompt management.** Sessions for agents/chatbots/pipelines, plus version-and-deploy prompts through the gateway without code changes, cover real production needs.
- **Compliance + free tier.** SOC 2/GDPR and a generous no-credit-card free tier ease both enterprise and trial adoption.
- **Self-hostable, Apache-2.0.** No mandatory lock-in.

## What didn't work or surprised us

- **Observes the AI app you build, not the coding agent.** Like langfuse/opik/promptfoo, the object is your LLM product; catalog-relevant as the gateway+obs layer, tangential to authoring code.
- **Double overlap.** It competes with litellm (gateway) *and* langfuse/opik (observability) simultaneously — strong as an all-in-one, but in any single dimension a specialist may go deeper.
- **Hosted gravity.** The smoothest path (free tier, managed dashboards, PostHog export) is hosted Helicone; self-hosting is supported but is real infra.
- **Gateway-in-the-path.** Routing through Helicone's gateway adds a hop and a dependency on its availability (mitigated by fallbacks).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (indirect) | Session tracing + prompt versioning on production data help catch and fix bad LLM behavior. |
| Speed | + | One-line logging + a playground speed debugging/iteration; gateway adds a hop. |
| Maintainability | + | Centralized prompt management + versioning + traces make LLM apps more debuggable. |
| Safety | + | SOC 2/GDPR, gateway-level control; self-hostable for data residency. |
| Cost Efficiency | + | Cost/latency analytics + routing/fallbacks + caching directly manage multi-provider spend. |

## Verdict

**CONDITIONAL** — Helicone is a strong, Apache-2.0 **all-in-one AI gateway + LLM observability** platform: one OpenAI-format key for 100+ models with routing/fallbacks, plus one-line request logging, agent/session tracing, cost analytics, and prompt management. Adopt it when you want **both** multi-provider routing *and* observability/prompt-management in a single tool with a famously easy integration, and you're shipping LLM-powered apps/agents. For this catalog it's CONDITIONAL because it observes the AI product you build rather than the coding agent, and it overlaps litellm (gateway) and langfuse/opik (obs) — choose Helicone for the unified experience, or the specialists for depth. The free tier makes trial cheap; self-host for data control.

Compared to neighbors: **litellm** is the gateway specialist; **langfuse** is tracing/observability + prompt management; **opik** is tracing + eval + optimization; **promptfoo** is eval/red-team. Helicone's distinguishing pitch is **gateway + one-line observability + prompt management unified, with a generous free tier.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Helicone](https://github.com/Helicone/helicone) | platform | Open-source AI gateway + LLM observability (Apache-2.0) — 100+ models via one OpenAI-format key with routing/fallbacks, plus one-line request logging, agent/session tracing, cost/latency analytics, prompt management, and fine-tuning; generous free tier | Want gateway routing AND tracing/cost/prompt observability for LLM apps in one tool, with a one-line integration | litellm, langfuse, opik, promptfoo |
