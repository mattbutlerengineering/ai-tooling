# Evaluation: squish-memory

**Repo:** [michielhdoteth/squish](https://github.com/michielhdoteth/squish) (npm: [`squish-memory`](https://www.npmjs.com/package/squish-memory))
**Stars:** 4 | **Last updated:** 2026-06-15 (created 2026-01-13) | **License:** MIT
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A local-first persistent memory runtime for AI coding agents, distributed as an npm global (`squish-memory`) that exposes a CLI (`squish`), an MCP server (`squish-mcp`, 15 tools), a Claude Code plugin (lifecycle hooks + a `squish-memory` skill), and an optional paid cloud (`squishplugin.dev`). It markets itself as cross-agent: Claude Code, Codex, Cursor, Copilot, Gemini CLI, OpenCode, OpenClaw, Cline, Goose, Windsurf, and any MCP/HTTP client share one backend.

The mechanism: `squish install --all` auto-detects installed agents and wires hooks for each. For Claude Code it installs three lifecycle hooks — `SessionStart` (sync, 30s, loads memory context), `Stop` (async, 15s, "saving checkpoint"), and `SessionEnd` (async, 30s) — that shell out to `scripts/session-*.sh`. A 4-stage pipeline processes memories: **Capture** filters noisy tool output and promotes decisions/constraints/preferences; **Filter** dedupes, resolves contradictions, scores importance; **Store** persists to SQLite (default) or PostgreSQL (team mode) with knowledge-graph edges (`kuzu`) and embeddings; **Retrieve** runs hybrid search (BM25 keyword + semantic cosine + recency, fused with RRF). It separates three layers: **Recall** (durable distilled facts — decisions, preferences, constraints, beliefs), **Sessions** (raw searchable past agent runs as evidence), and **Remember** (write to long-term memory). Memories decay over time and a knowledge graph reinforces relationships from usage. Embeddings are pluggable — the zero-dependency default is local TF-IDF (`core/embeddings/local-embeddings.ts`, 768-dim per README), with optional `@huggingface/transformers` (`transformers-local.ts`) and Google multimodal providers; no external LLM or API key is required for the local path.

## How we tested it

Repo + package identification and source/README review — **not a hands-on install.** The entry arrived UNLINKED and `gh search repos squish-memory` returns only a false positive (an 8-year-old's Squishmallow memory card game, 0 stars). I traced the real project through the **npm registry**: `squish-memory` v1.6.0 (description "Local-first memory runtime for Claude Code, Codex, ChatGPT, and AI agents") declares `repository: git+https://github.com/michielhdoteth/squish` and `homepage: https://squishplugin.dev`. I then verified that GitHub repo's metadata, releases, README, plugin manifest, hooks, and source tree directly via the `gh` API rather than trusting the README.

I deliberately **did not run `npm install -g squish-memory && squish install --all`**: it is a 4-star, single-author package whose installer writes lifecycle hooks into the live agent configs of every detected agent (`--all`) and shells out via `scripts/session-*.sh`. Installing it would risk hook collisions with the user's existing live memory stack (claude-mem, OMEGA, superpowers, claude-reflect) and execute unvetted code against real session data — the same posture taken in `longhand.md` and `memsearch.md`. Honest method statement: every claim below is grounded in npm metadata, GitHub API source inspection, and the project's own published numbers — no metrics were produced by me.

```bash
# Identification (GitHub search alone fails — false positive only)
gh search repos squish-memory --json fullName,description,stargazersCount,url
curl -s https://registry.npmjs.org/squish-memory/latest   # → repository: michielhdoteth/squish, homepage squishplugin.dev

# Verification against the real repo
gh api repos/michielhdoteth/squish --jq '{stars,license:.license.spdx_id,pushed_at,created_at,open_issues}'
gh api repos/michielhdoteth/squish/releases --jq '[.[].tag_name]'   # v1.6.0,v1.5.0,v1.2.0,v1.1.5,v1.0.2,v0.2.7
gh api repos/michielhdoteth/squish/readme --jq '.content' | base64 -d
gh api repos/michielhdoteth/squish/contents/plugin/claude-code/hooks/hooks.json --jq '.content' | base64 -d
gh api "repos/michielhdoteth/squish/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(startswith("tests/"))]|length'  # 98 test files
gh api "repos/michielhdoteth/squish/git/trees/HEAD?recursive=1" --jq '[.tree[].path|select(test("embed|security"))]'
```

Verified in source: 3 Claude Code hooks (`SessionStart` sync / `Stop` + `SessionEnd` async) in `plugin/claude-code/hooks/hooks.json`; plugin layers for claude-code, codex, and openclaw; a `core/security/` module (`secret-detector.ts`, `privacy.ts`, `governance.ts`, `encrypt.ts`); a pluggable `core/embeddings/` layer (local TF-IDF + transformers + Google); SQLite (`better-sqlite3`) default with PostgreSQL (`pg`/`pgvector`/`drizzle-orm`) and `kuzu` graph deps; 98 test files; MIT; single human committer (+ dependabot); 1 open issue.

## What worked

- **The repo was confidently identifiable and is genuinely an AI-agent memory runtime**, not the Squishmallow false positive. npm `repository`/`homepage` fields and the GitHub source tree corroborate each other — verified, not fabricated.
- **Zero-dependency local default.** SQLite + local TF-IDF embeddings means no external vector DB and no API key on the free path — a cleaner default than mem0 (Qdrant + cloud) and a notable selling point over memsearch's Milvus dependency. This is the same SQLite-first posture that makes claude-mem attractive.
- **Lean, fail-safe Claude Code hook footprint.** Only 3 hooks, with `Stop` and `SessionEnd` async (won't block the turn) and bounded timeouts (15–30s). Lower collision risk than agentmemory's 12 hooks — parity with longhand (3 hooks) and memsearch (4).
- **Genuinely broad cross-agent reach** — explicit plugins/hooks for Claude Code, Codex, and OpenClaw, plus MCP/HTTP config for ~12 more agents. If a user spans many harnesses, one shared backend is real value (same axis memsearch wins on).
- **Richer memory model than the summary-only peers** — three explicit layers (durable Recall vs raw Sessions vs Remember-write), a `kuzu` knowledge graph, decay, contradiction detection, and temporal facts. The Sessions-as-evidence layer overlaps conceptually with longhand's raw-transcript thesis.
- **Substantial test surface and security module for a 4-star project** — 98 test files (incl. `hook-system`, `hook-merge`, embedding-model validation) and a dedicated `core/security/` with a secret detector, privacy, governance, and AES-256-GCM encryption. More engineering hygiene than the star count suggests.

## What didn't work or surprised us

- **4 GitHub stars, single author, ~5 months old, no external contributors.** Bus-factor of one on infrastructure that ingests your entire dev history across every agent. This is the dominant adoption risk — and it is *lower* maturity than the memory CONDITIONALs already cataloged (longhand 10 stars, memsearch 2.1K, agentmemory 23K).
- **Commercial/SaaS orientation.** The README is a funnel for "Squish Cloud" ($9–$99/mo + a "Founder Pass" launch offer) with pricing tables and signup CTAs. The local tier is free and self-contained, so this is upsell rather than lock-in — but the project exists partly to sell cloud sync, which colors its self-comparisons.
- **Self-reported, partly soft benchmarks.** "9/9 core tests (100%)" is a unit-test pass rate, not a retrieval metric; the one real retrieval number is **LoCoMo 65%** (100 questions) — published but not independently reproduced, and modest. No R@5-style head-to-head against the alternatives it tables itself against.
- **Embedding claim has a minor inconsistency.** README says "Vector search with TF-IDF embeddings (768-dimensional)," yet the package also ships `@huggingface/transformers` and a `transformers-local.ts` provider. Embeddings are pluggable (TF-IDF is the zero-dep default), so it's accurate-but-incomplete framing rather than a falsehood — worth noting given the "no LLM required" marketing.
- **Heavy dependency tree for the full package** despite the "283 KB package" claim — `kuzu` (graph), `pg`/`pgvector`/`drizzle-orm`, `redis`, `@neondatabase/serverless`, `sql.js`, and optionally `@huggingface/transformers`. The local-SQLite path may not exercise most of these, but the install surface is larger than SQLite-only peers.
- **Self-authored competitor comparison table** (vs CLAUDE.md, agentmemory, mem0) is marketing, not a neutral evaluation — every row favors Squish. Treat as vendor framing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Hybrid retrieval (BM25 + semantic + recency, RRF) over auto-captured decisions/sessions aids recall; only self-reported LoCoMo 65% to quantify, no independent benchmark |
| Speed | + | Local embeddings ~6.6ms / hybrid search ~6.1ms (self-reported); async Stop/SessionEnd hooks don't block the turn |
| Maintainability | neutral | SQLite default + 98 tests + security module are positives, but single-author, 4-star, ~5-month-old, pre-stable cloud-funnel project adds real maintenance/bus-factor risk |
| Safety | + | Local-first default (no network, no API key), AES-256-GCM at rest, dedicated `core/security/` with secret detector; cloud tier sends memory off-box if enabled |
| Cost Efficiency | + | Zero API calls on the local path (local TF-IDF embeddings, SQLite); ~50-200 token avg injection claimed; cloud is the paid upsell, not required |

## Verdict

**SKIP**

squish-memory is a real, correctly-identified local-first memory runtime ([michielhdoteth/squish](https://github.com/michielhdoteth/squish), npm `squish-memory`) with a sound architecture — SQLite-default, zero-API local embeddings, a lean 3-hook Claude Code footprint, a three-layer memory model, and more test/security hygiene than its 4 stars imply. But it is **a thinner, less-proven duplicate of tools the catalog already has**, not an additive capability. Its differentiators are exactly the ones already covered: SQLite + local-embeddings memory is claude-mem's (ADOPT) territory; broad cross-agent reach is memsearch's (CONDITIONAL); raw "sessions as evidence" recall is longhand's (CONDITIONAL) lossless-transcript thesis. It beats none of them on its own axis — it has 4 stars and one author against claude-mem's mature ecosystem, memsearch's 2.1K-star vendor backing, and longhand's verbatim-recall depth — and it layers a SaaS funnel on top. For this Claude Code-centric user, claude-mem + OMEGA already cover durable memory and decision recall, with memsearch/longhand cataloged for the cross-agent and forensic-recall edge cases. There is no gap squish-memory fills.

KEEP the catalog entry (now linked to the verified repo) as a discovery record; re-evaluate only if it gains independent contributors, a stable post-cloud-launch trajectory, and reproducible retrieval benchmarks that beat the incumbents.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [squish-memory](https://github.com/michielhdoteth/squish) | MCP server | Local-first persistent memory runtime for AI agents — SQLite + local embeddings + knowledge graph, hybrid recall, cross-agent, no API key | Agents forget across sessions; CLAUDE.md-style files cap out and don't work across tools — needs durable, searchable, cross-agent memory | claude-mem, OMEGA, server-memory, memsearch, longhand, mem0, agentmemory |
