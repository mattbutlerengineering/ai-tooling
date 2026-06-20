# Evaluation: eino

**Repo:** [cloudwego/eino](https://github.com/cloudwego/eino)
**Stars:** ~11,900 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An LLM application development framework in **Go**, from CloudWeGo (ByteDance). Eino brings the LangChain/Google-ADK-style component model to idiomatic Golang.

Per the README it provides: **Components** — reusable building blocks like `ChatModel`, `Tool`, `Retriever`, and `ChatTemplate`, with official implementations (OpenAI, Ollama, and more in `eino-ext`); and an **Agent Development Kit (ADK)** for building agents with tool use, multi-agent coordination, context management, interrupt/resume for human-in-the-loop, and ready-to-use agent patterns. It's designed to follow Go conventions rather than being a port of a Python framework.

## How we tested it

Architecture review against the README and the component + ADK model (ChatModel/Tool/Retriever/ChatTemplate; agent tool use, multi-agent coordination, context management, interrupt/resume HITL). Confirmed the Go-idiomatic positioning and the LangChain/Google-ADK lineage. Not built a live Go app, so condition-gated.

```bash
gh api repos/cloudwego/eino --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/cloudwego/eino/readme --jq '.content' | base64 -d
```

## What worked

- **Fills the Go gap.** Most LLM/agent frameworks are Python or TS; a production, idiomatic-Go framework (from CloudWeGo) is genuinely useful for Go backends.
- **Component + ADK depth.** ChatModel/Tool/Retriever/ChatTemplate plus an agent ADK with multi-agent coordination and interrupt/resume HITL covers real production needs, not just a chat wrapper.
- **Credible maintainer.** CloudWeGo/ByteDance backing and ~12K stars signal seriousness and longevity.

## What didn't work or surprised us

- **Go-only.** Best (only) fit for Go shops; irrelevant for Python/TS stacks.
- **Ecosystem maturity.** Component implementations live in `eino-ext`; coverage of providers/integrations will lag the Python ecosystem.
- **Overlaps haystack/pydantic-ai/agent-kit conceptually.** Same patterns in a different language — the choice is driven by your stack being Go.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Typed Go components + structured agent patterns reduce glue bugs |
| Speed | + | Go runtime performance for LLM application backends |
| Maintainability | + | Idiomatic Go framework vs. hand-rolled LLM plumbing |
| Safety | + | Interrupt/resume HITL gates risky agent actions |
| Cost Efficiency | neutral | OSS; cost depends on the models you wire in |

## Verdict

**CONDITIONAL**

Adopt if you build LLM applications or agents in **Go** and want an idiomatic, production-oriented framework with a real component model and an agent ADK (multi-agent, HITL) — it's the standout option for Go shops, from a credible maintainer. Irrelevant for Python/TS stacks (use haystack/pydantic-ai or agent-kit/voltagent there). Check `eino-ext` for the provider/integration coverage you need.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [eino](https://github.com/cloudwego/eino) | framework | LLM application framework in Go (Apache-2.0, ★12K, by CloudWeGo/ByteDance) — Go-idiomatic building blocks (ChatModel, Tool, Retriever, ChatTemplate) plus an Agent Development Kit for tool use, multi-agent coordination, context management, and interrupt/resume HITL | Go shops lack a production LLM/agent framework (most are Python/TS); want idiomatic Go components + an agent ADK with HITL | haystack, pydantic-ai, agent-kit, langchain (ext.) |
