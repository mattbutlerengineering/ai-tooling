# Evaluation: crewAI

**Repo:** [crewAIInc/crewAI](https://github.com/crewAIInc/crewAI)
**Stars:** 53,987 | **Last updated:** 2026-06-19 (pushed; created 2023-10-27) | **License:** MIT
**Dev loop stage:** None of ours, by design. CrewAI is a runtime for orchestrating role-playing agents *inside an application you ship* — not a tool that intervenes in the Plan/Implement/Verify/Review/Ship/Reflect loop a developer runs to produce code. It is the engine *of* an agentic product, not an assistant *to* the engineer building one.
**Layer:** Infrastructure / framework (a `pip install crewai` Python library + an "AMP Suite" commercial control plane for hosting/observing the agents it runs)

---

## What it does

The repo description: "Framework for orchestrating role-playing, autonomous AI agents. By fostering collaborative intelligence, CrewAI empowers agents to work together seamlessly, tackling complex tasks." It is a lean Python framework — explicitly "built entirely from scratch, completely independent of LangChain" — with two primitives: **Crews** (autonomous, role/goal/backstory agents that collaborate) and **Flows** (event-driven, deterministic task orchestration, pitched as the "enterprise and production architecture"). You define agents in code or YAML, give each a role, goal, backstory, tools, LLM, and memory, then run the crew on a task.

This is the same shape as the frameworks this catalog has deliberately **skipped** — LangGraph, Flowise, dify: machinery for *building agentic applications*. You reach for CrewAI when your *product* needs a multi-agent backend (a research assistant, a customer-support swarm, a trip planner — all README examples), not when you want help writing or reviewing your own code. The README's center of gravity is the commercial **AMP Suite** (Crew Control Plane, tracing, control plane, enterprise security, on-prem/cloud deploy) and "100,000 developers certified through our community courses" — product-builder positioning, not dev-loop tooling.

Notably, CrewAI *does* ship a Claude Code plugin (`/plugin install crewai-skills@crewai-plugins`) with four skills (getting-started, design-agent, etc.) that teach an AI coding agent CrewAI best practices. That plugin is a dev-loop artifact; the framework it documents is not.

## How we tested it

**Source-grounded inspection — not installed, not run.** No `pip install crewai`, no crew defined, no flow executed, no AMP/Control Plane account. Every claim is from the repository surface (GitHub metadata, README, recursive file tree, release count), not from observed agent behavior. The "lightning-fast," "lean," and "100K certified developers" claims are the authors' README framing, not anything measured here.

```bash
gh api repos/crewAIInc/crewAI --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
# desc=role-playing agent orchestration; stars=53987; forks=7557; created 2023-10-27; MIT
gh api repos/crewAIInc/crewAI/readme --jq '.content' | base64 -d | head -120   # Crews + Flows + AMP Suite
gh api "repos/crewAIInc/crewAI/git/trees/HEAD?recursive=1" --jq '.tree[].path' | head -40  # Python pkg + docs/ + crewAIInc/skills plugin
gh api repos/crewAIInc/crewAI/releases --jq 'length'   # 30 (page-1 cap) — actively versioned on PyPI
```

## What worked

- **Mature, genuinely independent framework.** Built from scratch without LangChain, ~2.5 years old, actively pushed (same-day), heavily released on PyPI, 53.9K stars / 7.5K forks. The Crews-vs-Flows split (autonomy vs. deterministic event-driven control) is a real, considered design, not a thin wrapper.
- **Strong ergonomics for app builders.** Role/goal/backstory agents, YAML config, native tool and memory support, and a deterministic Flows layer give product teams a coherent path from prototype to "enterprise" multi-agent backends.
- **Dev-loop-adjacent skills exist.** The first-party `crewai-skills` Claude Code plugin is a legitimately useful artifact for *engineers who build on CrewAI* — it pulls best practices into the coding agent's context. That plugin (not the framework) is the catalog-relevant piece.
- **Production story is real.** AMP Suite (control plane, tracing/observability, on-prem) means teams shipping CrewAI agents get an operational surface, not just a library.

## What didn't work or surprised us

- **It builds the agent in your product; it doesn't help you build the product.** This is the LangGraph/dify/Flowise bar exactly. CrewAI orchestrates agents *at your application's runtime*; it does not Plan, Implement, Verify, Review, or Ship *your code*. The dev who uses CrewAI is writing an app, and CrewAI is a dependency of that app — squarely outside this catalog's scope.
- **Commercial-suite gravity.** The README leads with the paid AMP Suite and a certification funnel. The OSS framework is real and MIT, but the positioning is "platform you adopt," which raises lock-in and cost considerations irrelevant to a coding-loop tool.
- **Role-play framing is product theater, not coding rigor.** "Backstory"-driven role-playing agents are an application-design pattern for agentic products, orthogonal to the lean, verifiable instructions our better catalog entries favor for *producing code*.
- **Overlap is with skipped neighbors, not adopted ones.** Its true peers in this catalog are LangGraph and dify — both already triaged as out-of-scope app-builder frameworks. That alignment is the verdict.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | n/a (out of loop) | Affects the correctness of an *agentic product you build*, not the correctness of your own code changes. No bearing on the dev loop. |
| Speed | n/a | "Lightning-fast" refers to the framework's runtime for app agents, not to developer iteration speed on a codebase. |
| Maintainability | − (if adopted) | Adopting a multi-agent framework + control plane is a significant architectural dependency for your *application*, with its own lock-in surface. |
| Safety | neutral | Executes whatever agents/tools you wire up; risk lives in your app design, not in the dev loop. |
| Cost Efficiency | − | AMP Suite is commercial; multi-agent crews multiply LLM calls. A cost concern for app operators, not a coding-loop lever. |

## Verdict

**SKIP — app-building agent framework, same scope call as LangGraph/dify/Flowise.** CrewAI is a strong, mature, independent multi-agent *application* framework, but that is exactly the category this catalog excludes as adjacent to the dev loop. It is the engine inside an agentic product, not a tool that helps an engineer produce or ship code. Measured against the explicit bar — "skip app-building agent frameworks (LangGraph/Flowise/dify)" — CrewAI fails it cleanly; its nearest catalog neighbors are precisely those skipped entries.

Compared to neighbors: **LangGraph** and **dify** are already out-of-scope on identical grounds — CrewAI is their role-playing-agent cousin. The one genuinely catalog-relevant sliver is the first-party **`crewai-skills` Claude Code plugin** (Skills & Plugins), which teaches a coding agent CrewAI best practices; if anything from this ecosystem enters the catalog, it's that plugin, not the framework. Unlike **agent-orchestrator** or **claude-squad** (which orchestrate *coding* agents over *your* repo, inside the loop), CrewAI orchestrates *product* agents at *your app's* runtime, outside it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [crewAI](https://github.com/crewAIInc/crewAI) | framework | Lightweight, LangChain-independent Python framework for orchestrating role-playing multi-agent "Crews" and event-driven "Flows" inside agentic applications | Building a multi-agent backend for an agentic *product* (out of dev-loop scope; see SKIP verdict) | LangGraph, dify, Flowise (all skipped app-builder frameworks); crewai-skills plugin is the dev-loop-relevant sliver |
