# Evaluation: MemOS (Memory Operating System)

**Repo:** [MemTensor/MemOS](https://github.com/MemTensor/MemOS)
**Stars:** 10,591 | **Last updated:** 2026-08-05 (pushed; created 2025-07-06) | **License:** Apache-2.0
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context (cross-cutting — persistent memory layer for agents across sessions)
**Layer:** Infrastructure (TypeScript; cloud service or self-hosted; npm `@memtensor/memos`, plugins)

---

## What it does

MemOS is a **"memory operating system" for LLMs and AI agents** — a persistent, self-evolving memory layer that sits under your agent and provides ultra-persistent memory, hybrid retrieval, and **cross-task skill reuse**. Its v2.0 ("Stardust") headline is a layered, self-evolving architecture: **L1 trace** (what happened), **L2 policy** (how to act), **L3 world model**, plus **crystallized Skills** distilled from feedback — i.e. it doesn't just store conversation, it turns repeated experience into reusable policy/skills.

It's offered as a **cloud service or self-hosted**, with concrete integrations: a `memos-local-plugin` (local-first memory core for Hermes Agent and OpenClaw) and an OpenClaw Cloud plugin with multi-agent memory sharing by `user_id`. It publishes aggressive, research-style benchmark claims: **+43.70% accuracy vs. OpenAI Memory**, **35.24% memory-token savings** (72% via the cloud plugin), and scores on standard long-term-memory evals (LoCoMo 75.80, LongMemEval +40.43%, PrefEval, PersonaMem +40.75%). Docker deployment is supported (with a `MEMOS_HOME` config note).

## How we tested it

**Evidence:** RUN

**Hands-on** — installed it via `pip install MemoryOS` (v2.0.33, the PyPI package for `MemTensor/MemOS`) into a fresh venv under `/tmp/eval-memos/`, cloned the repo at `HEAD`, and ran the project's own pytest suite against that install in two arms, then drove its Qdrant vector-DB wrapper directly. Everything below is keyless: no LLM, no cloud account.

```bash
python3 -m venv v && v/bin/pip install MemoryOS pytest pytest-asyncio pytest-mock
cd src && ../v/bin/python -m pytest tests -q --continue-on-collection-errors -p no:cacheprovider
# arm A (bare install):
45 failed, 795 passed, 9 skipped, 27 errors in 17.87s
v/bin/pip install "MemoryOS[tree-mem,mem-scheduler,mem-reader]" qdrant-client
# arm B (documented extras, no torch):
4 failed, 861 passed, 9 skipped, 2 errors in 21.09s

# functional: MemOS Qdrant wrapper, local on-disk mode, 5 docs, hashing embedder (no model)
a -> a 0.707 | b -> b 0.655 | c -> c 0.577 | d -> d 0.655 | e -> e 0.775
top1 5 / 5   ms/query 0.5
```

## Test design

- **Task/corpus:** the repo's own `tests/` tree at `HEAD` (`a7367d0`, 876 test outcomes) run against the PyPI 2.0.33 install; plus a 5-document / 5-query retrieval fixture (`/tmp/eval-memos/func.py`, bag-of-words hashing embedder, 64 dims) pushed through `memos.vec_dbs` with the `qdrant` backend.
- **Baseline:** arm A, the bare `pip install MemoryOS` core, against arm B with the extras the README and `pyproject.toml` document for tree memory, scheduler and reader. This isolates whether the failures are packaging gaps or defects.
- **Metric:** pytest pass / fail / error counts; top-1 retrieval hits out of 5; mean ms per query.
- **Reproduce:** the commands in the block above; the functional fixture builds `VectorDBConfigFactory(backend="qdrant", ...)` and calls `add` then `search(top_k=1)`.

## What worked

- **The suite is green once the documented extras are installed.** Arm A to arm B moved 795 to 861 passing and 72 failures-or-errors down to 6. Every one of the 66 recovered cases was a missing optional module (`qdrant_client`, `neo4j`, `langchain_text_splitters`, `chonkie`, scheduler deps), not a logic defect.
- **Install is light.** The core wheel pulls no torch and no vector or graph database; the heavy pieces are opt-in extras, so a trial costs seconds.
- **The vector-DB layer works locally with no service.** Qdrant local mode stored and retrieved 5 of 5 planted documents at top-1, about 0.5 ms per query. That exercises the storage and retrieval plumbing only; the embedder was a hashing stand-in written for this test.
- **Self-host and Apache-2.0** hold up from the repo itself (`LICENSE`, `pyproject.toml`).

## What didn't work or surprised us

- **The headline function was not exercised.** Extracting memories from conversations, the L1/L2/L3 policy and world-model layers, crystallized Skills, and the README benchmark numbers (+43.70% vs OpenAI Memory, 35.24% token savings, LoCoMo 75.80) all need an LLM endpoint and, for tree memory, a Neo4j server. No key or service was available, so none of those claims are confirmed or contradicted here; they remain the project's own.
- **A bare `pip install MemoryOS` is not enough to run its own tests**: 72 of 876 outcomes red until extras are added, and the install emits a warning that `langchain_text_splitters` is missing and a simple-splitter fallback is used.
- **Six cases stay red without PyTorch** (`DynamicCache` in `tests/memories/activation/test_item.py`, `test_kv.py`, `test_hf.py`, one scheduler test). The torch-dependent KV-cache activation memory was left uninstalled to keep the run small, so those six are an environment gap, not a verdict on that feature.
- **Config surface is large.** Importing the package logs missing `NACOS_SERVER_ADDR` / `AK` / `SK` / `DATA_ID` warnings before any use, a sign of a platform with many optional backends to wire.
- Saturated niche: competes with mem0, cognee and agentmemory, which already carry their own evals here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Own suite 861 passed with extras and the vector layer retrieved 5/5; the accuracy claims for memory extraction are unverified without an LLM. |
| Speed | neutral | Local Qdrant search ran at ~0.5 ms/query on 5 vectors; no end-to-end agent latency was measured. |
| Maintainability | neutral | Affects agent memory, not your codebase structure; optional extras keep the core dependency set small. |
| Safety | neutral / − | Self-host keeps memory on your infra; a persistent, self-evolving store of agent behavior is a new state surface to govern. |
| Cost Efficiency | neutral | Claimed 35-72% token savings are self-reported and untested here; Apache-2.0 self-host avoids per-call fees but needs an LLM key and datastores. |
| Verifiability | neutral | A real test suite (876 test outcomes) gives a checkable baseline, but the claims that matter are benchmark scores a reader cannot reproduce without paid model access. |

## Verdict

**discovery-log — tentative read** — it installs and its own tests pass cleanly once the documented extras are added (861 passed; the 6 remaining reds all need PyTorch), and the local vector layer retrieved 5/5, but the self-evolving memory pipeline and the benchmark claims need an LLM key and Neo4j and were not exercised, so there is no basis for a real verdict. Compare against mem0, cognee and agentmemory by integration fit and pilot on your own workload with a key before committing.

Compared to neighbors: **mem0** is the broad "universal memory layer"; **cognee** an open-source memory platform; **agentmemory** a persistent store. MemOS's distinguishing pitch is self-evolving, layered memory (trace to policy to world-model) with crystallized skill reuse, which is exactly the part this keyless run could not reach.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MemOS](https://github.com/MemTensor/MemOS) | platform | Self-evolving "memory OS" for agents — layered L1-trace/L2-policy/L3-world-model + crystallized Skills, hybrid retrieval, cross-task skill reuse, cloud or self-hosted (claims 35%+ token savings) | Agents re-learn the same things every session and bloat context; want persistent memory that turns experience into reusable policy/skills | mem0, cognee, agentmemory |
