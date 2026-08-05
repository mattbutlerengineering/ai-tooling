# Evaluation: eino

**Repo:** [cloudwego/eino](https://github.com/cloudwego/eino)
**Stars:** ~11,900 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An LLM application development framework in **Go**, from CloudWeGo (ByteDance). Eino brings the LangChain/Google-ADK-style component model to idiomatic Golang.

Per the README it provides: **Components** — reusable building blocks like `ChatModel`, `Tool`, `Retriever`, and `ChatTemplate`, with official implementations (OpenAI, Ollama, and more in `eino-ext`); and an **Agent Development Kit (ADK)** for building agents with tool use, multi-agent coordination, context management, interrupt/resume for human-in-the-loop, and ready-to-use agent patterns. It's designed to follow Go conventions rather than being a port of a Python framework.

## How we tested it

**Evidence:** REVIEW

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

**SKIP — app-building framework, no dev-loop bridge.** CloudWeGo's Go framework for building LLM applications and agents, with a component model and a multi-agent ADK.

**Its own evaluation says so.** Its recommendation is "adopt if you **build LLM applications or agents in Go**", and it says outright that it is "irrelevant for Python/TS stacks (use haystack/pydantic-ai or agent-kit/voltagent there)".

The bar is not new and is not this lane's invention. `WORKFLOW.md`'s **Tools Deliberately
Excluded** table states it — "Flowise, LangGraph — visual/programmatic agent builders: for building AI
products, not for your own dev workflow" — and the catalog has already applied it nine times, to
`langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`, `aisuite`, `dify`, `Flowise` and
`RAGFlow`. The `langchain` eval spells out both the test and the exceptions: a framework earns a slot
only if it has a **dev-loop bridge**, as `fast-agent` does by doubling as a runnable MCP-native coding
agent and `vercel/ai` does by shipping a coding-agent skill plus a harness-building primitive.

A SKIP here removes nothing. Per the `Flowise` precedent — "SKIP for this catalog's purpose (keep as
a reference entry)" — the row stays in `CATALOG.md`; what changes is that it stops reading as
something to install into a dev loop.

One consequence worth stating plainly: this is the catalog's only Go entry in the category, so the SKIP leaves Go unrepresented. That is the correct outcome, not a gap — the category itself is out of scope, and leaving one row in to cover a language would imply the other twenty belong.

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [eino](https://github.com/cloudwego/eino) | framework | LLM application framework in Go (Apache-2.0, ★12K, by CloudWeGo/ByteDance) — Go-idiomatic building blocks (ChatModel, Tool, Retriever, ChatTemplate) plus an Agent Development Kit for tool use, multi-agent coordination, context management, and interrupt/resume HITL | Go shops lack a production LLM/agent framework (most are Python/TS); want idiomatic Go components + an agent ADK with HITL | haystack, pydantic-ai, agent-kit, langchain (ext.) |
