# Evaluation: memvid

**Repo:** [memvid/memvid](https://github.com/memvid/memvid)
**Stars:** ~15,700 | **Last updated:** 2026-05-27 | **License:** Apache-2.0
**Dev loop stage:** Reflect (Memory & Context)
**Layer:** Infrastructure

---

## What it does

A single-file memory layer for AI agents that replaces complex RAG pipelines. Memvid gives agents persistent, versioned, portable long-term memory with instant retrieval — and crucially, **without a database**: memory lives in a portable single-file artifact rather than a stateful vector store.

The pitch is operational simplicity plus accuracy: drop in a serverless, single-file memory and get long-horizon recall. The README leads with benchmark highlights — claiming higher accuracy than other memory systems on LoCoMo (+35% over SOTA), and large gains in multi-hop (+76%) and temporal (+56%) reasoning versus the industry average. Memory is persistent and versioned, so it travels with the project and can be moved between environments without migrating a database.

## How we tested it

Architecture review against the README and its single-file/no-database design and benchmark highlights (LoCoMo accuracy, multi-hop, temporal). Confirmed the "replace RAG pipeline with a portable single-file memory" positioning and the versioned/serverless properties. The benchmark numbers are the project's own and not independently reproduced. Not run against a live agent, so condition-gated.

```bash
gh api repos/memvid/memvid --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/memvid/memvid/readme --jq '.content' | base64 -d
```

## What worked

- **No database, no infra.** A serverless single-file memory removes the operational weight of standing up and maintaining a vector store — genuinely simpler to adopt and to move.
- **Portable + versioned.** Memory that travels as a file and is versioned fits agent workflows that need reproducible, shareable long-term context.
- **Benchmarks target the right axes.** If the LoCoMo / multi-hop / temporal gains hold, those are exactly the hard parts of conversational memory.

## What didn't work or surprised us

- **Self-reported benchmarks.** The headline accuracy/multi-hop/temporal numbers are project-authored; validate on your own workload before trusting them.
- **Single-file scaling questions.** A single-file model is elegant for portability but raises questions at very large scale / high concurrency that the README doesn't fully answer.
- **Crowded memory space.** Overlaps supermemory, memU, cognee, LightRAG; the differentiator is the database-free single-file artifact.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Claims strong long-horizon/multi-hop/temporal recall (unverified) |
| Speed | + | Instant retrieval; no DB round-trip |
| Maintainability | + | Single-file, versioned, portable — no store to operate |
| Safety | neutral | Memory layer; no direct safety effect |
| Cost Efficiency | + | Serverless, no vector-DB infra to run |

## Verdict

**CONDITIONAL**

Adopt when you want agent long-term memory without operating a vector database and value portability/versioning — the single-file model is its standout. Verify the self-reported LoCoMo/multi-hop/temporal gains on your own data before relying on them, and check scaling behavior for your concurrency needs. For a user already on claude-mem + OMEGA, it overlaps existing memory; the draw is the database-free portability.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memvid](https://github.com/memvid/memvid) | tool | Single-file memory layer for AI agents (Apache-2.0, ★16K) — persistent, versioned, portable long-term memory with instant retrieval and no database; reports SOTA on LoCoMo as a drop-in RAG-pipeline replacement | Standing up RAG/vector infra is heavy and stateful; want a serverless, single-file, portable memory to drop into an agent | supermemory, memU, cognee, LightRAG |
