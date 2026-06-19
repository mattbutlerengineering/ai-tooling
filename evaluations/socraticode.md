# Evaluation: SocratiCode

**Repo:** [giancarloerra/SocratiCode](https://github.com/giancarloerra/SocratiCode)
**Stars:** 3,014 | **Last updated:** 2026-06-18 | **License:** AGPL-3.0 (commercial license also offered)
**Dev loop stage:** Plan (codebase exploration before/during implementation)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Enterprise-grade codebase intelligence — semantic search, dependency graphs, 61% fewer tokens." SocratiCode is a Qdrant-backed code-intelligence engine exposed as an MCP server (npm package `socraticode`) plus native plugins/extensions for Claude Code, Cursor, VS Code Copilot, Codex, and Gemini CLI. It gives any MCP host deep, structural-plus-semantic understanding of a codebase so the agent searches an index instead of grepping and reading whole files.

The mechanism: on first use it auto-manages a local Docker stack — it pulls images and starts its own Qdrant (vector DB) and Ollama (local embeddings) containers, downloads the embedding model, then on `codebase_index {}` it chunks files at function/class boundaries via AST parsing (ast-grep, falling back to line-based for unsupported languages), embeds each chunk, and stores a dense vector + a BM25 sparse vector per chunk. Indexing is **batched and resumable** — it checkpoints progress so crashes/pauses don't lose work (claimed battle-tested up to ~40M LOC). A debounced (2s) file watcher then keeps the index current automatically across sessions and restarts (incremental re-index of changed files only, content hashes persisted in Qdrant), and `proper-lockfile`-based cross-process locking lets **multiple agents share one index** on the same repo concurrently.

At query time it exposes a set of `codebase_*` MCP tools. The core is `codebase_search` — hybrid search that runs dense + BM25 sub-queries in one Qdrant round-trip and fuses with Reciprocal Rank Fusion (RRF), with optional `includeLinked` cross-project search across repos linked via `.socraticode.json`. Beyond search it provides a **polyglot dependency graph** (`codebase_graph_query`, `codebase_graph_visualize`, `codebase_graph_circular`) built by static import/require/use/include analysis across 18+ languages, with circular-dependency detection and Mermaid + interactive HTML graph output; and a **symbol-level call graph** (`codebase_impact` for blast-radius, `codebase_flow` for entry-point→callee call-flow, `codebase_symbol` for definitions). It also indexes **context artifacts** — DB schemas, API specs, infra configs, architecture docs — as searchable non-code knowledge. Management tools include `codebase_status`, `codebase_update`, `codebase_watch`, and `codebase_stop`. Everything is local/private by default (no API keys, no data leaves the machine); cloud embeddings (OpenAI, Google Gemini), external/remote Qdrant or Ollama, LM Studio, and LiteLLM are optional swaps via env vars.

## How we tested it

**Method: inspected the GitHub repo, full README, release history, and repo tree. Did NOT install or run it hands-on.** No Docker stack was started, no `codebase_index` was executed, and no MCP session was driven. The 61%/84%/37x figures below are the author's published benchmark (VS Code 2.45M-line repo, live with Claude Opus 4.6), not numbers we reproduced. Per the catalog integrity rule, this is an architecture/maturity review calibrated against the existing codegraph (ADOPT) and code-context-engine (CONDITIONAL) evaluations.

What was actually inspected:

```
gh api repos/giancarloerra/SocratiCode --jq '{stars,license,description,pushed_at,created_at,forks,archived,language,homepage}'
# {stars:3014, forks:389, license:AGPL-3.0, lang:TypeScript, created:2026-02-26, pushed:2026-06-18, archived:false}

gh api repos/giancarloerra/SocratiCode/readme --jq '.content' | base64 -d   # full README (~34KB)
gh api repos/giancarloerra/SocratiCode/releases --jq '.[].tag_name'         # v1.8.17 down to v1.7.x (frequent, post-1.0)
gh api repos/giancarloerra/SocratiCode/git/trees/main --jq '.tree[].path'   # src/ tests/ vitest.config.ts biome.json
                                                                            # .claude-plugin .cursor-plugin .codex-plugin
                                                                            # docker-compose.yml SECURITY.md CLA.md CHANGELOG.md
```

Findings cross-referenced against `evaluations/codegraph.md` (ADOPT, 51K stars) and `evaluations/code-context-engine.md` (CONDITIONAL, 175 stars) for maturity and capability calibration, and against the catalog's other Code Understanding peers (gortex, trace-mcp, Understand-Anything).

## What worked

- **Genuinely mature, unlike the CONDITIONAL peer (CCE).** At v1.8.17 (post-1.0, frequent releases), 3,014 stars / 389 forks, a `tests/` dir + vitest + Biome + CI badge, a `SECURITY.md`, `CHANGELOG.md`, and a CLA — this is a maintained, production-shaped project, not a weekend prototype. This is the decisive contrast with code-context-engine (175 stars, v0.x, two months old) which was held to CONDITIONAL largely on maturity.
- **Broadest capability surface of any Code Understanding tool in the catalog.** It combines what codegraph and CCE do *separately* and adds more: hybrid semantic+BM25 search (CCE-style) AND a dependency graph + symbol-level impact/call-flow (codegraph-style) AND non-code artifact search (schemas/API/infra) AND cross-project + branch-aware + multi-agent shared index. The multi-agent shared index with cross-process locking is unique here.
- **Resumable, checkpointed indexing tested at enterprise scale** (claimed ~40M LOC; ~3M LOC indexed in <10 min on an M4). This directly targets the large-monorepo case where CCE's self-reported recall was brittle (R@10 0.07 on a Go monorepo).
- **Local and private by default** — auto-managed Docker Qdrant + Ollama, no API keys, suitable for air-gapped/on-prem. Cloud embeddings are optional, never required.
- **Truly host-agnostic** — one index serves Claude Code, Cursor, Copilot, Windsurf, Codex, Gemini, Zed via MCP; the understanding "lives with the codebase, not the assistant." Wider host reach than codegraph.
- **Published, reproducible-shaped benchmark** on a real public 2.45M-line repo (VS Code) with a named model (Opus 4.6): 61% less context, 84% fewer tool calls, 37x faster vs grep-based exploration — the same metric family codegraph reports (16% tokens / 58% fewer calls), at a larger scale.
- **Pre-computes the expensive structural work** (blast radius, call-flow, dependency traversal), letting smaller/cheaper models tackle architecturally complex tasks.

## What didn't work or surprised us

- **Heavier setup than its peers: Docker is a hard prerequisite.** It runs its own Qdrant + Ollama containers (~5 min one-time pull + model download). codegraph and CCE are lighter (npm/PyPI, no mandatory Docker daemon). On macOS/Windows the Docker containers can't use the GPU, so large repos need native Ollama or cloud embeddings for acceptable speed — a real friction point on the exact large codebases the tool targets.
- **AGPL-3.0 license.** The strong copyleft is a meaningful adoption blocker for some commercial/enterprise teams (a separate commercial license, `LICENSE-COMMERCIAL`, exists for that reason). codegraph and CCE are MIT — frictionless by comparison. This is the single biggest "check before adopting" item.
- **Capability overlap risk if you already run codegraph or CCE.** SocratiCode subsumes most of both; running all three would be redundant and could mean three watchers/indexes on one repo. It is a *consolidation* play, not an additive one.
- **Benchmark not independently reproduced.** The 61%/84%/37x numbers are the author's own, single-repo, single-model. Credible and detailed, but not third-party verified, and "vs grep-based exploration" is a favorable baseline (like CCE's "vs full-file reads").
- **Resource footprint.** A persistent Qdrant + Ollama container pair plus a file watcher is more ambient RAM/CPU than a SQLite-based index (CCE's sqlite-vec is ~2 MB). Fine on a workstation; notable on constrained machines.
- **Cloud is private beta and the maintainer surface looks single-org / single-author** (`giancarloerra`, sponsored by Altaire). Strong velocity, but bus-factor and long-term governance are unproven vs codegraph's larger ecosystem.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agents get structural (impact/call-flow/dependency) + semantic awareness instead of grep-and-guess; pre-computed blast radius reduces missed-dependent errors before edits |
| Speed | + | Author benchmark: 84% fewer tool calls and 37x faster architectural answers on a 2.45M-line repo vs grep-based exploration |
| Maintainability | + | Impact analysis, circular-dependency detection, and call-flow help understand/refactor large legacy codebases safely (mild edge over codegraph, which is search/graph-only) |
| Safety | + | Local/private by default, no API keys, air-gap capable; SECURITY.md present. (Docker daemon is added attack surface, but no cloud exfiltration by default) |
| Cost Efficiency | + | 61% less context per session benchmarked; pre-computed structure lets smaller/cheaper models handle complex tasks |

## Verdict

**CONDITIONAL**

SocratiCode is the most capable single Code Understanding tool in the catalog — it consolidates semantic search (CCE's strength), structural/dependency + symbol-level impact graphs (codegraph's strength), and non-code artifact knowledge into one mature (v1.8.17, 3K stars, tested, CI'd), local-first, host-agnostic engine with a published large-scale benchmark. On maturity and breadth it clears the bar that kept code-context-engine at CONDITIONAL. It is **additive in capability but a consolidation in practice** — it largely subsumes both codegraph and CCE, so the value is replacing them, not stacking on top.

It lands at CONDITIONAL rather than ADOPT for two concrete reasons that codegraph (the ADOPT incumbent) doesn't have: (1) a **mandatory Docker + Qdrant + Ollama footprint** that is heavier to set up and run, with GPU caveats on macOS/Windows; and (2) an **AGPL-3.0 license** that is a genuine blocker for many commercial teams. codegraph stays the lighter, MIT, frictionless default.

**Use SocratiCode when:** you work on large/enterprise polyglot codebases or monorepos (its checkpointed indexing and shared multi-agent index shine where CCE's recall was brittle), you want one index across multiple IDEs/agents, you need symbol-level impact/blast-radius analysis and non-code (schema/API/infra) knowledge that codegraph doesn't offer, you're comfortable running Docker, and AGPL-3.0 (or the commercial license) is acceptable for your repo. **Prefer codegraph instead when** you want a lightweight, MIT, zero-Docker MCP for structural navigation on small-to-medium projects. Re-evaluate for ADOPT if a third party reproduces the benchmark and the Docker/GPU friction is removed (e.g. a no-Docker mode).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SocratiCode](https://github.com/giancarloerra/SocratiCode) | tool | Enterprise-grade codebase intelligence — semantic search, dependency graphs, 61% fewer tokens (3K stars) | Agents waste tokens on large codebases; need indexed code intelligence with impact analysis | codegraph, code-context-engine, trace-mcp, gortex |
