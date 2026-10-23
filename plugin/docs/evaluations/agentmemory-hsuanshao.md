# Evaluation: AgentMemory (hsuanshao)

**Repo:** [hsuanshao/AgentMemory](https://github.com/hsuanshao/AgentMemory)
**Stars:** n/a (no `repo-metadata.json` record for this slug; no fresh lookup in this pass) | **Last updated:** n/a (upstream HEAD at test time: 2026-10-23) | **License:** BUSL-1.1 (read from the cloned `LICENSE`, not the metadata cache)
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Self-hosted team memory service for AI agents, written in Rust (`memory-core`, the `amem` client) with a TypeScript panel. Conversations land as L0 turns (SQLite + FTS5, or PostgreSQL + pgvector); an LLM-driven background pipeline distils them into L1 facts, L2 scenes and an L3 persona; `/v3/recall` combines BM25 and vector search. Memory is scoped department → team → agent → user, and clients authenticate with a per-user key. The `amem` client plugs into Claude Code, Codex, Antigravity and Hermes hooks.

## How we tested it

**Evidence:** RUN

**Hands-on** — cloned `hsuanshao/AgentMemory` at HEAD (commit dated 2026-10-23, crate version 0.4.1), built `memory-server` and `amem` with `cargo build --release` (Rust 1.97, Linux, 4 cores), started the server with no LLM and no embedding provider configured, and drove its HTTP API with a fixed planted-fact fixture. Also ran the upstream `cargo test --workspace` suite.

```
git clone --depth 1 https://github.com/hsuanshao/agentmemory
cargo build --release -p memory-server -p memory-client     # Finished in 4m 36s
AGENT_MEMORY_API_KEY=evalkey AGENT_MEMORY_DATA_DIR=./data AGENT_MEMORY_HOST=127.0.0.1 AGENT_MEMORY_PORT=8420 memory-server
  -> memory-core listening addr=127.0.0.1:8420 auth=true llm=false embedding=false
POST /v3/internal/meta/user/init-admin  -> 200 (user_id, user_key, team_id, agent_id)
60 x POST /v3/conversation/add          -> 60 turns ingested in 0.32s (count reports 120 rows: user turn + assistant "ack")
12 x POST /v3/conversation/search       -> fact turn in top-5 for 12/12 queries, MRR 1.000
12 x POST /v3/recall                    -> strategy "bm25", memories [] for 12/12 queries
naive token-overlap baseline (python)   -> fact turn in top-5 for 12/12 queries, MRR 1.000
cargo test --workspace                  -> 257 passed, 0 failed (14 result lines)

isolation / safety probes (second user "bob", member of the same team):
  bob searches admin's facts            -> 200, 0 results
  admin searches bob's private note     -> 200, 0 results
  bob searches his own note             -> 200, 1 result
  bob names admin's user_id             -> 403 permission_denied: role does not allow this access
  request with no user key              -> 401 unauthorized: missing_user_key
  stored text "sk-proj-… password=Hunter2!…" -> read back as "[REDACTED:openai-key]" and "[REDACTED:secret-assignment]"
```

## Test design

- **Task/corpus:** 60 single-turn conversation messages, shuffled with a fixed seed: 12 planted-fact turns (e.g. "staging database is postgres 16 on port 54329") and 48 topical distractors that deliberately share vocabulary with the facts (retry, webhook, Kafka, backups, flags). Each fact has one paraphrased question. Fixture and driver lived under `/tmp/eval-agentmemory-hsuanshao/work/` (not committed).
- **Baseline:** a naive keyword-overlap ranker over the same 60 turns (count of shared lowercase tokens), the "no memory service" arm.
- **Metric:** fact turn present in top-5 (hit@5, k/12) and mean reciprocal rank.
- **Reproduce:** build as above, start the server with the env shown, then `python3 run.py` (init admin, ingest, search, recall, score) and `python3 iso.py` (second user, isolation and redaction probes).

## What worked

- Builds from a clean clone with stock Rust and starts keyless in a few seconds; the startup line states `llm=false embedding=false` honestly.
- L0 keyword search (`/v3/conversation/search`) put the planted turn in the top 5 for 12/12 queries, MRR 1.000, on a fixture with 48 near-vocabulary distractors.
- The upstream suite is real: 257 tests across the workspace pass, including end-to-end and worker/dead-letter tests.
- Team isolation behaves as documented: a member reads only their own L0, naming another user is a 403, a missing key is a 401.
- Secret redaction ran at ingest: an OpenAI-style key and a `password=` assignment were replaced before storage.

## What didn't work or surprised us

- The fixture is too easy to discriminate: the naive keyword baseline also scored 12/12, so this run shows the L0 search works but does not show it beats grep. Paraphrase-heavy queries are where a vector arm would matter, and no embedding endpoint was available.
- `/v3/recall`, the endpoint the hooks call before each prompt, returned an empty `memories` list for every query. With no LLM configured nothing is distilled into L1, so recall has nothing to return; L0 turns are searchable only through `conversation/search`. The headline value (facts, scenes, persona, distillation quality) is therefore unmeasured here.
- Needs a distillation LLM (OpenAI-compatible endpoint or a local `claude`/`codex`/`agy` CLI) to deliver its core function; none was available.
- License is BUSL-1.1 with an Additional Use Grant capping free production use at one department and ten members for organisations (personal and non-profit use is free); `crates/memory-client/` and `clients/` are MIT. The `CATALOG.md` row still reads "⚠️ no license", which the tree contradicts. Human follow-up, not edited here.
- Docker, Postgres/pgvector, Redis, the panel and the Claude Code hook integration were out of reach in this sandbox and are untested.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | L0 search 12/12 hit@5, but the keyword baseline matched it and L1–L3 distillation was untested |
| Speed | + | 60 turns ingested in 0.32s locally; build is 4m 36s from cold |
| Maintainability | neutral | Layered Rust workspace with a passing 257-test suite, but a server plus panel to operate for what a local store does |
| Safety | + | Per-user isolation enforced with 403/401, secret redaction before storage; a BUSL licence limits team use |
| Cost Efficiency | neutral | Keyless L0 search costs nothing; useful recall needs an LLM for distillation |
| Verifiability | neutral | Stored turns are inspectable and counted through the API, but distilled facts depend on an LLM we could not check |

## Verdict

**discovery-log — tentative read** — keyless L0 search worked (12/12) and the isolation and redaction probes passed, but recall returns nothing without a distillation LLM, so the product's core value is unmeasured, and a naive baseline tied it on this fixture. Blocks a real read: an LLM endpoint for L1–L3, an embedding endpoint, and a head-to-head against `agentmemory` (rohitg00), which targets the same single-developer job under Apache-2.0 with no server to run. The BUSL-1.1 licence and the stale "no license" catalog note need a human look before any promotion.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AgentMemory (hsuanshao)](https://github.com/hsuanshao/AgentMemory) | tool | Self-hosted team memory service for AI agents (⚠️ no license; Rust) — layered L0→L3 memory, async LLM distillation, hybrid BM25+vector recall, department/team isolation | Agent-memory tools assume a single user; teams of agents working together have no shared, isolated, persistent memory service | agentmemory, friday, okf-agent-memory |
