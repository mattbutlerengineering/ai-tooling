# Evaluation: agent-kit

**Repo:** [inngest/agent-kit](https://github.com/inngest/agent-kit)
**Stars:** ~900 | **Last updated:** 2026-04-29 | **License:** Apache-2.0
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A TypeScript framework for building multi-agent networks with **deterministic routing**, from Inngest. The pitch is more code-controllable orchestration than fully-autonomous frameworks, plus durable, fault-tolerant execution via the Inngest engine.

Core concepts per the README:
- **Agents** — LLM calls combined with prompts, tools, and MCP servers.
- **Networks** — a way to get agents to collaborate over shared **State**, including handoff.
- **State** — conversation history plus a fully-typed state machine used in routing.
- **Routers** — where autonomy lives, spanning code-based routing to LLM-based (ReAct) orchestration.
- **Tracing** — built-in local and cloud tracing to debug/optimize workflows.

You `npm i @inngest/agent-kit inngest`, define agents/tools (or pull tools from MCP servers, e.g. via Smithery), wire a network with a router, and run it locally with the Inngest Dev Server — then deploy to the Inngest engine for orchestration and fault tolerance.

## How we tested it

Architecture review against the README and core-concepts docs. Confirmed the agents/networks/state/routers model, the code-based↔LLM-based routing spectrum, MCP tooling support, the built-in tracing, and the Inngest Dev Server (local) + engine (cloud durability) pairing. Noted the v0.9.0 requirement to install `inngest` separately. Last push ~2026-04 — steadier cadence than some rivals. Not run on a live network build, so condition-gated.

```bash
gh api repos/inngest/agent-kit --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/inngest/agent-kit/readme --jq '.content' | base64 -d
```

## What worked

- **Deterministic routing is the differentiator.** A typed state machine with code-based routers (escalating to LLM/ReAct only where you want) gives more control and reproducibility than fully-autonomous loops — easier to test and debug.
- **Durable execution via Inngest.** Pairing with the Inngest engine brings fault tolerance, retries, and orchestration that most agent libraries leave to you.
- **MCP-native, TypeScript-first.** Tools-via-MCP and a TS-native API fit the growing TS agent ecosystem.

## What didn't work or surprised us

- **Inngest gravity.** The best durability story assumes you adopt Inngest's engine/Dev Server — a platform commitment, not just a library.
- **Crowded TS-agent space.** Overlaps voltagent, pydantic-ai (Python), Microsoft Agent Framework, Mastra; the edge is deterministic routing + Inngest orchestration, not the agent primitives.
- **Smaller footprint.** ~900 stars and a separate-`inngest`-dependency gotcha at v0.9.0 signal a younger, still-evolving API.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Typed state + deterministic routers make agent flow reproducible |
| Speed | neutral | Framework ergonomics; no runtime perf claim |
| Maintainability | + | Code-controllable routing is easier to test than opaque autonomy |
| Safety | + | Deterministic routing + durable retries reduce uncontrolled behavior |
| Cost Efficiency | neutral | OSS; orchestration value tied to Inngest platform |

## Verdict

**CONDITIONAL**

Adopt for TypeScript multi-agent systems where you want deterministic, code-controllable routing and durable, fault-tolerant execution — particularly if you already use or are willing to adopt Inngest. For Python stacks, pydantic-ai fits better; for a broader TS platform with bundled ops, compare voltagent. Strong concept; weigh the Inngest platform commitment.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-kit](https://github.com/inngest/agent-kit) | framework | TypeScript multi-agent framework (Apache-2.0, by Inngest) — agent networks with shared typed state, routers from code-based to LLM-based (ReAct), MCP tooling, built-in tracing; pairs with the Inngest engine for durable, fault-tolerant runs | Most TS agent frameworks lean fully autonomous; want deterministic routing plus durable orchestration | voltagent, pydantic-ai, microsoft/agent-framework, strands-agents (harness-sdk) |
