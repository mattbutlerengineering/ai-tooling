# Evaluation: Honcho

**Repo:** [plastic-labs/honcho](https://github.com/plastic-labs/honcho)
**Stars:** 5,297 | **Last updated:** 2026-06-19 (pushed) | **License:** AGPL-3.0 | **Language:** Python (FastAPI; Python + TS SDKs)
**Dev loop stage:** Memory & Context (memory infrastructure)
**Layer:** Infrastructure (FastAPI server; managed at api.honcho.dev or self-hosted)

---

## What it does

Honcho is **memory infrastructure for stateful agents that understand changing people, agents, groups, projects, and ideas over time.** The loop is **Store → Reason → Query → Inject**: store messages/events/documents/tool-traces on a session, let Honcho process the queue in the background to update **per-peer representations**, then query for context, search results, peer representations, or a natural-language answer via a Chat endpoint — and drop the result into any LLM call or framework. It is "reasoning-first" (extracts conclusions, not just matching chunks), models multi-peer perspective (what one peer knows about another), and integrates with MCP, Claude Code, OpenCode, OpenClaw, Hermes, and Cursor-compatible clients. Managed (`api.honcho.dev`, $100 free credits) or self-hosted.

## How we tested it

**Source-grounded inspection — not installed, not run.** No server deployed, no peers/sessions created, the claimed "Pareto frontier of agent memory" evals not reproduced.

```bash
gh api repos/plastic-labs/honcho --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 5297, AGPL-3.0, pushed 2026-06-19
gh api repos/plastic-labs/honcho/readme --jq '.content' | base64 -d | sed -n '100,180p'       # Honcho Loop, peer model, integrations, quickstart
```

## What worked

- **Reasoning-first model.** "Extracts conclusions from conversations and events, not just matching chunks" is a meaningfully different premise from vector-recall memory — closer to a derived belief store than a transcript index.
- **Peer-centric, multi-perspective.** Modeling users/agents/groups/projects/ideas as entities that change over time, plus "what one peer knows about another," fits multi-user and multi-agent products better than a single global memory.
- **Clean integration story.** MCP + Claude Code/OpenCode/OpenClaw/Hermes/Cursor means it slots into agents directly, and the SDK path serves product builders.
- **Managed or self-hosted.** FastAPI server is self-hostable; the managed tier with free credits lowers trial friction.
- **Eval-forward positioning.** Public evals page + benchmark blog post make claims falsifiable (still vendor-run).

## What didn't work or surprised us

- **AGPL-3.0.** The strong copyleft license is a real consideration for embedding the server in a closed product — heavier than the MIT/Apache memory peers.
- **Background reasoning is async + opaque.** A queue that builds peer representations is powerful but adds eventual-consistency and auditability questions (when is a conclusion "settled," and can you inspect why).
- **Crowded category.** Competes directly with mem0, cognee, supermemory, Memori, MemOS; the differentiator is the reasoning-first peer model, not a new category.
- **Some value is the managed service.** The smoothest path (api.honcho.dev, dedicated instance, credits) is hosted; self-hosting is supported but is real infra.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reasoning-first per-peer representations surface conclusions, not just nearest chunks, keeping accurate context available. |
| Speed | + / neutral | Background reasoning + query endpoints avoid re-explaining; running/scaling a FastAPI service adds overhead. |
| Maintainability | neutral / − | Strong SDK/MCP surface; AGPL-3.0 + a stateful reasoning service is real infrastructure to run and license-check. |
| Safety | neutral | Self-hostable (good); per-peer belief derivation is an auditability/governance surface. |
| Cost Efficiency | neutral | Open core + free managed credits; infra/inference cost to run; reasoning can cut re-derivation. |

## Verdict

**CONDITIONAL** — Honcho is a benchmark-forward, **reasoning-first** memory layer whose distinctive idea is building queryable **per-peer representations** (users, agents, groups, projects, ideas) that change over time, exposed via a Chat endpoint and MCP. Adopt it when your product or multi-agent system needs memory that models *people and relationships* — not just a transcript vector store — and you can either accept AGPL-3.0 for self-hosting or use the managed api.honcho.dev. For a coding agent that just needs cross-session recall, lighter MIT/Apache options (claude-mem, OMEGA, supermemory) are simpler; Honcho earns its place when the reasoning-first, multi-peer model is the point. Treat the "Pareto frontier" claims as vendor-run and pilot on your data.

Compared to neighbors: **mem0** stores relationships as a memory layer; **cognee** is a knowledge-graph memory; **supermemory**/**Memori** are benchmark-forward/production memory engines; **MemOS** crystallizes experience into policy/skills. Honcho's distinguishing pitch is **reasoning-first per-peer representations of changing entities, queried in natural language.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [honcho](https://github.com/plastic-labs/honcho) | platform | Reasoning-first memory infrastructure (AGPL-3.0) — stores messages/events, reasons in the background to build per-peer representations of users/agents/groups/ideas, queried via a Chat endpoint or MCP; managed or self-hostable FastAPI | Chunk-matching memory recalls text but not conclusions; want memory that models how people and agents change over time | mem0, cognee, supermemory, Memori, MemOS |
