# Evaluation: agentscope

**Repo:** [agentscope-ai/agentscope](https://github.com/agentscope-ai/agentscope)
**Stars:** ~27,000 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An agent framework whose organizing principle is transparency: "build and run agents you can **see, understand, and trust**." It provides message-based multi-agent orchestration with built-in visibility into what agents do.

Mechanically, AgentScope models multi-agent systems as message-passing between agents, and emphasizes observability — you can inspect the messages, tool calls, and behavior flowing through the system rather than treating the agent loop as a black box. It's a mature, widely-adopted (arXiv-backed) Python framework for building and running multi-agent applications, with the differentiator being the focus on inspectability/trust over raw feature count.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the framework's stated emphasis (message-based multi-agent orchestration with see/understand/trust observability; arXiv-backed). Confirmed the transparency-first positioning that distinguishes it from opaque agent frameworks. Not built a live multi-agent app, so condition-gated.

```bash
gh api repos/agentscope-ai/agentscope --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/agentscope-ai/agentscope/readme --jq '.content' | base64 -d
```

## What worked

- **Transparency as a first-class goal.** Inspectable message flow, tool calls, and behavior directly address the "I can't tell what my multi-agent system actually did" problem — valuable for debugging and trust.
- **Mature and popular.** ~27K stars, Apache-2.0, arXiv-backed — a serious, well-adopted framework, not a prototype.
- **Message-based model.** A clear message-passing abstraction makes multi-agent systems easier to reason about and observe.

## What didn't work or surprised us

- **Crowded framework space.** Overlaps Microsoft Agent Framework, voltagent, pydantic-ai, haystack; AgentScope's edge is the transparency/observability emphasis, not unique capabilities.
- **Framework commitment.** Adopting it means building around its abstractions; heavier than a thin agent library for simple needs.
- **Python-centric.** Best for Python multi-agent systems; TS teams will look elsewhere (agent-kit/voltagent).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Inspectable behavior makes multi-agent bugs diagnosable |
| Speed | neutral | Framework ergonomics; runtime depends on your agents |
| Maintainability | + | Transparent message flow is easier to reason about/maintain |
| Safety | + | Visibility into agent actions aids oversight |
| Cost Efficiency | neutral | OSS; cost depends on the models/agents you run |

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** A Python multi-agent framework whose differentiator is observability — seeing and trusting what the agents do.

**Its own evaluation says so.** Its recommendation is "adopt for **Python multi-agent systems**", with `agent-kit`/`voltagent` and `haystack` named as the alternatives — all members of the same out-of-scope category.

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

Worth noting what is being given up, because it is the most interesting thing in this batch: inspectability-as-a-feature is close to the catalog's **Verifiability** signal, the newest of the six and the least covered. But the thing made inspectable is an agent *application* at its own runtime, not the user's dev loop, so the signal is being moved somewhere this catalog does not measure.

Re-open if it grows a dev-loop bridge of the kind `fast-agent` and `vercel/ai` have — a runnable
coding agent, an installable coding-agent skill, or a documented primitive for building a harness.
Nothing about the project's quality is in dispute; this is a category call.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentscope](https://github.com/agentscope-ai/agentscope) | framework | Transparency-first agent framework (Apache-2.0, ★27K) — "build and run agents you can see, understand, and trust": message-based multi-agent orchestration with built-in visibility into behavior, tool use, and message flow; arXiv-backed | Most agent frameworks are opaque about what agents actually did; want a framework where multi-agent behavior is inspectable and trustworthy | voltagent, microsoft/agent-framework, pydantic-ai, haystack |
