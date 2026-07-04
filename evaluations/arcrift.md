# Evaluation: ArcRift

**Repo:** [Eshaan-Nair/ArcRift](https://github.com/Eshaan-Nair/ArcRift)
**Stars:** 234 | **Last updated:** 2026-06-07 (created 2026-04-21) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

ArcRift is a local-first persistent-memory layer for AI tools whose distinguishing thesis is the **browser-chat ↔ IDE-agent bridge**: a Chrome/Firefox extension captures conversations from web chat UIs (Claude.ai, ChatGPT, Gemini, DeepSeek, Grok, Copilot, Mistral), and a native MCP server exposes that same memory to coding agents (Claude Code, Cursor, Windsurf, Claude Desktop). Both halves read/write one shared local `ArcRift.db`, so a decision you reach in a ChatGPT web chat is immediately recallable inside Claude Code, and vice versa. No other catalog memory entry centers this cross-surface (web ↔ IDE) sync.

Mechanically, capture runs two parallel tracks. The **vector track** chunks text (300-word sliding window, 80-word overlap), embeds it with a local Ollama model (`nomic-embed-text`, 768-dim) into SQLite-vec `vec0` virtual tables, and queues sentence-level embeddings as a background job. The **graph track** sends text to a local Ollama LLM (`llama3.1:8b`, with Groq as an optional cloud fallback) to extract subject-relation-object triples (22 entity types, 20+ relation types) into a SQLite facts table. Recall fuses three engines (sentence vectors, chunk vectors, FTS5 prefix keyword) plus graph facts, applies HyDE (embeds a hypothetical answer alongside the query), then "surgical sentence trimming" returns only the matching sentences from each chunk (claimed up to 95% noise reduction) with small-to-big parent-chunk expansion. The MCP surface is **seven tools**: `recall_context`, `store_memory`, `search_memory`, `list_projects`, `get_project_summary`, `identify_active_project`, `prune_memory`. Storage defaults to zero-Docker SQLite (WAL mode for concurrent extension/dashboard/MCP access); a Docker profile swaps in Neo4j + MongoDB + ChromaDB. A React 19 + D3.js dashboard on `localhost:3001` visualizes the knowledge graph and a background job queue.

## How we tested it

**Evidence:** REVIEW

Architecture review via the GitHub API — disambiguated the (unlinked) catalog name, confirmed repo identity, read the full README, inspected the recursive file tree (`backend/src/mcp/tools/*`, `extension/`, services), the release list, and the contributor list. **Not installed or run hands-on.** The hands-on cost here is unusually high: ArcRift requires a running Ollama daemon (pulling `nomic-embed-text` + `llama3.1:8b` models), a persistent local backend process on port 3001, and a manually side-loaded browser extension — and standing up a second memory layer with its own MCP server + store risks colliding with the user's live claude-mem (ADOPT) + OMEGA setup. Same rationale applied to the prior memory-category evals (agentrecall-mcp, memsearch, agentmemory). Calibrated against `evaluations/agentrecall-mcp.md` (CONDITIONAL), `evaluations/memsearch.md` (CONDITIONAL), and claude-mem (ADOPT — the user's choice).

```bash
gh search repos ArcRift --limit 30 --json fullName,description,stargazersCount,url,updatedAt   # disambiguate the unlinked name
gh api repos/Eshaan-Nair/ArcRift --jq '{description,stars:.stargazers_count,license:.license.spdx_id,pushed_at,created_at,open_issues,forks:.forks_count,homepage,language}'
gh api repos/Eshaan-Nair/ArcRift/readme --jq '.content' | base64 -d
gh api "repos/Eshaan-Nair/ArcRift/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/Eshaan-Nair/ArcRift/releases --jq '.[].tag_name'        # v1.6.3 latest, ~10+ releases
gh api repos/Eshaan-Nair/ArcRift/contributors --jq '.[].login'      # Eshaan-Nair + dependabot + 2 others
```

**Repo identity confirmed.** `gh search repos ArcRift` returns exactly one match: `Eshaan-Nair/ArcRift` — 234 stars, 31 forks, MIT, TypeScript, homepage `arcrift.vercel.app`, description verbatim matching the tool ("Persistent local memory layer for AI… extension and a native MCP server to sync context… from your browser chats… to your local IDE agents… powered by a local SQLite knowledge graph"). The repo went through prior rebrands (npm `glia-ai-setup`, `synq-setup` → current `arcrift-setup`), so the catalog name maps cleanly to this single repo.

## What worked

- **Genuinely distinct axis — web-chat ↔ IDE memory bridge.** The killer feature is bidirectional sync between *browser* AI chats and *IDE* coding agents over one shared SQLite store. No other catalog memory entry (claude-mem, agentmemory, SimpleMem, OMEGA, memsearch, AgentRecall) bridges the web-UI surface to the coding-agent surface. For users who plan in ChatGPT/Claude.ai web then implement in Claude Code, this closes a real gap. memsearch's cross-agent reach is IDE-to-IDE; ArcRift's is web-to-IDE — a different, complementary axis.
- **Local-first, zero-cloud default with strong privacy posture.** Embeddings and graph extraction both run locally via Ollama; nothing leaves the box unless you opt into the Groq fallback key. PII scrubbing (API keys, JWTs, connection strings, emails, IPs → `[REDACTED]`) happens in the browser *before* data reaches the backend. CORS locked to localhost, Helmet headers, and retrieved chunks are scanned for 10 prompt-injection patterns before injection. This is a Safety profile on par with claude-mem / agentmemory.
- **Lean, sensibly-named MCP surface — 7 tools.** Far below agentmemory's 53, comparable to the focused surfaces of memsearch (3 skills) and AgentRecall (5 default). Notably includes `prune_memory` for surgically correcting outdated facts and `identify_active_project` for CWD-based project auto-detection.
- **Thoughtful retrieval engineering.** Three-engine hybrid fusion (sentence + chunk vectors + FTS5) + HyDE + surgical sentence trimming + small-to-big expansion is a coherent, modern RAG pipeline, and the README documents concrete tuning decisions (0.30 trim threshold, FTS5 prefix matching, history-aware fallback, 5-char sentence filter).
- **Real engineering surface and active maintenance.** TypeScript monorepo (backend MCP + REST, browser extension with multi-strategy DOM resolver across 7 platforms, React/D3 dashboard), CI + integration-test + release + selector-check GitHub workflows, a SQLite storage test, dead-letter queue with retry/backoff, ghost-job recovery, WAL concurrency, npm `arcrift-setup` one-command bootstrap, multiple docs (ARCHITECTURE, RAG_PIPELINE, SECURITY, SELF_HOSTING). ~10+ releases through v1.6.3, pushed within ~2 weeks of evaluation.

## What didn't work or surprised us

- **Hard Ollama dependency raises the adoption floor.** Both embeddings *and* graph extraction require a running Ollama daemon with two pulled models (`nomic-embed-text` + `llama3.1:8b`, several GB). claude-mem and agentmemory get strong recall from bundled/local embeddings without standing up a separate LLM runtime. For a user already running claude-mem with no Ollama dependency, this is meaningful operational overhead for the IDE-side benefit alone.
- **Desktop install path is Windows-`.exe`-first.** The "easy way" install points to `ArcRift_Installer.exe` and config examples lean Windows (`%APPDATA%`, `.bat` launchers, a checked-in `backend/bin/node.exe`). macOS/Linux users fall back to the `npx arcrift-setup` / build-from-source path. The product clearly originated on Windows; macOS maturity is unproven from sources.
- **Benchmarks are self-run and small-scale.** The headline 90% Recall@1 (web) and 90% total recall (MCP) come from the author's own scripts on tiny corpora — the MCP benchmark is **10 facts / 30 queries**, the web benchmark 20 facts / 60 queries. These are credible internal smoke tests, not reproducible third-party benchmarks like agentmemory's LongMemEval-S (500 questions). Recall quality at real scale is unverified — same caveat applied to memsearch (no published benchmarks) and AgentRecall (3–6-item smoke test).
- **Single-author, young, persistent-process project.** Effectively one author (`Eshaan-Nair`) plus dependabot and two minor contributors; created Apr 2026. Adopting it means trusting a young single-author infrastructure layer that runs a persistent backend on port 3001 plus an Ollama daemon — a larger always-on footprint than a SQLite-file-only peer.
- **Store/MCP collision risk with the live setup.** ArcRift wants its own MCP server, its own `ArcRift.db`, and (for full value) its own always-on backend + browser extension. The user already runs claude-mem (session hooks + store) and OMEGA. Two recall layers both injecting context risks duplicate/conflicting context, with no documented coexistence strategy.
- **Manual capture discipline on the IDE side.** Unlike claude-mem's transparent session hooks, ArcRift's MCP memory relies on the agent explicitly calling `store_memory` after work and `recall_context` at session start (the browser side auto-injects, but the coding-agent side does not auto-hook by default per the README usage guide).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Three-engine hybrid fusion + HyDE + graph facts + surgical trimming targets recall of past decisions; but recall numbers come from a 10–20-fact self-run benchmark, not validated at scale |
| Speed | + | 7 lean MCP tools, async background sentence indexing (instant save), WAL concurrency; offset by the local Ollama LLM extraction step on capture |
| Maintainability | neutral | Clean TS monorepo with CI and good docs, but young (Apr 2026), effectively single-author, and runs a persistent backend + Ollama daemon vs a file-only peer |
| Safety | + | Zero-cloud default, browser-side PII scrubbing, localhost-only CORS, Helmet headers, prompt-injection scanning of recalled chunks |
| Cost Efficiency | + | Free local embeddings + extraction (no API key required; Groq fallback opt-in), small tool surface; cost is local compute/RAM for Ollama, not API spend |

## Verdict

**CONDITIONAL**

ArcRift is a credible, MIT-licensed, local-first memory tool whose real differentiator is the **browser-chat ↔ IDE-agent bridge** — syncing memory between web AI UIs and coding agents over one shared SQLite store, an axis no other catalog memory entry covers. That makes it *additive*, not a thin duplicate: agentmemory competes on benchmarked recall and platform breadth, memsearch on cross-IDE portability, AgentRecall on correction-first compounding, and ArcRift on web-to-IDE unification. Use it when your real pain is **"I plan and decide in ChatGPT/Claude.ai web chats, then lose all that context when I switch to my coding agent"** — and you're willing to run Ollama and a persistent local backend.

For this user's case — Claude Code, local-first, already on claude-mem (ADOPT) + OMEGA — it does **not** displace claude-mem. It is far younger (234 stars, single-author, created Apr 2026), its recall is validated only on a 10–20-fact self-run benchmark, its hard Ollama dependency and persistent-backend footprint exceed claude-mem's file-only model, the desktop install is Windows-first, and adopting a second MCP recall layer risks colliding with the live claude-mem/OMEGA setup. Like agentrecall-mcp and memsearch (both CONDITIONAL), it wins on a specific axis (web↔IDE bridge) but loses to claude-mem on battle-testing and Claude Code ecosystem fit. ADD the catalog entry as CONDITIONAL — not ADOPT, not SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ArcRift](https://github.com/Eshaan-Nair/ArcRift) | tool | Local-first memory layer bridging browser AI chats and IDE coding agents via a shared SQLite knowledge graph | Context from web chats (ChatGPT, Claude.ai) is lost when switching to coding agents; need one local memory shared across both surfaces | claude-mem, memsearch, agentmemory, AgentRecall-MCP, OMEGA, mem0 |
