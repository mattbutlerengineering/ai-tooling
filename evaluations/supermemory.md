# Evaluation: supermemory

**Repo:** [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)
**Stars:** 28,780 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT | **Packages:** npm `supermemory`, PyPI `supermemory`
**Last verified:** 2026-10-25
**Last triaged:** 2026-10-25  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context (cross-cutting — persistent memory + context layer for AI apps and agents)
**Layer:** Infrastructure (memory/context engine + hosted app; cloud API or fully self-hostable)

---

## What it does

supermemory is a **memory and context engine for AI** that positions itself as state-of-the-art: it claims **#1 on LongMemEval, LoCoMo, and ConvoMem** — the three major AI-memory benchmarks. The pitch is that "your AI forgets everything between conversations" and supermemory fixes that by automatically learning from conversations, extracting facts, building user profiles, reconciling contradictions/temporal updates, forgetting expired information, and returning the right context at query time.

It's a **full context stack in one system**, not just a vector store:

- **Memory** — extracts facts from conversations; handles temporal change, contradictions, automatic forgetting.
- **User profiles** — auto-maintained stable-facts + recent-activity context, one call (~50ms claimed).
- **Hybrid search** — RAG knowledge-base docs and personalized memory in a single query.
- **Connectors** — Google Drive, Gmail, Notion, OneDrive, GitHub with real-time webhook sync.
- **Multi-modal extractors** — PDFs, image OCR, video transcription, AST-aware code chunking.

It ships TS + Python SDKs, a hosted dashboard/console, and a documented self-hosting path; MIT-licensed.

## How we tested it

**Evidence:** REVIEW

**Source-grounded review — not run hands-on.** The self-hosted engine (`npx supermemory local`, the `curl -fsSL https://supermemory.ai/install | bash` installer, or the Docker compose image) was not run: this unattended sandbox blocked executing the downloaded installer, and the other two routes fetch and run the same vendor binary or image (a second pass 2026-10-19 reached the installer through the npm CLI, `supermemory local install`, and it answered HTTP 403 from the sandbox proxy; Docker has no daemon here), so none was tried. The hosted cloud API needs a vendor key that the sandbox does not have. What was executed is only the PyPI client library, against a throwaway local HTTP stub on `127.0.0.1:6767` — that checks the SDK's request surface, not memory extraction, search quality or the vendor's benchmark claims, which remain the vendor's own.

```bash
python3 -m venv v && v/bin/pip install supermemory        # -> supermemory 5.0.0 (PyPI)
# stub server returns {} for every POST; client pointed at it via base_url
v/bin/python mock2.py
  no-key client: SupermemoryError The api_key client option must be set either by passing api_key to the client or by setting the SUPERMEMORY_API_KEY envi...
  add ok DocumentRef
  search ok SearchResponse
  profile ok ProfileResponse
  ('POST', '/ns/u1/document', 'Bearer sm_test', '{"content":"I prefer tabs over spaces"}')
  ('POST', '/ns/u1/search', 'Bearer sm_test', '{"query":"indent style"}')
  ('POST', '/ns/u1/profile', 'Bearer sm_test', '{}')
# the README's Python quickstart, verbatim, against the same stub
v/bin/python readme_snippet.py
  README add(): TypeError Supermemory.add() got an unexpected keyword argument 'container_tag'
  README profile(): TypeError Supermemory.profile() got an unexpected keyword argument 'container_tag'
# second pass 2026-10-19: npm CLI 5.0.2, same stub (SUPERMEMORY_API_URL / SUPERMEMORY_API_KEY set)
node_modules/.bin/supermemory local install
  Installing local Supermemory via https://supermemory.ai/install
  curl: (22) The requested URL returned error: 403
  Error: installer exited with code 22
node_modules/.bin/supermemory local status   -> {"installed": null, "reachable": false, "url": "http://localhost:6767"}
node_modules/.bin/supermemory add "I prefer tabs" --namespace u1 ; search "indent" ; profile
  stub log: GET /v3/session ; POST /ns/u1/document {"content":"I prefer tabs"} ; POST /ns/u1/search {"query":"indent"} ; POST /ns/u1/profile {}
v/bin/python rd.py   # README quickstart form, PyPI supermemory 5.0.0
  README add TypeError Supermemory.add() got an unexpected keyword argument 'container_tag'
  README profile TypeError Supermemory.profile() got an unexpected keyword argument 'container_tag'
# third pass 2026-10-25: re-check the installer route and the SDK release
curl -sSL https://supermemory.ai/install -o install.sh   # -> HTTP 200, 11155 bytes (readable, not executed)
  header: "downloads the matching binary from the supermemoryai/supermemory GitHub Releases, verifies sha256"
v/bin/pip index versions supermemory   # -> supermemory (5.0.0)   [same release as the earlier passes]
bash install.sh   # HOME=/tmp/eval-supermemory/home SUPERMEMORY_NO_START=1 SUPERMEMORY_NO_PROMPT=1
  -> refused by the sandbox's permission layer before it started; nothing installed
```

## Test design

- **Task/corpus:** the three client calls the README lists first (`add`, `search`, `profile`) plus the README's own Python quickstart snippet, run against a local stub that records each request.
- **Baseline:** none — no with/without arm; this is a surface check of the released SDK against its README.
- **Metric:** whether the documented call signature runs, and which HTTP path/auth header the SDK emits.
- **Reproduce:** `pip install supermemory==5.0.0`, start any HTTP server on port 6767 that answers POSTs with `{}`, point `Supermemory(api_key=..., base_url=...)` at it and call the snippet from README lines 224-234.

## What worked

- **Benchmark-leading positioning.** Claiming #1 on LongMemEval/LoCoMo/ConvoMem (the standard AI-memory benchmarks) is a stronger, more falsifiable differentiator than most memory libraries offer — even if self-reported.
- **Whole context stack, not just storage.** Fact extraction + user profiles + hybrid RAG + connectors + multimodal extractors in one ontology is broader than a key-value or pure-vector memory layer.
- **Real product surface.** TS + Python SDKs, hosted console, documented connectors and self-hosting — adoptable today, MIT-licensed.
- **Temporal/contradiction handling and automatic forgetting** target the failure modes (stale facts, conflicting updates) that naive memory stores ignore.

## What didn't work or surprised us

- **The README's Python quickstart does not run against the released SDK.** It passes `container_tag=` to `add()` and `profile()`; `supermemory` 5.0.0 on PyPI takes a positional `namespace` and raises `TypeError` on the README form. The SDK posts to `/ns/<namespace>/document|search|profile`, and `search` is a method taking `query=`, not the README's `client.search.documents()` table entry. A newcomer's first copy-paste fails.
- **The npm CLI (5.0.2) and the PyPI SDK (5.0.0) emit the same `/ns/<namespace>/document|search|profile` paths** against the stub, so the CLI surface is consistent with the SDK; the CLI also issues a `GET /v3/session` first. This is still a request-shape check only.
- **Third pass changed nothing on the engine.** The installer URL now answers HTTP 200 (it was a 403 on 2026-10-19), but the sandbox refused to execute the downloaded script, and PyPI still lists `supermemory` 5.0.0 as the latest release, so the README-vs-SDK mismatch above was not re-tested against a newer client.
- **The engine itself is unmeasured.** Extraction quality, recall, the ~50ms profile latency and the self-host footprint were not observed here.
- **Self-host still wants a model key for memory extraction** by the README's own account (OpenAI/Anthropic/Gemini/Groq or Ollama); only embeddings default to a local model.
- **Heavy and product-shaped for a solo dev loop.** The connectors (Gmail/Drive/Notion), profiles, and hosted console are aimed at app builders / "company brain" use cases — overkill for a single developer already running claude-mem + OMEGA for Claude Code session continuity.
- **Cloud-first happy path.** The quickstart leans on the hosted API/console; self-hosting the full engine is documented but is not the front-and-center story. Confirm the self-host scope before assuming "MIT = run it all yourself."
- **Benchmarks are self-reported.** The #1 claims are the vendor's; unverified here.
- **Saturated niche.** Competes head-on with mem0, cognee, MemOS, Memori, and memsearch — differentiation is breadth + benchmark posture, not a unique category.
- **A memory engine is a real dependency and data surface.** Sending conversation/profile/connector data through it (especially the cloud path) is a meaningful coupling and privacy surface to govern.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Fact extraction, contradiction/temporal handling, and right-context retrieval reduce stale or lost context across sessions. |
| Speed | + / neutral | One-call profiles (~50ms claimed) and hybrid single-query retrieval cut plumbing; integration of the full stack is non-trivial. |
| Maintainability | neutral / − | Broad engine slots in via SDKs, but adds a substantial external dependency (and connector surface) to maintain. |
| Safety | neutral / − | Cloud-first default and connectors (Gmail/Drive) send personal/conversation data off-box — privacy surface to govern (self-host mitigates). |
| Cost Efficiency | neutral | MIT core; hosted API is the paid path; good retrieval can trim re-explanation tokens. |
| Verifiability | neutral / − | Benchmark rank is self-reported, and the README's quickstart not matching the 5.0.0 SDK shows its examples are not kept in step with releases; a self-hosted run would let a reader check recall on their own data. |

## Verdict

**discovery-log — tentative read** — the engine could not be run here (installer execution refused by the sandbox on three passes, no vendor key); only the Python client was exercised, and the README's Python quickstart fails with `TypeError` on SDK 5.0.0. Prior read, unchanged by this pass: supermemory is one of the most capable memory+context engines in this catalog: a benchmark-leading (self-reported), full-stack system with fact extraction, user profiles, hybrid RAG, connectors, and multimodal ingestion, MIT-licensed with TS/Python SDKs. Adopt it when you're **building an AI app or a personal/company "brain"** that needs the whole context stack — not just session memory. For a solo developer whose goal is Claude Code continuity, it's heavier and largely redundant with claude-mem + OMEGA, and the headline path leans on the hosted cloud. Pilot on your own data, confirm the self-host scope, and measure recall quality before depending on it.

Compared to neighbors: **mem0** is the broad universal memory layer; **cognee** a self-hosted knowledge-graph memory; **MemOS** a self-evolving "memory OS" with policy/skill layers; **Memori** drop-in production memory with multi-tenant attribution; **memsearch** a Milvus-backed shared layer. supermemory's distinguishing pitch is **benchmark-topping breadth — memory + profiles + RAG + connectors + multimodal in one engine** — closer to a context platform than a memory library.

## Triage note

Cites claude-mem (STACK ADOPT) in Overlaps with, but the eval's own comparison already draws the line: this is a benchmark-topping cross-cutting context platform (memory + RAG + connectors + multimodal), not a redundant re-implementation of claude-mem's Claude Code-only auto-capture. ★28.8K, MIT, actively pushed. Left for a real hands-on eval rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [supermemory](https://github.com/supermemoryai/supermemory) | platform | Benchmark-leading memory + context engine (MIT) — auto fact extraction, user profiles, hybrid RAG+memory search, Gmail/Drive/Notion/GitHub connectors, and multimodal (PDF/OCR/video/code) ingestion; cloud API or self-hostable | AI forgets across conversations; want a full benchmark-topping context stack (memory + RAG + connectors + multimodal), not just key-value persistence | mem0, cognee, memsearch, claude-mem, OMEGA |
