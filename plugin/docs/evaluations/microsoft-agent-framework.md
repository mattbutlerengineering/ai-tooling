# Evaluation: Microsoft Agent Framework (MAF)

**Repo:** [microsoft/agent-framework](https://github.com/microsoft/agent-framework)
**Stars:** 11,486 | **Last updated:** 2026-06-19 (pushed) | **License:** MIT | **Language:** Python + C#/.NET
**Dev loop stage:** Agent Orchestration (production agent/workflow framework) — building agentic systems
**Layer:** Infrastructure (framework/SDK; PyPI `agent-framework` + NuGet `Microsoft.Agents.AI`)

---

## What it does

Microsoft Agent Framework (MAF) is **an open, multi-language framework for building production-grade AI agents and multi-agent workflows in .NET and Python.** It's pitched at "teams taking agents from prototype to production": a consistent foundation for building, orchestrating, and operating agent systems across Python and C#/.NET, with provider flexibility (Microsoft Foundry, Azure OpenAI, OpenAI, GitHub Copilot SDK, more). Key features: **graph-based orchestration** (sequential, concurrent, handoff, group-collaboration) with **checkpointing, streaming, human-in-the-loop, and time-travel**; **middleware** for request/response processing and custom pipelines; **OpenTelemetry observability**; **declarative agents** (YAML); **agent skills** (domain knowledge bases); and **Foundry-hosted agents** (deploy with ~2 extra lines). It positions as the convergence of Semantic Kernel + AutoGen lineage.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No agent/workflow built, no provider configured.

```bash
gh api repos/microsoft/agent-framework --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 11486, MIT, pushed 2026-06-19
gh api repos/microsoft/agent-framework/readme --jq '.content' | base64 -d | sed -n '58,114p'        # .NET+Python, graph orchestration, durability, Foundry
```

## What worked

- **The serious .NET option.** Most agent frameworks are Python/TS-only; first-class **C#/.NET *and* Python** with consistent APIs is a real gap-filler for enterprise/Microsoft shops.
- **Production-grade orchestration.** Graph patterns (sequential/concurrent/handoff/group) plus checkpointing, restartability, HITL, and "time-travel" target exactly the durability concerns that kill naive agent loops.
- **Governance + observability built in.** OTel tracing, middleware pipelines, and declarative agents suit teams that need auditability and consistency, not just demos.
- **Microsoft backing + lineage.** Consolidates Semantic Kernel/AutoGen experience; MS Learn docs, samples, and Foundry hosting lower the enterprise adoption path.
- **Provider flexibility.** Foundry/Azure OpenAI/OpenAI/Copilot SDK and more, so architecture can evolve without rewrites.

## What didn't work or surprised us

- **Builds agentic systems, not the coding loop.** Like the other agent frameworks here, it's for *building production agents*, not authoring code with a coding agent — catalog-relevant as infrastructure.
- **Microsoft/Azure gravity.** Strongest with Foundry/Azure; usable elsewhere but the smooth, hosted path is Microsoft's.
- **Heavyweight.** Graph orchestration, middleware, hosting, governance — substantial surface for teams that only need a single agent.
- **Young, consolidating.** Merges prior frameworks; APIs and the SK→MAF migration story are still settling.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Checkpointing, HITL, and graph orchestration reduce the failure modes of unstructured agent loops. |
| Speed | neutral | Faster to a production multi-agent system than DIY; not relevant to single-prompt tasks. |
| Maintainability | + | Consistent .NET/Python APIs, middleware, declarative agents, and OTel make systems debuggable and governable. |
| Safety | + | HITL control, governance, and observability are first-class. |
| Cost Efficiency | neutral | MIT/free framework; inference + Azure/Foundry hosting cost money. |

## Verdict

**CONDITIONAL** — Microsoft Agent Framework is the **production, enterprise, multi-language** entry in the agent-framework field: graph-based multi-agent orchestration with durability, HITL, governance, and OTel, uniquely spanning **.NET and Python**. For this catalog it's CONDITIONAL because it builds agentic systems rather than serving the coding dev loop directly. Adopt it when you're a **Microsoft/.NET (or mixed .NET+Python) team taking multi-agent workflows to production** and value durability/restartability/governance and Foundry hosting — it's the natural Semantic-Kernel/AutoGen successor. For Python-only app building, pydantic-ai/LangGraph are lighter; for a coding harness, this isn't it.

Compared to neighbors: **LangGraph** is the Python graph-orchestration incumbent; **crewAI** is role-based multi-agent; **pydantic-ai** is type-safe Python; **strands-agents** is a dual-language SDK. MAF's distinguishing pitch is **production multi-agent orchestration with first-class .NET + Python and Microsoft Foundry hosting.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [microsoft/agent-framework](https://github.com/microsoft/agent-framework) | framework | Microsoft's open multi-language framework (MIT) for production agents + multi-agent workflows in .NET and Python — graph-based orchestration (sequential/concurrent/handoff/group), middleware, checkpointing, HITL, time-travel, OTel observability, Foundry hosting | Taking agents prototype→production needs durable, restartable, governed multi-agent orchestration across .NET and Python | LangGraph, crewAI, strands-agents, pydantic-ai |
