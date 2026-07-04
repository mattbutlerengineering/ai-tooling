# Evaluation: server-memory

**Repo:** [modelcontextprotocol/servers — src/memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory)
**Stars:** 87,453 (monorepo) | **Last updated:** 2026-06-17 (pushed; monorepo created 2024-11-19) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Outer-loop **Reflect** / cross-session continuity — it is the persistence substrate an agent reads at task start and writes at task end, not a stage that produces code.
**Layer:** Infrastructure (a stdio MCP server process holding a knowledge graph; the agent is the only client and decides what to store)

---

## What it does

The official reference **Knowledge Graph Memory Server** from the Anthropic/MCP team — "a basic implementation of persistent memory using a local knowledge graph" so a model can remember facts about the user across chats. Its data model is three primitives: **entities** (named nodes with an `entityType` and a list of `observations`), **relations** (directed, active-voice edges like `John_Smith --works_at--> Anthropic`), and **observations** (atomic string facts attached to an entity). It exposes nine tools — `create_entities`, `create_relations`, `add_observations`, `delete_entities`, `delete_observations`, `delete_relations`, `read_graph`, `search_nodes`, `open_nodes` — plus a live MCP **resource** (`memory://knowledge-graph`) that emits `notifications/resources/updated` on every mutation.

Mechanism: a single TypeScript file (`index.ts`) on `@modelcontextprotocol/sdk` ^1.29.0, persisting to a **newline-delimited JSON file** (`memory.jsonl`; path overridable via `MEMORY_FILE_PATH`, with automatic one-time migration from a legacy `memory.json`). There is no database, no embeddings, no vector search — `search_nodes` is a substring scan over entity names, types, and observation text. It is deliberately minimal: the canonical "here is what an MCP memory server looks like" specimen, designed to be read and copied as much as run.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No server was started, no graph was written, and no MCP client was connected. Every claim comes from the repository: the `src/memory` subtree, its README, `index.ts`, and `package.json` — not from observed runtime behavior. We did not measure recall quality, latency, or token cost; those are reasoned from the code, not benchmarked.

```bash
gh api repos/modelcontextprotocol/servers --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/modelcontextprotocol/servers/contents/src/memory --jq '.[].name'
gh api repos/modelcontextprotocol/servers/contents/src/memory/README.md --jq '.content' | base64 -d   # data model + 9 tools + resource
gh api repos/modelcontextprotocol/servers/contents/src/memory/index.ts   --jq '.content' | base64 -d | grep -nE "MEMORY_FILE|readFile|writeFile|search"  # JSONL persistence, substring search
gh api repos/modelcontextprotocol/servers/contents/src/memory/package.json --jq '.content' | base64 -d   # v0.6.3, sdk ^1.29.0
```

Note: the monorepo's NPM-published license resolves as `NOASSERTION` at repo level, but the package and tree are MIT.

## What worked

- **Canonical, legible reference.** One TypeScript file, three clean primitives, nine well-named tools, and a Dockerfile + tests (`__tests__`, `vitest.config.ts`). If you want to understand the *shape* of an MCP memory server before building or adopting one, this is the source of truth — and the design vocabulary (entity/relation/observation) that most catalog memory tools echo.
- **Genuinely portable and dependency-light.** Single SDK dependency, plain JSONL on disk, `MEMORY_FILE_PATH` override, and a documented Docker run. No service to host, nothing to authenticate, trivially version-controllable or wipeable.
- **Live resource subscription.** Mutations fan out `notifications/resources/updated` on `memory://knowledge-graph`, so a subscribed client sees changes without re-polling — a notably correct MCP-protocol touch for a "basic" server.
- **Maintained and current.** Lives in the actively-pushed official servers monorepo (pushed 2026-06-17), at package v0.6.3 on a recent SDK — not an abandoned demo.

## What didn't work or surprised us

- **The catalog one-liner is wrong.** CATALOG.md line 271 calls it "basic persistent key-value memory." It is not key-value — it is a typed knowledge graph with relations. That entry needs fixing (out of scope here; flagged).
- **Substring search is the ceiling.** `search_nodes` is a literal text scan — no embeddings, ranking, or semantic recall. As the graph grows, the agent's options are a substring query or `read_graph` (the *entire* graph), the latter of which dumps everything into context. There is no summarization, decay, or relevance budget.
- **Storage and recall are entirely the model's job.** The server never decides what is worth remembering; it only executes CRUD. Recall quality depends wholly on the host prompting the model to write good entities/observations and to query before acting — exactly the orchestration that richer tools bundle and this one omits.
- **No multimodal, no consolidation, no learning.** Compared to neighbors it has no overnight consolidation, no correction-driven learning, no vector backend, no timeline. It is a substrate, not a memory *system*.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Persisting typed facts/relations across sessions can prevent re-deriving known context; but substring-only recall and model-dependent writes mean it doesn't *guarantee* the right memory surfaces at the right time. |
| Speed | + | Local JSONL, single dependency, no network/auth — near-zero startup and lookup latency at small scale. Degrades only when `read_graph` is used as a crutch on a large graph. |
| Maintainability | + | One readable file, plain-text store you can diff/version/wipe, MIT, official upstream. Easiest memory backend in the catalog to reason about and audit. |
| Safety | + | Local-only file I/O, no network egress, no host reach beyond one JSONL path. Lowest-attack-surface option among memory tools; the store is human-readable and inspectable. |
| Cost Efficiency | + / − | No infra cost and tiny footprint; but lacking relevance budgeting, naive recall (`read_graph` / broad observations) can balloon context tokens as the graph grows. |

## Verdict

**CONDITIONAL — adopt as a reference and as a minimal local backend; do not expect it to be a memory *system*.** server-memory is the official, MIT, beautifully minimal knowledge-graph specimen: the right thing to read before building or choosing memory tooling, and a fine zero-infra local store for small graphs where you control what gets written. But it deliberately stops at CRUD + substring search — no semantic recall, consolidation, learning, or relevance budgeting — so for real cross-session continuity you'll outgrow it.

Compared to neighbors: **OMEGA** (this user's installed stack) adds semantic search, coordination, checkpoints, and a protocol layer that decides *when* to read/write — capabilities server-memory leaves to the host. **claude-mem** adds semantic search and timeline views; **mem0** and **cognee** add relationship-aware vector backends. server-memory wins decisively on legibility, safety, and zero-dependency portability, and it is the conceptual ancestor most of those tools borrow from — but as a working memory layer it is the floor, not the ceiling.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [server-memory](https://github.com/modelcontextprotocol/servers/tree/main/src/memory) | MCP server | Official reference knowledge-graph memory server — typed entities/relations/observations persisted to local JSONL, with 9 CRUD tools and substring search | Need a minimal, auditable, zero-infra cross-session memory backend and the canonical pattern to build memory tooling from | OMEGA, claude-mem, mem0, cognee, agentmemory (all add semantic recall/consolidation this omits) |
