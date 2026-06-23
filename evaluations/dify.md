# Evaluation: dify

**Repo:** [langgenius/dify](https://github.com/langgenius/dify)
**Stars:** 145,776 | **Last updated:** 2026-06-19 | **License:** Custom (SSPL-like with Commons Clause)
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Visual LLM app development platform for building AI-powered products. Drag-and-drop workflow canvas, RAG pipeline, agent builder with 50+ built-in tools, prompt IDE, model management across hundreds of providers, LLMOps observability (Langfuse/Opik integration), and Backend-as-a-Service APIs. Self-hosted via Docker Compose or available as Dify Cloud SaaS.

The platform targets teams building AI applications for end users — chatbots, document Q&A, workflow automation, content generation. It provides the infrastructure to go from prototype to production with visual orchestration, not code-first development.

## How we tested it

**Evidence:** REVIEW

Architecture review based on repository structure, README, release history, and feature documentation. Did not deploy locally — the evaluation focuses on whether the tool fits the dev loop for coding agent workflows.

```
gh api repos/langgenius/dify --jq '.description, .stargazers_count, .license.spdx_id'
gh api repos/langgenius/dify/releases --jq '.[0:3] | .[] | "\(.tag_name) \(.published_at)"'
gh api repos/langgenius/dify/git/trees/main --jq '.tree[].path' | head -30
```

Key structural observations:
- Has `.claude/`, `.codex/`, `.gemini/`, `CLAUDE.md`, `AGENTS.md` — built with AI coding agents
- `api/`, `web/`, `docker/`, `cli/`, `dify-agent/` — full-stack application, not a developer tool
- v1.14.2 (May 2026), biweekly releases, 145K+ stars, Linux Foundation project

## What worked

- **Most complete visual AI app builder**: workflow canvas, RAG, agent builder, model management, observability, and API layer in one platform — no other tool covers this breadth
- **Production deployment maturity**: Kubernetes Helm charts, Terraform modules for AWS/Azure/GCP, Grafana dashboards, Alibaba Cloud one-click — genuine enterprise readiness
- **Model coverage**: hundreds of providers including all major commercial and open-source models, OpenAI-compatible API support
- **Has CLAUDE.md and AGENTS.md**: the project itself uses AI coding agents for development, demonstrating the tools this catalog evaluates

## What didn't work or surprised us

- **Not a coding agent tool**: Dify builds AI products for end users, not AI-enhanced developer workflows. It doesn't write code, run tests, edit files, or integrate with git/CI in the way coding agents do
- **Visual orchestration ≠ dev workflow**: the drag-and-drop canvas is for building chatbots and RAG pipelines, not for the Plan→Implement→Verify→Review→Ship loop
- **Heavy infrastructure**: Docker Compose with PostgreSQL, Redis, multiple services — overkill for developer workflow augmentation
- **Custom license**: SSPL-like with Commons Clause restrictions on commercial hosting — not truly open source despite the marketing

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Builds AI apps, doesn't write or verify code |
| Speed | neutral | Not part of the coding workflow — no dev loop acceleration |
| Maintainability | neutral | No codebase quality impact — it's a separate product platform |
| Safety | neutral | Has security features but for AI app deployment, not code safety |
| Cost Efficiency | neutral | Separate infrastructure cost, not token/context optimization |

## Verdict

**SKIP**

Dify is the best visual LLM app development platform available, but it operates entirely outside the dev loop this catalog evaluates. Like cherry-studio (SKIP) and lobehub (SKIP), it's for building AI products, not for making developers more productive with AI coding agents. If you're building a chatbot or RAG-powered application for end users, Dify is excellent. If you're trying to improve your own coding workflow with AI, it has no touchpoint. The catalog categories (Flowise, LangGraph) it sits alongside are correctly flagged as "for building AI products, not for your own dev workflow" in WORKFLOW.md's excluded tools section.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dify](https://github.com/langgenius/dify) | platform | Production-ready agentic workflow platform with visual orchestration | Need visual agent workflow design at production scale | Flowise, LangGraph |
