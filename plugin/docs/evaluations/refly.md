# Evaluation: refly

**Repo:** [refly-ai/refly](https://github.com/refly-ai/refly)
**Stars:** 7,381 | **Last updated:** 2026-03-25 (pushed); latest release v1.1.0, 2026-02-02 | **License:** ReflyAI Open Source License (Apache-2.0 + commercial-use restriction)
**Dev loop stage:** Implement (only via the thin Claude Code skill-export edge; the platform itself sits outside the loop)
**Layer:** Infrastructure (self-hosted Docker app platform)

---

## What it does

Catalog one-liner: "Open-source agent skills builder — define skills by vibe workflow, run on Claude Code, Cursor, Codex & more." Despite the "agent skills builder" framing, Refly is structurally a **self-hosted, visual agentic-workflow / app platform** — the same product class as Dify and n8n (its own README repeatedly positions it "vs n8n, Dify"; one of its GitHub topics is literally `n8n-alternative`).

The mechanism: you deploy Refly via Docker (`docs.refly.ai/community-version/self-deploy`, runs at `http://localhost:5700`), register an account, configure model providers (OpenAI/Anthropic API keys), then build "workflows" on a free-form visual canvas — drag nodes (Web Search → LLM → Output), wire them together, or use "Vibe Mode" to describe the flow in natural language and have a copilot generate it. Refly compiles intent into a "Model-Native DSL" and runs it on a stateful, "intervenable" runtime (pause/audit/re-steer mid-run). What Refly calls a "skill" is a **versioned, packaged workflow** stored in a central registry, not an Anthropic `SKILL.md` file. These packaged workflows can then be **delivered** four ways: as REST APIs (e.g. for Lovable frontends), as webhooks (Slack, Lark/Feishu, Teams), as MCP servers, and — the catalog-relevant edge — **exported to Claude Code / Cursor as invokable tools** via a separate CLI (`npm i -g @powerformer/refly-cli`; `refly skill install/publish`, or `npx skills add refly-ai/<name>`). Native Cursor export is marked "coming soon."

So the honest description is: Refly is a Dify-class workflow/app-orchestration platform whose distinguishing pitch is "skills as durable, versioned, governed infrastructure," with a packaging layer that can expose a built workflow to a coding agent as a remote tool. The "skill" it builds is a hosted workflow you call out to — not a local instruction file that shapes how the agent reasons.

## How we tested it

Method: repository + full README (English) + LICENSE review, plus maturity/adoption signals pulled from the GitHub API (stars, forks, contributors, release tags, created/pushed dates, open issues). Read the four documented use cases (API integration, Lark/Feishu webhook, **Skills for Claude Code**, Build Clawdbot), the self-deploy / `localhost:5700` quick-start, the comparison tables Refly itself draws against n8n/Dify/LangChain, and the CLI export contract (`@powerformer/refly-cli`, `refly skill install/publish`). Calibrated against the two SKIP app-platform evals already in this catalog (**dify**, **aisuite**) and the **openskills** CONDITIONAL eval (the actual SKILL.md portability peer). **Did not deploy Refly via Docker or run the CLI** — this is a repo + README + registry review, not hands-on usage. No metrics were invented; all numbers are quoted from the GitHub API or the README.

```bash
gh api repos/refly-ai/refly --jq '{stars,license,description,pushed_at,forks,topics}'
# 7,381 stars, NOASSERTION (ReflyAI License = Apache-2.0 + commercial restriction), TypeScript,
# pushed 2026-03-25, 720 forks; topics include n8n-alternative, vibe-workflow, skills-builder, slack, lark-bot
gh api repos/refly-ai/refly --jq '{created_at,open_issues,subscribers}'   # created 2024-02-19, 93 open issues, 52 watchers
gh api repos/refly-ai/refly/releases --jq '.[].tag_name'                  # v0.3.0 … v1.1.0 (latest published 2026-02-02)
gh api repos/refly-ai/refly/contributors --jq 'length'                    # 30 contributors
gh api repos/refly-ai/refly/contents/LICENSE | jq -r .content | base64 -d # Apache-2.0 + corporate-commercial-use restriction
gh api repos/refly-ai/refly/readme | jq -r .content | base64 -d          # 4 use cases, self-deploy, vs-n8n/Dify tables
```

## What worked

- **Coherent, well-built product in its own category.** A visual canvas + Vibe-Mode copilot + stateful "intervenable" runtime + central versioned registry + multi-target delivery (API / webhook / MCP / coding-agent export) is a genuinely complete workflow-platform offering. The "intervenable runtime" (pause/audit/re-steer mid-run) and versioned-skill governance are real differentiators over n8n/Dify.
- **There IS a real Claude Code touchpoint** — unlike dify (which has none). A published Refly workflow can be installed into Claude Code/Cursor as an invokable tool via `@powerformer/refly-cli` or `npx skills add`, so a coding agent can call a Refly-hosted workflow as a remote action. This is more dev-loop-adjacent than dify or aisuite.
- **MCP-native both ways.** Consumes 3,000+ tools and MCP servers as inputs; can also be exported as an MCP server. Fits the MCP ecosystem the catalog tracks.
- **Reasonable adoption and active maintenance.** 7.4K stars, 720 forks, 30 contributors, release cadence through v1.1.0 (Feb 2026), pushed Mar 2026 — healthier bus factor than several skill tools in the catalog.

## What didn't work or surprised us

- **It is a Dify-class app/workflow platform, not a coding-agent dev-loop tool.** Self-hosted Docker stack at `localhost:5700`, account registration, provider config, REST APIs, webhooks for Slack/Lark/Teams, "n8n-alternative" topic, explicit "vs n8n/Dify/LangChain" comparison tables — this is infrastructure for building AI *products/automations for end users*, the exact profile this catalog flags as out-of-loop (see dify, aisuite, WORKFLOW.md excluded tools).
- **"Agent skills builder" is a naming collision, not the Anthropic SKILL.md primitive.** A Refly "skill" is a versioned hosted *workflow* you invoke remotely — not a local `SKILL.md` instruction file with progressive disclosure that shapes the agent's reasoning. It does not author, improve, test, or review SKILL.md content. So it does NOT overlap with skill-creator / openskills the way the catalog entry implies; the overlap is superficial (shared word "skills").
- **The Claude Code value is a thin export edge on a heavy platform.** To get the one dev-loop-relevant feature (call a workflow as a tool), you must stand up and operate the whole Refly platform (or use the hosted SaaS). The coding-agent integration is the smallest surface of a large product, and native Cursor export is "coming soon."
- **Not OSI open source.** The "ReflyAI Open Source License" is Apache-2.0 *plus* a clause requiring a commercial license for any company/organization use, plus a no-logo-removal restriction and an appearance patent on the canvas UI. Same trap as dify — "open source" in marketing, source-available with corporate restrictions in fact.
- **Heavy infra for what a coding-agent user needs.** Docker, model-provider config, a registry, a stateful runtime — overkill if all you wanted was a skill or a tool for Claude Code.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Builds/runs hosted workflows; does not write, verify, or reason about your code. A called workflow's determinism is internal to Refly, not a code-quality lever in your repo |
| Speed | neutral | No inner/outer-loop acceleration; standing up the platform is a cost, not a speedup, for a coding-agent user |
| Maintainability | neutral | Governs *Refly workflow* assets, not your codebase. Adds an external service to operate |
| Safety | neutral / − | Self-hosted keeps data local, but it's another deployed service with API keys + webhooks to secure; corporate-commercial license restriction is a governance footgun |
| Cost Efficiency | neutral | Separate infra + model spend; the "minimal DSL lowers token cost" claim is about Refly's own runs, not your dev loop. Not independently measured |

## Verdict

**SKIP**

Refly is a well-built, actively maintained, Dify-class self-hosted visual workflow/app platform — and it self-identifies as exactly that (an "n8n alternative," compared head-to-head with n8n/Dify/LangChain throughout its own README). Like **dify** (SKIP) and **aisuite** (SKIP), it lives outside the coding-agent dev loop this catalog evaluates: it exists to compile business SOPs into hosted, governed workflows that you ship as APIs, webhooks, and bots for *end users*, not to make a developer faster inside Plan→Implement→Verify→Review→Ship→Reflect.

The catalog entry's framing — "agent skills builder," overlapping skill-creator/openskills — is a naming collision worth correcting: a Refly "skill" is a versioned hosted workflow invoked remotely, not an Anthropic `SKILL.md` instruction file. Refly does not author, improve, test, or load SKILL.md skills, so it does not actually compete with skill-creator (skill authoring) or openskills (SKILL.md portability).

It earns one honest distinction from dify: Refly has a *real* Claude Code touchpoint — its CLI (`@powerformer/refly-cli`) can publish a built workflow as a tool a coding agent invokes. But that is the thinnest edge of a large platform, requiring you to operate the whole stack to use it, with native editor export still "coming soon." That edge is not enough to pull a full app platform into the loop. **Skip** for coding-agent workflow augmentation. **Revisit only if** you separately need a hosted workflow/automation platform (the Dify/n8n use case) AND want to expose those workflows to Claude Code as remote tools — and even then, weigh the corporate-commercial license restriction. For the actual skill-authoring lever, use **skill-creator** / **write-a-skill**; for cross-editor SKILL.md portability, **openskills** (CONDITIONAL).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [refly](https://github.com/refly-ai/refly) | platform | Self-hosted visual agentic-workflow / app platform ("n8n/Dify alternative"); compiles workflows into versioned "skills" shippable as APIs, webhooks, MCP servers, or Claude Code/Cursor tools (7K stars, Apache-2.0+commercial restriction) | Need a governed platform to build hosted AI workflows/automations for end users and optionally expose them to coding agents as remote tools | dify, n8n (same app-platform class; out of dev loop). Not a true overlap with skill-creator/openskills — Refly "skills" are hosted workflows, not Anthropic SKILL.md files |
