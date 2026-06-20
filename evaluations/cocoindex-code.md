# Evaluation: cocoindex-code (ccc)

**Repo:** [cocoindex-io/cocoindex-code](https://github.com/cocoindex-io/cocoindex-code)
**Stars:** 2,175 | **Last updated:** 2026-06-19 (pushed) | **License:** Apache-2.0 | **Language:** Python (built on the Rust CocoIndex engine)
**Dev loop stage:** Code Understanding (semantic code search) — Implement
**Layer:** Tooling (CLI + Claude Code skill / plugin + MCP server)

---

## What it does

cocoindex-code (`ccc`) is a **zero-config, AST-based semantic code search tool** for a codebase, built on [CocoIndex](https://github.com/cocoindex-io/cocoindex), a Rust data-transformation engine. It's usable from the CLI or wired into Claude/Codex/Cursor (any coding agent) via a **Skill** or **MCP server**. Claims: **~70% token savings**, **1-minute setup, zero config**. The recommended path is the skill (`npx skills add cocoindex-io/cocoindex-code`) — no manual `ccc init`/`ccc index` needed; the skill teaches the agent to initialize, index, search, and keep the index fresh on its own, invoking semantic search automatically when useful (or via `/ccc`). Install via `pipx install 'cocoindex-code[full]'` (batteries-included with local embeddings, default `snowflake-arctic-embed-xs`, no API key) or the slim LiteLLM-only variant. Also distributes as a Claude Code plugin marketplace.

## How we tested it

**Source-grounded inspection — not installed, not run.** No index built, no searches performed, the 70% token-savings claim not measured.

```bash
gh api repos/cocoindex-io/cocoindex-code --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 2175, Apache-2.0, pushed 2026-06-19
gh api repos/cocoindex-io/cocoindex-code/readme --jq '.content' | base64 -d | sed -n '277,367p'        # AST search, skill/MCP install, embeddings
```

## What worked

- **AST-based, not naive chunking.** Parsing structure rather than line-windowing should produce more meaningful retrieval units than text-chunk embeddings.
- **Truly low-friction.** The skill path needs no `init`/`index` step and auto-maintains the index as you work — the agent just searches when helpful. That removes the usual "remember to re-index" failure mode.
- **Local embeddings out of the box.** The `[full]` variant ships `sentence-transformers` so semantic search works with **no API key** (good for privacy and cost); a slim cloud-embedding variant exists for those avoiding ~1 GB of torch deps.
- **Multiple integration surfaces.** CLI, skill, MCP, and a Claude Code plugin marketplace — fits most agent stacks.
- **Credible foundation.** Backed by the actively developed Rust CocoIndex engine, Apache-2.0.

## What didn't work or surprised us

- **Very crowded niche.** Code-search-for-token-savings is the most contested category in the catalog (serena, claude-context, code-context-engine, SocratiCode, gortex, codebase-memory-mcp). The wedge is zero-config + AST + local embeddings, not a new capability.
- **`[full]` is heavy.** Local embeddings pull ~1 GB of torch/transformers; the slim variant needs a cloud key — pick your trade-off.
- **Self-reported 70%.** Token-savings and "just works" claims are vendor-stated and workload-dependent.
- **Index freshness vs. correctness.** Auto-maintained indexes are convenient but stale-index drift on fast-moving repos is the classic risk; not evaluated here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | AST-based semantic search surfaces the right code; agent reads fewer wrong files. |
| Speed | + | Search instead of grep/read; auto-indexing keeps lookups fast. |
| Maintainability | neutral | Self-maintaining index reduces upkeep; another tool/index in the stack. |
| Safety | + / neutral | Local-embeddings variant keeps code on-box (no API key); slim variant sends to a cloud embedder. |
| Cost Efficiency | + | Claimed ~70% token savings + no-API-key local embeddings cut both API and search cost. |

## Verdict

**CONDITIONAL** — cocoindex-code is a well-packaged, Apache-2.0 **AST-based semantic code search** that competes in a crowded field on two real strengths: **genuinely zero-config** (the skill self-initializes and auto-maintains the index) and **local embeddings with no API key**. Adopt it if you want agent-driven semantic search that "just works" without a setup ceremony or a mandatory cloud embedder, and you can absorb the `[full]` install size (or use the slim cloud variant). Against serena (LSP symbol-level edits) and claude-context (Milvus-backed), cocoindex-code's pitch is friction and privacy, not breadth of language tooling. Measure the 70% claim on your repo and watch index freshness before trusting it on fast-moving code.

Compared to neighbors: **serena** does IDE-grade symbol find/refactor over LSP; **claude-context** uses Milvus + embeddings with AST chunking; **code-context-engine**/**SocratiCode**/**gortex** are indexed code-intelligence engines. cocoindex-code's distinguishing pitch is **zero-config AST search with optional fully-local embeddings, delivered as a self-maintaining skill.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cocoindex-code](https://github.com/cocoindex-io/cocoindex-code) | tool | Zero-config AST-based semantic code search (CLI / skill / MCP) built on a Rust transformation engine — `npx skills add` or plugin-marketplace install, claims ~70% token savings and 1-min setup | Agents grep and read whole files to locate code; want fast, local, no-config semantic search the agent uses automatically | serena, claude-context, code-context-engine, SocratiCode, gortex |
