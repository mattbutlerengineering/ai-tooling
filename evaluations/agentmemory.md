# Evaluation: agentmemory

**Repo:** [rohitg00/agentmemory](https://github.com/rohitg00/agentmemory)
**Stars:** 26,556 | **Last updated:** 2026-08-03 | **License:** Apache-2.0
**Last verified:** 2026-10-17
**Last triaged:** 2026-10-17  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

MCP-based persistent memory engine for AI coding agents with hybrid retrieval (BM25 + vector + knowledge graph via RRF fusion). Built on the "iii engine," it runs as a local server on `:3111` and auto-captures session context through 12 hooks — no manual `memory.add()` calls needed. Exposes 53 MCP tools, ships 15 native skills (8 invocable, 7 reference), and connects to 15+ agent platforms via `agentmemory connect <agent>`. Extends Karpathy's LLM Wiki pattern with confidence scoring, lifecycle management, and compression that claims 92% token savings.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed `@agentmemory/agentmemory@0.9.30` from npm into a scratch directory (Node 22, Linux, `HOME` redirected so nothing touched a real profile), started the server with no LLM or embedding key, seeded it through its REST API and scored recall against a fixed planted-fact corpus, against a grep-style baseline over the same text.

```
npm install @agentmemory/agentmemory@0.9.30          # 30s
agentmemory demo --serve                              # boots engine + worker, seeds 3 sessions, "agentmemory is working"
agentmemory                                           # keyless server on :3111 (BM25 only)
python3 ingest.py && python3 ab.py                    # arm 1: keyless
npm install --ignore-scripts @huggingface/transformers
EMBEDDING_PROVIDER=local agentmemory                  # arm 2: on-device all-MiniLM-L6-v2
python3 ingest.py && python3 ab.py

arm                      query set   top-1  top-5   MRR   median latency
grep-style baseline      lexical     24/24  24/24    -    -
grep-style baseline      paraphrase   1/24   4/24    -    -
agentmemory keyless      lexical     22/24  24/24  0.958  93 ms
agentmemory keyless      paraphrase   4/24   8/24  0.226  96 ms
agentmemory local-embed  lexical     24/24  24/24  1.000  73 ms
agentmemory local-embed  paraphrase   9/24  22/24  0.579  25 ms
```

## Test design

- **Task/corpus:** 60 observations posted to `/agentmemory/observe` as `post_tool_use` events: 24 planted engineering facts (one per session, e.g. "chose jose over jsonwebtoken", "pgbouncer transaction mode", "argon2id memory cost 64MiB") plus 36 generic distractors ("ran prettier", "bumped version"). Each fact has two hand-written queries: a **lexical** one sharing its keywords and a **paraphrase** one sharing none of its content words ("database refused new clients when busy, what capacity change did we make"). Gold = the fact's own session id appears in the top-5 `smart-search` results.
- **Baseline:** grep-style keyword ranking over the same 60 texts (count of query tokens present, plus substring matches, stop-words dropped) - deliberately generous, since it is what an agent with `grep` over its own notes would get.
- **Metric:** top-1 and top-5 hit counts out of 24, MRR for agentmemory, median latency over 24 queries per set. Scored mechanically by `ab.py`; no model judgement involved.
- **Reproduce:** the corpus, ingest script and scorer live under `/tmp/eval-agentmemory/fx/` in the run sandbox (not committed); the corpus is fully described above and the install commands are in the block above.

## What worked

- **Installs and runs with no key.** `npx`-style install, the pinned `iii` engine auto-provisioned, `demo --serve` seeded and recalled in one command; the REST API is bearer-authenticated from a generated `~/.agentmemory/secret`.
- **Lexical recall is at parity with grep.** Keyless BM25 reached 24/24 top-5 on the keyword queries (22/24 top-1 vs grep's 24/24) - so it costs nothing on the easy case.
- **On-device embeddings are the real gain.** With `EMBEDDING_PROVIDER=local` the paraphrase set went from 4/24 (grep) and 8/24 (keyless) to **22/24 top-5**, with no API key and ~25 ms median query latency. This is exactly the capability a keyword search cannot supply.
- **Claims that held:** local embeddings are free and need no key, search is fast (tens of ms), and the BM25 fallback works without any provider.
- **Published benchmarks** (95.2% R@5 on LongMemEval-S, with an `eval/` harness) and 15+ agent integrations remain as documented in the README; broad platform support and 12 capture hooks are as advertised in `agentmemory --help`.

## What didn't work or surprised us

- **Keyless mode is weak on paraphrase.** 8/24 top-5 without embeddings - only marginally above grep - so the zero-config path under-delivers on the semantic recall the README leads with; the embedding step is effectively required.
- **Local embeddings need an undeclared extra install.** `EMBEDDING_PROVIDER=local` on a fresh install logged "Install @huggingface/transformers for local embeddings" for every observation and silently fell back to BM25 (identical scores to the keyless arm). The first `npm install @huggingface/transformers` hit an ECONNRESET in this sandbox; `--ignore-scripts` succeeded and the model then loaded.
- **Compact search results carry no text.** `smart-search` returns ids, scores and the tool name as `title` (`"Bash"`), so recall quality is judged by session id; the 92% token-savings claim was not measured here.
- **`project` filter did not isolate results**: the three demo sessions surfaced in fixture queries until deleted via the documented cleanup call.
- **Scale is small.** 60 observations, synthetic phrasing, one author writing both the facts and the paraphrases; results say nothing about a corpus of thousands of real tool outputs, nor about the 53-tool MCP surface, hook conflicts or the `iii` engine's opacity, which remain as in the earlier review.
- **Head-to-head with the incumbent is unmeasured.** claude-mem (ADOPT) was not run against the same corpus.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Paraphrase recall 22/24 top-5 with local embeddings vs 4/24 for grep on the same corpus; lexical recall at parity (24/24) |
| Speed | + | Median query latency 25-96 ms across arms; capture is automatic via hooks |
| Maintainability | neutral | Large surface (53 MCP tools, 12 hooks) on an opaque single-author engine; unchanged from the earlier review |
| Safety | neutral | Local-first, bearer-authenticated REST on loopback, no key needed; broad hook footprint still widens the attack surface |
| Cost Efficiency | + | Local embeddings and BM25 are free; the token-savings headline was not measured |
| Verifiability | neutral | Compact results are ids and scores only, so a human must expand a hit to confirm it; the viewer on :3113 helps but was not exercised |

## Verdict

**discovery-log — measured; promotion candidate** — on a disclosed 60-observation fixture, keyless it matches grep on keyword recall, and with free on-device embeddings it recovers 22/24 paraphrased facts in the top 5 against grep's 4/24; would read CONDITIONAL on human confirmation (adopt-if: you need semantic recall across sessions or agents and will install `@huggingface/transformers`), pending a head-to-head against claude-mem (ADOPT), which remains the simpler Claude Code-only choice.

## Triage note

Left at `discovery-log`, not SKIPped. Its evaluation already ran the comparison
against [`claude-mem`](https://github.com/thedotmack/claude-mem) (STACK, `ADOPT`/`MEASURED`) and
found a real split rather than a loss: agentmemory wins on published retrieval benchmarks and
15+ agent-platform reach, claude-mem wins on Claude Code ecosystem fit, simplicity (20 vs 53 MCP
tools), and battle-testing. A challenger that leads the incumbent on a named, measurable axis is
not redundant — it is unmeasured, which is a different problem and a different band.

Re-examined 2026-10-05 (5-oldest-untriaged pass): reasoning still holds, not newly dominated
by a STACK incumbent. Exercised hands-on 2026-10-17 (eval-runner pass); see Test design.

_Triaged 2026-08-04 by the P2 challenger band ([#264](https://github.com/mattbutlerengineering/ai-tooling/issues/264)); re-stamped 2026-10-05._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentmemory](https://github.com/rohitg00/agentmemory) | tool | Persistent memory for AI coding agents based on real-world benchmarks | Need memory that's been validated against actual dev workflows | OMEGA, beads, claude-mem |
