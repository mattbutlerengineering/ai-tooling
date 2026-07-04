# Evaluation: memsearch

**Repo:** [zilliztech/memsearch](https://github.com/zilliztech/memsearch)
**Stars:** 2,076 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A persistent, unified semantic memory layer for AI coding agents (Claude Code, Codex CLI, OpenClaw, OpenCode), backed by Markdown files as the source of truth and Milvus as a rebuildable "shadow" vector index. Maintained by Zilliz, the company behind Milvus.

The mechanism: a Claude Code plugin installs four hooks (`SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`). After each turn, the `Stop` hook parses the last turn, has an LLM (Haiku by default) summarize it into bullet points, and appends them to a daily `.memsearch/memory/YYYY-MM-DD.md` file with a `<!-- session:UUID -->` anchor. A file watcher re-chunks changed Markdown, SHA-256-hashes each chunk to skip unchanged content, embeds new chunks, and upserts them into Milvus. Recall is a 3-layer progressive search: L1 `search` returns ranked chunks (hybrid dense vector + BM25 sparse + RRF reranking), L2 `expand <chunk_hash>` returns the full `.md` section, L3 parses the raw transcript JSONL. Recall triggers via the `/memory-recall` skill or naturally when Claude senses a question needs history. Embeddings default to local ONNX bge-m3 (~558 MB, CPU, free); Milvus defaults to Milvus Lite (single local file). The newer "Skills from Memory" feature distills repeated workflows into installable Agent Skills (procedural memory), and optional background tasks maintain durable `PROJECT.md` / `USER.md` notes.

## How we tested it

**Evidence:** REVIEW

Architecture review — inspected the GitHub repo, README, the Claude Code plugin manifest (`plugins/claude-code/.claude-plugin/plugin.json`), the hook configuration (`plugins/claude-code/hooks/hooks.json`), the skills directory (`memory-config`, `memory-recall`, `memory-to-skill`), the documented CLI/Python API, and the Milvus/embedding configuration surface. **Did not install or run hands-on** — the user already runs claude-mem (ADOPT) + OMEGA for memory, and installing a competing hook-based memory layer risks hook conflicts in the live setup. Compared against the existing `agentmemory.md` (CONDITIONAL) eval and claude-mem (ADOPT, the user's choice).

```bash
gh api repos/zilliztech/memsearch --jq '{stars,license,description,pushed_at,open_issues}'
gh api repos/zilliztech/memsearch/readme --jq '.content' | base64 -d
gh api "repos/zilliztech/memsearch/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/zilliztech/memsearch/contents/plugins/claude-code/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/zilliztech/memsearch/releases --jq '.[].tag_name'   # → v0.4.10 latest, ~40 releases
```

Reviewed: 4 Claude Code hooks, 3 plugin skills, 4-platform plugin layer, CLI verbs (index/search/expand/watch/compact/stats/reset), Python `MemSearch` API, embedding providers (onnx/openai/ollama/google/voyage/jina/mistral), Milvus deployment modes (Lite/Zilliz Cloud/self-hosted Docker). 17 contributors, ~31 test files.

## What worked

- **Markdown-as-source-of-truth, Milvus-as-shadow** is the strongest design decision. Memories are human-readable, editable, and git-versionable `.md` files; the vector DB is a derived, rebuildable cache (`memsearch reset --yes` rebuilds it). This is the same philosophy claude-mem and agentmemory use, and it means you are never locked out of your own memory by a DB.
- **Genuine cross-agent portability.** A conversation in Claude Code becomes searchable in Codex CLI, OpenClaw, and OpenCode because all four plugins share one `.memsearch/` backend. This is a real differentiator over claude-mem (Claude Code-centric) for users who switch harnesses.
- **Lean hook footprint for Claude Code** — only 4 hooks (`SessionStart`, `UserPromptSubmit`, `Stop`, `SessionEnd`), with `Stop`/`SessionEnd` async. Compare agentmemory's 12 hooks. Fewer hook slots means lower collision risk with an existing setup (superpowers, claude-reflect, OMEGA).
- **Zero-external-DB and zero-API-key default path.** Milvus Lite (local single file) + ONNX bge-m3 (local CPU embeddings) means no cloud account and no API key are required to run. Capture summarization defaults to the plugin's native model.
- **Small, focused MCP/skill surface** — 3 skills (`memory-recall`, `memory-config`, `memory-to-skill`) rather than a 53-tool wall (agentmemory). Lower context overhead.
- **Active maintenance and vendor backing.** ~40 releases (latest v0.4.10), pushed within the last day, CI test workflow, published on PyPI. Backed by Zilliz, not a lone author.
- **"Skills from Memory"** (procedural memory) is a novel third layer — distilling repeated workflows into installable Agent Skills following the agentskills.io standard, kept inert until you explicitly install.

## What didn't work or surprised us

- **The Milvus dependency adds weight without clear payoff for a single Claude Code user.** claude-mem and agentmemory get strong recall from SQLite + local embeddings with *zero* vector-DB layer. memsearch's default Milvus Lite is "just a file" too, but it pulls in the Milvus client stack and the conceptual overhead of a vector DB to solve a problem the ADOPTED tool already solves without one. The benefit (Milvus) only materializes at team/multi-user scale.
- **Clear Zilliz-vendor steering.** The README repeatedly recommends Zilliz Cloud (the company's hosted product, "⭐ recommended") with UTM-tagged signup links. The default is local Milvus Lite, so this is upsell rather than lock-in — but the project exists partly as a funnel for Zilliz Cloud, which colors its "recommended" guidance. The embedding/DB layers are swappable, so true lock-in is low.
- **No published retrieval benchmarks.** Unlike agentmemory (95.2% R@5 on LongMemEval-S) or mem0, memsearch ships no reproducible recall numbers. The "design-philosophy" page has a competitor comparison but no quantified retrieval evaluation. Cannot verify recall quality from sources.
- **Younger and smaller than the alternatives.** Created Feb 2026, 2.1K stars, still v0.x (v0.4.10) — pre-1.0 API stability. claude-mem is far more battle-tested with a mature plugin ecosystem; agentmemory has 23K stars and 1,400+ tests.
- **Capture uses an LLM summarizer per turn** (Haiku by default). This is a recurring token cost on every conversation turn, even if small — claude-mem also summarizes, so this is parity, not a regression, but it is not free.
- **OpenClaw inspiration / lineage overlap.** memsearch borrows its Markdown memory architecture from OpenClaw, and shares assets with Zilliz's own `claude-context` repo — the design is derivative rather than novel on the core memory model.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Hybrid search (dense + BM25 + RRF) over auto-captured session history aids recall of past decisions; no published benchmark to quantify |
| Speed | + | 3-layer progressive retrieval + SHA-256 dedup avoids re-embedding; async Stop/SessionEnd hooks don't block the turn |
| Maintainability | + | Markdown source-of-truth is human-editable and git-versionable; Milvus is rebuildable; but adds a vector-DB dependency vs SQLite-only peers |
| Safety | neutral | Local-first default (no cloud, no API key); lean 4-hook surface; but Zilliz Cloud path sends memory off-box if enabled |
| Cost Efficiency | + | Local ONNX embeddings (free) + Milvus Lite (free); only per-turn Haiku summarization cost; Zilliz Cloud is the paid upsell |

## Verdict

**CONDITIONAL**

Use memsearch when you genuinely work across multiple agent harnesses (Claude Code + Codex CLI + OpenClaw + OpenCode) and want one shared, portable project memory — that cross-agent unification is its real, unique value, and the Markdown-source-of-truth design is sound. For a Claude Code-only user (this user), it does not beat claude-mem (ADOPT): claude-mem is more battle-tested, has a mature plugin ecosystem, and delivers comparable hybrid recall from SQLite + local embeddings with **no vector-DB dependency**, whereas memsearch's Milvus backing is overhead that only pays off at team/multi-user scale and comes with Zilliz Cloud upsell steering. Like agentmemory (CONDITIONAL), it is a credible memory tool that wins on a specific axis (cross-agent reach) but loses to claude-mem on Claude Code ecosystem fit and simplicity. KEEP the catalog entry; do not adopt over claude-mem.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memsearch](https://github.com/zilliztech/memsearch) | tool | Persistent, unified memory layer for AI agents (Claude Code, Codex), backed by Markdown + Zilliz/Milvus | Agents lose context across sessions; need shared, cross-agent vector-backed memory | claude-mem, OMEGA, mem0, supermemory, agentmemory |
