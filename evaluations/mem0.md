# Evaluation: mem0

**Repo:** [mem0ai/mem0](https://github.com/mem0ai/mem0)
**Stars:** 58,871 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Universal memory layer for AI agents. Stores User, Session, and Agent state with entity linking and temporal reasoning. Retrieval fuses semantic search, BM25 keyword search, and entity matching scored in parallel. Available as a Python/Node SDK, self-hosted Docker server, managed cloud platform, or Claude Code plugin (v0.2.10 via `.claude-plugin/marketplace.json` in the repo).

The core differentiator is a research-backed algorithm with published benchmarks: 91.6 LoCoMo, 94.8 LongMemEval, 64.1 BEAM (1M tokens). No other memory tool in the catalog has reproducible retrieval benchmarks. Entity linking connects people, code, and concepts across memories, and temporal reasoning handles "what was X last month?" vs "what is X now?" — critical for long-running projects.

MCP server integration is community-maintained: `coleam00/mcp-mem0` (678 stars) is the most popular, with self-hosted options (`elvismdev/mem0-mcp-selfhosted`) bundling Qdrant + Neo4j + Ollama.

## How we tested it

Architecture-review evaluation based on:
1. Existing detailed comparison at `evaluations/mem0-vs-claude-mem.md` covering head-to-head benchmarks, feature matrices, and use-case mapping
2. Inspection of the official Claude Code plugin (marketplace.json v0.2.10) and 6 bundled skills (`mem0-cli`, `mem0-integrate`, `mem0-oss-to-platform`, `mem0-test-integration`, `mem0-vercel-ai-sdk`, `mem0`)
3. Survey of 5 community MCP server implementations (678 stars to 8 stars)
4. Repo health metrics: 58.8K stars, 6.7K forks, 339 open issues, 3 years old, updated today

```bash
gh api repos/mem0ai/mem0 --jq '.description, .stargazers_count, .updated_at'
gh api repos/mem0ai/mem0/contents/.claude-plugin/marketplace.json --jq '.content' | base64 -d
gh api search/repositories -f q='mem0 mcp server' -f sort=stars --jq '.items[] | .full_name, .stargazers_count'
```

## What worked

- **Published, reproducible benchmarks** — 91.6 LoCoMo and 94.8 LongMemEval are the only hard retrieval numbers in the memory tool ecosystem; no other catalog entry has comparable evidence
- **Entity linking** — connects people, code, and concepts across memories for retrieval boosting; genuinely useful for large memory stores where flat search degrades
- **Temporal reasoning** — time-aware retrieval distinguishes past vs present state, which flat memory systems conflate
- **Multi-platform** — Python SDK, Node SDK, REST API, browser extension, Claude Code plugin, MCP servers; the only memory tool that works across Claude Code, Codex, Cursor, and custom agents simultaneously
- **Official Claude Code plugin** — v0.2.10 ships in-repo with 6 skills, not just community-maintained

## What didn't work or surprised us

- **No auto-capture** — requires explicit `mem0 add` calls; unlike claude-mem which passively captures via hooks, mem0 depends on the agent being instructed to save memories
- **MCP servers are community-maintained** — the official repo ships a plugin but the MCP path (`coleam00/mcp-mem0`) is a third-party project, adding integration risk
- **339 open issues** suggests rapid growth outpacing support capacity
- **Richest features require cloud or Docker** — dashboard, auth, advanced retrieval need the platform or self-hosted Docker; the plugin alone is a subset
- **No bundled workflow skills** — claude-mem ships 18+ skills (make-plan, learn-codebase, pathfinder, weekly-digests); mem0 is memory-only

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Published benchmarks (91.6 LoCoMo, 94.8 LongMemEval) demonstrate superior retrieval accuracy vs unscored alternatives |
| Speed | + | Entity linking and temporal reasoning reduce irrelevant recall, faster convergence on correct context |
| Maintainability | neutral | Memory is infrastructure, not code quality; no direct impact |
| Safety | neutral | Apache-2.0, self-hostable; cloud path adds vendor dependency |
| Cost Efficiency | - | Cloud platform has costs beyond free tier; self-hosted requires Docker + Qdrant + Neo4j |

## Verdict

**CONDITIONAL**

Use mem0 when you need memory that works across multiple AI editors (Claude Code + Codex + Cursor), when your memory store exceeds ~5K entries and needs entity linking for retrieval quality, or when you need publishable retrieval benchmarks to justify the tool to stakeholders. For Claude Code-only workflows, claude-mem (ADOPT) remains the better choice: zero-friction install, auto-capture via hooks, and 18+ bundled workflow skills. Do not run both simultaneously.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mem0](https://github.com/mem0ai/mem0) | MCP server | AI memory layer with entity linking, temporal reasoning, and published retrieval benchmarks (58.8K stars) | Need cross-platform memory with relationship-aware retrieval that scales past thousands of entries | claude-mem, OMEGA, SimpleMem |
