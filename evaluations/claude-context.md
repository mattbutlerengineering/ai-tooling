# Evaluation: claude-context

**Repo:** [zilliztech/claude-context](https://github.com/zilliztech/claude-context)
**Stars:** 11,897 | **Last updated:** 2026-06-08 (pushed; created 2025-06-06) | **License:** MIT
**Last verified:** 2026-07-08  <!-- source-grounded re-check; not a hands-on re-verification -->
**Dev loop stage:** Implement and Plan (inner loop) — it's a retrieval substrate that feeds the agent relevant code before it edits or reasons, replacing multi-round file discovery. Not a Review/Ship/Reflect tool.
**Layer:** Tooling (an MCP server the agent calls), backed by Infrastructure (a Milvus/Zilliz vector DB + an external embedding API).

---

## What it does

Catalog one-liner: "Code search MCP for Claude Code. Make entire codebase the context for any coding agent." **Claude Context** is a semantic-search MCP plugin from Zilliz (the company behind the Milvus vector database). It indexes your whole codebase into a vector store and exposes search tools so the agent retrieves the few relevant snippets for a query instead of grepping and reading whole directories round after round. The pitch is two-fold: better recall over "millions of lines," and lower cost — "instead of loading entire directories into Claude for every request… only uses related code in context."

Mechanically it is a TypeScript pnpm monorepo (`packages/core`, `packages/mcp`, plus a VS Code extension and a Chrome extension). The core does AST-aware code splitting (tree-sitter), generates embeddings via a pluggable provider (`packages/core/src/embedding` — OpenAI, VoyageAI, Gemini, Ollama per the topics), writes vectors to Milvus/Zilliz Cloud, and uses a **Merkle-tree file synchronizer** for incremental re-indexing so only changed files are re-embedded. The MCP server (`@zilliz/claude-context-mcp`) wires this to Claude Code, Codex, Gemini CLI, Qwen, Windsurf, Cursor, Cline, Augment, Cherry Studio, and Claude Desktop — the README documents a JSON/TOML stanza for each. The published config is hosted-first: `MILVUS_ADDRESS`/`MILVUS_TOKEN` point at Zilliz Cloud and `OPENAI_API_KEY` at OpenAI's embedding API.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No MCP server was added, no codebase was indexed, no Milvus cluster or embedding key was provisioned, and no search was issued. There is no Zilliz Cloud signup, no OpenAI key, and no measured token/recall numbers here. Every claim comes from the repository (GitHub metadata, README, recursive file tree, package layout, commit/release counts) and the authors' own framing. The "94%-style" cost and "millions of lines" claims are README marketing, not anything I benchmarked.

```bash
gh api repos/zilliztech/claude-context --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id,topics}'
gh api repos/zilliztech/claude-context/readme --jq '.content' | base64 -d | head -330
gh api "repos/zilliztech/claude-context/git/trees/HEAD?recursive=1" --jq '.tree[].path'   # monorepo: core / mcp / vscode-extension / chrome-extension
gh api repos/zilliztech/claude-context/commits  --jq 'length'   # 30 (page-1 cap; active)
gh api repos/zilliztech/claude-context/releases --jq 'length'   # 0 tagged GH releases (ships via npm semver)
```

## What worked

- **Right architecture for the stated problem.** AST-aware (tree-sitter) chunking + embeddings + a real vector DB is the textbook design for "find the 5 relevant functions across a huge repo," and it beats naive grep/read loops on large monorepos where the agent otherwise burns turns discovering files.
- **Incremental indexing is the standout.** The Merkle-tree synchronizer means edits re-embed only changed files rather than re-indexing the whole tree — the detail that makes vector search viable on an actively-edited codebase rather than a stale snapshot.
- **Serious maintainer and broad reach.** Built by Zilliz/Milvus (a vector-DB vendor with deep retrieval expertise), 11.9K stars / 880 forks, published npm packages (`-core`, `-mcp`), a VS Code Marketplace extension, docs site, CI, and config for ~10 host agents. This is a maintained product, not a weekend repo.
- **Pluggable embeddings.** OpenAI / VoyageAI / Gemini / Ollama support (topics + `embedding/` dir) means you can avoid sending code to OpenAI specifically, and Ollama allows a fully local embedding path.

## What didn't work or surprised us

- **Heavy infrastructure dependency — the core tradeoff.** Unlike `serena` (LSP, zero external services) or `codebase-memory-mcp` (single static binary, local), claude-context needs a **running Milvus/Zilliz vector DB plus an embedding provider**. The documented happy path is *Zilliz Cloud + OpenAI*, i.e. two third-party accounts and two API keys before first search. Self-hosting Milvus is possible but is real ops.
- **Code leaves the machine by default.** The published config embeds via OpenAI's API and stores vectors in Zilliz Cloud, so your source is sent to two external services unless you deliberately switch to Ollama + self-hosted Milvus. For proprietary code this is a governance decision, not a default to wave through.
- **Recurring cost, not just setup cost.** Embedding API calls (re-embedding on edits) and a hosted vector DB are ongoing spend. The "cost-effective" claim is *relative to* dumping whole directories into the context window — it trades context tokens for embedding+DB cost, which can be the better deal on large repos but isn't free.
- **Semantic recall is probabilistic.** Vector search returns "similar" chunks; it can miss an exact symbol that `grep` or an LSP `find-references` (serena) would catch deterministically. Best as a *complement* to symbol-level tools, not a replacement.
- **0 tagged GitHub releases.** Versioning lives on npm (`@latest` in every config example), so there's no pinned, curated bundle from the GH side — you run whatever `@latest` resolves to.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Better recall of relevant code across large repos improves grounding; but probabilistic vector search can miss exact symbols a deterministic LSP/grep would find — complements, not replaces. |
| Speed | + | Eliminates multi-round file discovery; one search returns the relevant snippets. Merkle-tree incremental re-index keeps the index fresh without full rebuilds. |
| Maintainability | neutral | Doesn't touch your codebase; adds operational surface (a vector DB + embedding pipeline) you now run/pay for. |
| Safety | − | Default path sends source to OpenAI (embeddings) and Zilliz Cloud (vectors). Mitigable via Ollama + self-hosted Milvus, but the documented default exfiltrates code. |
| Cost Efficiency | + / − | Cuts context tokens on large codebases (the headline win), but adds recurring embedding-API + vector-DB cost. Net-positive mainly at large-repo scale. |

## Verdict

**CONDITIONAL — adopt for large/monorepo codebases where multi-round file discovery is the bottleneck and you accept a vector-DB + embedding dependency; skip for small repos and code you can't send off-box without self-hosting.** claude-context is the best-pedigreed semantic-search MCP in this category — Zilliz built it, the AST-chunking + Merkle incremental-index design is sound, and broad host support makes it easy to wire in. The cost is genuine infrastructure: a Milvus/Zilliz vector DB and an embedding provider, with the documented default sending source to OpenAI + Zilliz Cloud. That's a fine trade on a giant repo where context tokens dominate spend; it's overkill (and an exfiltration risk) on a codebase small enough to grep.

Compared to neighbors: **serena** is the strongest alternative for most teams — symbol-level LSP retrieval with *zero* external services and deterministic find/reference/rename, no embedding cost or code exfiltration; prefer it when you want precision and local-only. **codebase-memory-mcp** and **gortex** offer local static-binary structural indexing (broad language counts, no vector DB) — lighter ops than claude-context, weaker at fuzzy semantic recall. **code-context-engine** is the closest peer (indexed search, token-savings pitch) but with less retrieval pedigree than Zilliz. claude-context wins specifically on *semantic* recall over very large codebases and on incremental freshness; it loses on operational weight and default privacy posture.

## Catalog entry

Target category: **MCP Servers** (cross-listed conceptually with Code Understanding).

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-context](https://github.com/zilliztech/claude-context) | MCP server | Semantic code search over your whole codebase via Milvus vector DB + embeddings (AST chunking, Merkle incremental re-index), from the Zilliz/Milvus team | Agents burn turns and tokens grepping/reading whole directories; semantic retrieval surfaces the few relevant snippets across millions of lines | serena, code-context-engine, codebase-memory-mcp, gortex, codegraph |
