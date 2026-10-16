# Evaluation: cognee

**Repo:** [topoteretes/cognee](https://github.com/topoteretes/cognee)
**Stars:** 29,784 | **Last updated:** 2026-08-04 | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Reflect / Retrospect
**Layer:** Infrastructure

---

## What it does

Open-source AI memory platform that builds a self-hosted knowledge graph from ingested data, giving agents persistent long-term memory across sessions. The core API is three operations — `remember` (ingest and graph-connect), `recall` (query with auto-routing between vector, graph, and hybrid search), and `forget` (delete). Under the hood, cognee combines vector embeddings, graph reasoning, and cognitive-science-grounded ontology generation to create a knowledge graph where documents are both searchable by meaning and connected by relationships that evolve.

The platform ships as a Python library (`pip install cognee`), CLI (`cognee-cli`), MCP server (`cognee-mcp` in the monorepo), Claude Code plugin (via separate `cognee-integrations` repo), and managed cloud service. The Claude Code plugin uses 6 lifecycle hooks (SessionStart, UserPromptSubmit, PostToolUse, Stop, PreCompact, SessionEnd) to automatically capture prompts, tool traces, and responses into session memory, inject relevant context on prompt submit, and sync to the permanent graph at session end.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed cognee 1.6.4 from PyPI into a clean Python 3.11 venv, ingested a five-document fixture with known facts through `cognee.add` and `cognee.cognify`, then asked five questions whose answers are fixed strings and scored cognee's `CHUNKS` retrieval against a keyword-grep baseline over the same files. No LLM key was set (`LLM_API_KEY` unset throughout).

```
python3 -m venv v && v/bin/pip install cognee     # rc=0, 1m43s, 170 packages in the venv
v/bin/pip install s3fs                            # needed: first cognee.add() raised ModuleNotFoundError: No module named 's3fs'
env -u LLM_API_KEY v/bin/python run1.py           # cognee.add 3.9s; cognee.cognify 83s wall (first run, includes local model fetch)
env -u LLM_API_KEY v/bin/python run2.py           # 5 questions x (grep top-2 files) vs (cognee CHUNKS top_k=2)
```

Fixture (`/tmp/eval-cognee/fx`, five one-or-two-sentence files): Alice Nguyen owns the billing service, which depends on the ledger-db Postgres cluster (d1); Bob Ortiz maintains ledger-db, which failed over on 2026-03-02 after a disk-full incident (d2); the checkout API calls billing and is owned by Carol Diaz (d3); Decision 14 chose Postgres over DynamoDB for ledger-db for transactional guarantees (d4); the mobile app uses the checkout API and Dev Patel leads mobile (d5).

Printed results (hit = every expected string appears in the returned text):

```
Q1 Who maintains the database that the billing service depends on?  expect "Bob Ortiz"              grep=False  cognee=False
Q2 Why did we choose Postgres for ledger-db?                          expect "transactional guarantees" grep=False  cognee=True
Q3 What happened on 2026-03-02?                                       expect "failed over"             grep=True   cognee=True
Q4 Who leads the mobile team?                                         expect "Dev Patel"               grep=True   cognee=True
Q5 Who owns the service that the mobile app uses?                     expect "Carol Diaz"              grep=False  cognee=True
RESULT grep 2/5  cognee-chunks 4/5
```

Under the hood the log reported the embedder as local (`FastembedEmbeddingEngine`, `BAAI/bge-small-en-v1.5`) and the graph as 37 nodes and 56 edges after `cognify`, built with no LLM call. `SearchType.SUMMARIES` returned 5 summary payloads in 0.1s.

## Test design

- **Task / corpus:** the five-file fixture above plus five questions with fixed expected strings; two questions need a hop across documents (Q1, Q5).
- **Baseline:** keyword grep, stop-words removed, files ranked by keyword hit count, top 2 files concatenated.
- **Treatment:** `cognee.search(query_type=SearchType.CHUNKS, top_k=2)` after `add` + `cognify` on a CPU-only sandbox with no LLM key.
- **Metric:** k/N questions where all expected strings appear in the returned text (mechanical oracle, Correctness protocol in `measurement-protocols.md`); wall-clock for add, cognify and search.
- **Reproduce:** recreate the five files from the description, run the commands above, score by substring match. N=5 is small and the fixture is tiny, so the 4/5 vs 2/5 gap is an indication, not a benchmark.

## What worked

- **Zero-key local path exists.** With no `LLM_API_KEY`, `add` and `cognify` completed and built a 37-node, 56-edge graph using a local embedder and a local extractor; retrieval then returned answers in about 0.1s per query after the first (4.6s, model load).
- **Beat keyword grep on this fixture.** 4/5 against 2/5; the semantic chunk search found the "why" question (Q2) and the indirect-ownership question (Q5), which share few keywords with their answer files.
- **Broad surface in one package.** The CLI exposes `add, search, cognify, memify, remember, recall, improve, forget, serve, eval, doctor` among others, and the Python API exposes the 1.0 `remember/recall/forget/improve` set alongside the V1 calls.

## What didn't work or surprised us

- **Clean install is incomplete.** After `pip install cognee`, the first `cognee.add()` raised `ModuleNotFoundError: No module named 's3fs'`, and `cognify()` failed with `CognifyFailedError` (status 422) for the same reason, after 96s. Installing `s3fs` by hand fixed it.
- **The headline graph-reasoning path needs an LLM key.** `GRAPH_COMPLETION` and `RAG_COMPLETION` both failed with `LLMAPIKeyNotSetError: LLM API key is not set`, and `TRIPLET_COMPLETION` failed with `NoDataError` until a `create_triplet_embeddings` memify pipeline is run. So the knowledge-graph answering that distinguishes cognee was not measured here.
- **The multi-hop question that motivates a graph still missed.** Q1 (billing → ledger-db → Bob Ortiz) failed for both arms with chunk retrieval alone.
- **Heavy for a first run.** 170 packages, a 1m43s install, 83s for the first `cognify` of five one-line files (including a local model fetch), and the log warns that session memory and multi-user access control are on by default.
- **Scope of the claim.** N=5 on a synthetic fixture; no Claude Code plugin hooks, MCP server or cloud path were exercised, and the published HotPotQA benchmark claims were not re-run.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | 4/5 vs 2/5 for keyword grep on a disclosed five-question fixture (chunk retrieval only; graph completion needs an LLM key) |
| Speed | neutral | ~0.1s per query after load, but 1m43s install and 83s first `cognify` on five tiny files |
| Maintainability | neutral | Explicit graph is queryable, but a missing `s3fs` dependency on a clean install is a packaging defect |
| Safety | neutral | Multi-user access control on by default per the startup log; no isolation test was run |
| Cost Efficiency | + | The measured path ran with no LLM key and no API spend; graph answering would add LLM cost |
| Verifiability | neutral | Retrieval returns raw chunks a human can check against source; graph-completion answers were not produced to check |

## Verdict

**discovery-log — tentative read** — cognee runs locally without a key and its chunk retrieval beat keyword grep 4/5 vs 2/5 on a five-question fixture, but the graph-completion path that is its differentiator needs an LLM key, the one multi-hop question missed, and a clean install needed a manual `s3fs` fix. A key-backed run of `GRAPH_COMPLETION` against claude-mem on a larger fixture is what a real verdict needs.

## Triage note

Cites claude-mem (STACK ADOPT) in Overlaps with, but the eval's own REVIEW already draws the line: cognee's knowledge-graph layer and published benchmarks are a differentiated job from claude-mem's zero-friction Claude Code memory, not a redundant re-implementation. ★29.8K, Apache-2.0, actively pushed. Left for a real hands-on eval rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cognee](https://github.com/topoteretes/cognee) | platform | Open-source AI memory with self-hosted knowledge graph engine for persistent agent memory | Need structured knowledge graph memory that agents can query across sessions | claude-mem, OMEGA, SimpleMem, OpenViking, MemOS, supermemory |
