# Evaluation: letta

**Repo:** [letta-ai/letta](https://github.com/letta-ai/letta)
**Stars:** 23,415 | **Last updated:** 2026-05-14 (pushed; created 2023-10-11) | **License:** Apache-2.0
**Dev loop stage:** Cross-cutting (Memory & Context) — it is not a dev-loop stage tool but the *substrate* an agent stands on: stateful agents whose memory persists, self-edits, and self-improves across sessions. Touches Reflect (continual learning) and Implement (Letta Code, a terminal agent built on the memory engine).
**Layer:** Infrastructure (a self-hostable agent-memory *server* + Python/TypeScript SDKs + REST API — a backend platform you build agents into, formerly the MemGPT research project), not a Claude Code add-on

---

## What it does

Letta (formerly MemGPT) is an open-source platform for building **stateful agents with advanced, self-editing memory**. Its core thesis, inherited from the MemGPT paper, is the LLM-as-OS analogy: the model has limited "main context" (the prompt window) and unlimited "external context" (storage), and the agent itself issues tool calls to page memory in and out — editing its own `memory_blocks` (e.g. a `human` block and a `persona` block), searching archival memory, and consolidating learnings over time. Memory is not a passive store the harness writes to; it is something the agent reasons about and rewrites.

Two surfaces: (1) the **Letta API/SDK** — `pip install letta-client` / `npm install @letta-ai/letta-client` — for embedding stateful agents into your own applications via a full agents REST API; and (2) **Letta Code** (separate `@letta-ai/letta-code` CLI repo), a terminal coding agent built on the engine, with skills, subagents, and pre-built memory/continual-learning behaviors. It is model-agnostic (recommends Opus 4.5 / GPT-5.2). The `letta/` source tree is a real backend — `server`, `services`, `orm`, `schemas`, `agents`, `groups` (multi-agent), `llm_api`, `local_llm`, `data_sources`, `otel`/`monitoring` — i.e. a Postgres-backed agent server, not a library. Notably, Letta the org also authored `claude-subconscious` (already in this catalog), a Claude Code plugin that ports this persistence idea into the harness.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `pip install`, no server stood up, no agent created, no memory block edited or retrieved. Every claim comes from GitHub metadata, the README (Hello-World examples), the recursive file tree, the `letta/` core listing, and release counts — plus prior knowledge of the published MemGPT paper. The "self-improving," "learns over time," and "advanced memory" claims are Letta's README/product framing and the paper's thesis, not memory quality I measured against a task.

```bash
gh api repos/letta-ai/letta --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/letta-ai/letta/readme --jq '.content' | base64 -d | head -120
gh api "repos/letta-ai/letta/git/trees/HEAD?recursive=1" --jq '.tree[].path' | head -40
gh api repos/letta-ai/letta/contents/letta --jq '.[].name'   # server services orm schemas agents groups llm_api local_llm data_sources otel ...
gh api repos/letta-ai/letta/releases/latest --jq '{tag:.tag_name,date:.published_at[0:10]}'  # 0.16.8 / 2026-05-14
gh api repos/letta-ai/letta --jq '{forks:.forks_count,open_issues:.open_issues_count}'   # 2487 / 66
```

## What worked

- **The deepest, most principled memory model in the category.** MemGPT's self-editing memory (agent issues tool calls to rewrite its own context, page archival memory) is a genuinely different and more powerful idea than the write-and-retrieve stores that dominate this category (claude-mem, server-memory, agentmemory). The agent owns its memory rather than the harness bolting one on.
- **Mature, real infrastructure.** Created 2023-10, Apache-2.0, 23.4K stars, 2.5K forks, a full Postgres-backed server with REST API, Python + TS SDKs (Fern-generated, with CI for both), Alembic migrations, OTel monitoring, multi-agent `groups`, and a model-sweep test harness. Only 66 open issues despite the age — a tended project, not a research dump.
- **Model-agnostic and self-hostable.** Works across providers (Opus/GPT/local), runs on your own infra, and is not tied to any single harness — closer in spirit to OMEGA's "portable brain" goal than to harness-locked plugins.
- **A built-in agent on top (Letta Code).** Unlike pure memory libraries, Letta ships a usable terminal coding agent that demonstrates the memory engine in the dev loop, with skills and subagents.

## What didn't work or surprised us

- **It is a platform you build *on*, not a memory you bolt *onto* Claude Code.** This is the central mismatch with this catalog. OMEGA, claude-mem, and server-memory are MCP servers/plugins that add memory to your *existing* harness in minutes. Letta asks you to adopt *its* agent runtime, its API, its agent abstraction, and (for self-host) a Postgres server. That is a far larger commitment for a documentation/dev-loop catalog centered on Claude Code.
- **Wrong layer for the common case.** If the goal is "make my Claude Code agent remember across sessions," Letta is over-scoped — you would reach for the org's own `claude-subconscious` plugin (already cataloged) or OMEGA, not stand up a Letta server. Letta wins when you are *building an application's agents*, not augmenting a coding harness.
- **Operational weight.** Postgres, migrations, a server process, SDK integration, and an API key (or self-host) versus an MCP-server config line. The infrastructure that makes it powerful is exactly what makes it heavy for solo/dev-loop adoption.
- **Memory quality is unmeasured here.** The self-editing model is compelling in theory and on paper; this inspection did not verify recall quality, consolidation behavior, or whether the agent's self-edits stay coherent over long horizons. Stars and architecture are not benchmarks.
- **Overlaps cognee/mem0 more than OMEGA.** As an application-grade memory *platform*, its truest neighbors are cognee and mem0 (also platform-layer), not the lightweight harness-memory tools the task framed it against.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Self-editing, persistent memory can sharpen long-horizon agent correctness by preserving task state and learned facts across sessions — its core value claim, though unverified here. |
| Speed | − / neutral | Adds latency (memory tool-call round-trips, server hops) and a real integration/setup cost; not a fast on-ramp like an MCP-server config line. |
| Maintainability | − | You now operate a Postgres-backed agent server + SDK integration + migrations. Powerful, but a new piece of infrastructure to maintain — heavier than any other entry in this category. |
| Safety | neutral / − | Self-hostable and Apache-2.0 (good for data control), but the hosted Letta Cloud path sends agent state/memory to a third party; self-managed Postgres carries the usual data-store responsibilities. |
| Cost Efficiency | − / neutral | Open-source core is free, but operating a stateful-agent server (or paying for Letta Cloud) plus per-call memory tool overhead costs more than a local MCP memory store for the dev-loop use case. |

## Verdict

**DEFER — a serious, principled agent-memory platform, but the wrong layer for this catalog's Claude-Code-centric dev loop.** Letta is the deepest memory model in the category: the agent owns and rewrites its own context (the MemGPT thesis), backed by mature, self-hostable, model-agnostic infrastructure with strong SDK/CI hygiene. The problem is fit, not quality. This catalog augments an existing coding harness; Letta asks you to build *on its* agent runtime and operate a server. For "give my Claude Code sessions persistent memory," reach for the lighter, harness-native options — including Letta's own `claude-subconscious` plugin, already cataloged. Letta becomes a clear ADOPT only if your goal shifts from *augmenting a coding harness* to *building stateful agents into an application*; for the dev loop it documents, defer.

Compared to neighbors: it is far more capable and architecturally ambitious than **server-memory** (minimal reference KG) or **agentmemory** (validated-but-simple store), and deeper than **claude-mem** (semantic search + timeline plugin). But all three slot into Claude Code in minutes, where Letta does not. Against **OMEGA** (KEEP) — the catalog's portable, MCP-native cross-session brain — Letta is the heavier, build-your-own-runtime end of the spectrum: more powerful for app-building, far more operational overhead for the dev loop. Its truest peers here are platform-layer **cognee** and **mem0**, not the harness-memory tools.

## Catalog entry

**Target category:** Memory & Context

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [letta](https://github.com/letta-ai/letta) | platform | Stateful agents with self-editing, persistent memory (formerly MemGPT) — self-hostable server + Python/TS SDKs + REST API | Building application agents that remember, learn, and self-improve across sessions — agent-owned memory rather than a store the harness writes to | cognee, mem0 (memory platforms); OMEGA, claude-mem, claude-subconscious (lighter harness-native memory) |
