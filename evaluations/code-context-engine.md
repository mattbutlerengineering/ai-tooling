# Evaluation: code-context-engine (CCE)

**Repo:** [elara-labs/code-context-engine](https://github.com/elara-labs/code-context-engine)
**Stars:** 175 | **Last updated:** 2026-06-17 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (codebase exploration before/during implementation)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "Index codebase, agents search instead of reading files — 94% token savings." CCE is a local-first MCP server (Python 3.11+, PyPI package `code-context-engine`) that indexes a codebase into semantic chunks and exposes search over them so the agent retrieves the relevant 40-line function instead of reading an 800-line file.

The mechanism: `cce init` runs tree-sitter AST parsing to chunk code into functions/classes/modules (AST-aware for 10 extensions across Python/JS/TS/PHP/Go/Rust/Java, line-range fallback for 40+ more), embeds the chunks locally (fastembed/ONNX via the `[local]` extra, or Ollama `nomic-embed-text`), and stores vectors + FTS5 + a code graph + a compression cache in three SQLite files (sqlite-vec). It then auto-detects the editor and writes the MCP config (`.mcp.json` for Claude Code) plus agent instruction files (`CLAUDE.md`), and installs git hooks that keep the index current (sub-1s re-index, 96% embedding cache hit). At query time it exposes **9 MCP tools** — the core being `context_search` (hybrid vector + BM25 via Reciprocal Rank Fusion, graph expansion over CALLS/IMPORTS edges, confidence scoring blending similarity 50% / keyword 30% / recency 20%), `expand_chunk`, and `related_context`. Compression then truncates retrieved chunks to signatures + docstrings (or LLM-summarizes if Ollama is up).

Beyond search, CCE bundles two extra capabilities most pure-search MCPs don't: (1) **cross-session memory** — `record_decision` / `record_code_area` / `session_recall` persist architecture decisions in SQLite (overlaps the memory category: OMEGA, claude-mem); and (2) **output compression** — `cce init` writes "caveman-style" terseness rules into `CLAUDE.md` that apply to the whole session (overlaps the caveman skill), plus a `set_output_compression` tool with off/lite/standard/max levels. A `cce savings` CLI and web `cce dashboard` track token/dollar savings against live Anthropic pricing.

## How we tested it

**Evidence:** REVIEW

**Method: repo + README + benchmark-doc inspection. Not installed or run hands-on.** No `cce init` was executed and no MCP session was driven; the 94%/89%/0.90-recall figures below are the author's published benchmarks, not numbers we reproduced. Honesty note per the catalog integrity rule: this is an architecture/maturity review calibrated against the existing codegraph (ADOPT) and agentmemory (CONDITIONAL) evaluations.

What was actually inspected:

```
gh api repos/elara-labs/code-context-engine --jq '{stars,license,description,pushed_at,created_at,archived,language}'
# {stars:175, license:MIT, lang:Python, created:2026-04-27, pushed:2026-06-17, archived:false}

gh api repos/elara-labs/code-context-engine/readme --jq '.content' | base64 -d   # full README
gh api repos/elara-labs/code-context-engine/releases --jq '.[].tag_name'         # v0.4.23 ... v0.4.19 (frequent)
gh api repos/elara-labs/code-context-engine/git/trees/main --jq '.tree[].path'   # benchmarks/ tests/ pyproject.toml present
```

Findings cross-referenced against `evaluations/codegraph.md` (the catalog's ADOPT code-intelligence tool) and the catalog's other code-search peers (repomix, context7, trace-mcp, SocratiCode, gortex).

## What worked

- **Reproducible, honest benchmarks.** Multi-language results published in-repo (FastAPI Python 94% retrieval savings / 0.90 R@10; chi Go 76% / 0.67; fiber Go monorepo 93% / **0.07**) with a `benchmarks/run_benchmark.py` you can re-run. Critically, the README itself flags that the 94% is measured against *full-file reads*, not against Claude Code's actual grep/partial-read behavior — so real-world savings are lower. That self-correction is rare and raises trust.
- **Genuinely local and private.** sqlite-vec + local embeddings (fastembed ONNX on CPU, or Ollama). No cloud, no API keys for indexing. Secret files (.env, *.pem) are excluded; content is scanned for AWS/GitHub/Slack/Stripe keys + JWTs; PII scrubbed from memory writes; MCP paths validated against traversal.
- **Editor-agnostic single index.** One `cce init` configures Claude Code, VS Code/Copilot, Cursor, Gemini CLI, Codex, OpenCode, Tabnine — useful for multi-editor teams; codegraph and most peers are narrower.
- **Lean footprint and fast re-index.** sqlite-vec replaced LanceDB (217 MB → 2 MB index); ~17 MB core install (189 MB with local embeddings); sub-1s re-index via content-hash cache. Git hooks keep it current automatically (like codegraph's auto-sync).
- **Three-in-one value:** semantic search + cross-session memory + output compression in a single package, each with its own savings ledger bucket.
- **Active maintenance / CI:** v0.4.23 with frequent releases, `tests/` directory, CI across macOS/Linux/Windows × Python 3.11/3.12/3.13, listed in the MCP Registry.

## What didn't work or surprised us

- **Low maturity: 175 stars, created 2026-04-27 (under two months old), still v0.x.** This is the decisive contrast with codegraph (51K stars, ADOPT). Single-org project, pre-1.0, API surface and index format may churn.
- **Recall is brittle on monorepos.** Self-reported R@10 of **0.07** on the fiber Go monorepo means it missed the right files in 9+ of 10 top-10 results there — the exact large-codebase scenario where "search instead of read" matters most. Go's shorter files also shrink the savings headroom (76% on chi).
- **Headline 94% is a best-case, not-vs-Claude-Code number.** Apples-to-apples savings against normal Claude Code (which already greps and partial-reads) are unstated and lower. Real ROI is unproven.
- **Capability + hook overlap.** Output compression duplicates the caveman skill (ADOPT); cross-session memory duplicates claude-mem/OMEGA; git/lifecycle hooks can collide with an existing memory/hook stack. Running CCE alongside a memory tool risks two systems writing decisions.
- **Build dependency friction.** Needs a C compiler + cmake (tree-sitter grammars) — heavier setup than a pure-npm MCP.
- **Compared to codegraph it's a different shape, not strictly better:** CCE = embedding/semantic retrieval + memory + compression; codegraph = structural call/dependency graph queried for definitions, callers, callees. Codegraph answers "who calls this?"; CCE answers "where's the code about payments?".

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Author claims quality unchanged (0.90 R@10 on FastAPI), but 0.07 R@10 on a monorepo means relevant files can be silently missed |
| Speed | + | Retrieving chunks instead of whole files reduces context and round-trips; 0.4ms p50 retrieval, sub-1s re-index |
| Maintainability | neutral | Helps agents find code; doesn't improve the code itself |
| Safety | + | Local-first, secret-file exclusion, credential scanning, PII scrubbing, path-traversal validation — stronger default posture than most peers |
| Cost Efficiency | + | Targets input tokens (85-95% of bill); 94% retrieval savings benchmarked (best case), plus optional output compression |

## Verdict

**CONDITIONAL**

CCE is a well-engineered, honestly-benchmarked, local-first semantic-search MCP with strong security defaults and useful memory/compression extras. But at 175 stars and under two months old (v0.x), it is far below the maturity bar that earned codegraph an ADOPT (51K stars), and its monorepo recall (R@10 0.07 on fiber) is a real liability for the large-codebase case the tool exists to serve.

**vs codegraph (the key comparison): additive, not redundant, and not yet better.** They solve adjacent problems — codegraph gives agents *structural* graph awareness (definitions, callers, callees, dependencies); CCE gives *semantic* retrieval (find code by meaning) plus cross-session memory and output compression. You could run both. But codegraph is the safer default today on maturity alone.

**Use CCE when:** you want one local index across multiple editors (Claude Code + Cursor + VS Code + Gemini/Codex), you prioritize a strong privacy/security posture, your codebase is small-to-medium (not a sprawling monorepo), and you don't already run a separate memory tool (claude-mem/OMEGA) or caveman whose functions CCE would duplicate. Re-evaluate for ADOPT if it crosses ~1K+ stars / reaches 1.0 with a stable index format and improves monorepo recall.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [code-context-engine](https://github.com/elara-labs/code-context-engine) | MCP server | Index codebase, agents search instead of reading files — 94% token savings | AI agents read too many files and waste tokens; indexed semantic search is faster and cheaper | repomix, codegraph, context7, trace-mcp, SocratiCode, gortex, caveman, claude-mem |
