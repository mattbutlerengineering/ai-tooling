# Evaluation: cognee

**Repo:** [topoteretes/cognee](https://github.com/topoteretes/cognee)
**Stars:** 17,903 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Reflect / Retrospect
**Layer:** Infrastructure

---

## What it does

Open-source AI memory platform that builds a self-hosted knowledge graph from ingested data, giving agents persistent long-term memory across sessions. The core API is three operations — `remember` (ingest and graph-connect), `recall` (query with auto-routing between vector, graph, and hybrid search), and `forget` (delete). Under the hood, cognee combines vector embeddings, graph reasoning, and cognitive-science-grounded ontology generation to create a knowledge graph where documents are both searchable by meaning and connected by relationships that evolve.

The platform ships as a Python library (`pip install cognee`), CLI (`cognee-cli`), MCP server (`cognee-mcp` in the monorepo), Claude Code plugin (via separate `cognee-integrations` repo), and managed cloud service. The Claude Code plugin uses 6 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, PreCompact, SessionEnd) to automatically capture prompts, tool traces, and responses into session memory, inject relevant context on prompt submit, and sync to the permanent graph at session end.

## How we tested it

**Evidence:** REVIEW

Architecture-level review of the main repo, MCP server, Claude Code plugin, and published benchmarks. Did not install or run locally due to infrastructure requirements.

```bash
gh api repos/topoteretes/cognee --jq '.description, .stargazers_count, .updated_at'
gh api repos/topoteretes/cognee/git/trees/main --jq '.tree[].path'
gh api repos/topoteretes/cognee/contents/cognee-mcp/src/server.py --jq '.content' | base64 -d
gh api repos/topoteretes/cognee-integrations/git/trees/main?recursive=1 --jq '.tree[].path'
gh api repos/topoteretes/cognee/contents/evals/README.md --jq '.content' | base64 -d
```

Reviewed: MCP server tool implementations (12 MCP primitives: 3 core tools + 9 UI/management tools), Claude Code plugin hooks architecture (6 lifecycle hooks with session-to-graph sync), evaluation benchmarks (45 cycles on HotPotQA against Mem0, Graphiti, LightRAG), and deployment options (6 platforms: Cloud, Modal, Railway, Fly.io, Render, Daytona).

## What worked

- **Published comparative benchmarks** — 45 evaluation cycles on HotPotQA against Mem0, Graphiti, and LightRAG. Only memory platform in the catalog with peer-reviewed competitive benchmarks (arXiv paper: 2505.24478). Cognee showed consistent improvements across EM, F1, and DeepEval Correctness.
- **Mature Claude Code integration** — 6-hook lifecycle with genuine architectural thought. PostToolUse captures tool traces (not just prompts), PreCompact preserves memory across context resets, SessionEnd bridges session data into the permanent graph. This is the deepest Claude Code hook integration of any memory tool in the catalog.
- **Minimal MCP API** — only 3 core tools (remember, recall, forget) vs mem0's larger surface. Auto-routing in `recall` picks the best search strategy (vector, graph, hybrid) without the user specifying. Session-aware memory with separate fast cache and permanent graph storage.
- **Research-backed architecture** — cognitive-science-grounded ontology generation is a genuine differentiator. The knowledge graph evolves its schema as knowledge grows, rather than using a fixed schema.
- **Deployment flexibility** — 6 one-click deployment options plus managed cloud. Docker Compose for local, Modal/Railway/Fly.io/Render for cloud, Daytona for sandboxes.

## What didn't work or surprised us

- **Heavy infrastructure for local use** — requires Python 3.10+, an LLM API key (OpenAI by default), and builds a local SQLite/graph database. Docker Compose setup adds PostgreSQL. This is significantly heavier than claude-mem (npm plugin, no external dependencies) or engram (single Go binary).
- **OpenAI dependency by default** — `LLM_API_KEY` defaults to OpenAI for graph construction. The remember operation uses LLM calls to build the knowledge graph, adding cost and latency. Other providers are documented but OpenAI is the happy path.
- **Claude Code plugin is in a separate repo** — `cognee-integrations`, not the main monorepo. Discovery is harder, and the plugin repo has lower visibility. Installation requires cloning the integrations repo and pointing `--plugin-dir` at it — not a marketplace install.
- **Commercial trajectory** — Cognee Cloud is the managed product; the OSS version is the on-ramp. The `serve()` API for cloud connection is prominent in docs. Apache-2.0 license is genuine, but the product incentives point toward cloud.
- **Benchmark limitations acknowledged** — the team notes that HotPotQA is a "benchmark mismatch" for memory systems and that LLM-as-judge evaluation carries inconsistencies. Honest, but means the competitive claims are weaker than they appear.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Graph-connected memory with relationship reasoning surfaces context that flat search misses |
| Speed | neutral | Graph construction adds latency to `remember`; `recall` auto-routing is fast but requires infrastructure |
| Maintainability | + | Knowledge graph evolves with the codebase; relationships between concepts are explicit |
| Safety | + | Dataset-level isolation, user/tenant separation, audit traits |
| Cost Efficiency | - | LLM calls for graph construction add cost; heavier infrastructure than lightweight alternatives |

## Verdict

**CONDITIONAL**

Use when you need relationship-aware memory that connects concepts across documents and sessions — the knowledge graph genuinely adds value for complex, multi-domain projects where flat text search misses relationships. The Claude Code integration is the deepest hook-based memory integration in the catalog. Choose claude-mem (ADOPT) for simpler setups where you want local-first memory without infrastructure overhead, or engram (CONDITIONAL) for portable cross-agent memory. Choose cognee when you need the knowledge graph layer, published benchmarks matter, or you're building a team-wide memory infrastructure.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cognee](https://github.com/topoteretes/cognee) | platform | Open-source AI memory with self-hosted knowledge graph engine for persistent agent memory | Need structured knowledge graph memory that agents can query across sessions | claude-mem, OMEGA, SimpleMem |
