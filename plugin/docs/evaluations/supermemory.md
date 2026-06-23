# Evaluation: supermemory

**Repo:** [supermemoryai/supermemory](https://github.com/supermemoryai/supermemory)
**Stars:** 27,206 | **Last updated:** 2026-06-19 (pushed) | **License:** MIT | **Packages:** npm `supermemory`, PyPI `supermemory`
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

**Source-grounded inspection — not installed, not run.** No SDK wired in, no memory store exercised, no benchmark reproduced. Claims (including the #1 benchmark positioning and the ~50ms profile latency) come from the repository's own README and metadata, not observed behavior.

```bash
gh api repos/supermemoryai/supermemory --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 27.2K, MIT
gh api repos/supermemoryai/supermemory/readme --jq '.content' | base64 -d | head -60   # engine scope, benchmarks, connectors, multimodal
```

## What worked

- **Benchmark-leading positioning.** Claiming #1 on LongMemEval/LoCoMo/ConvoMem (the standard AI-memory benchmarks) is a stronger, more falsifiable differentiator than most memory libraries offer — even if self-reported.
- **Whole context stack, not just storage.** Fact extraction + user profiles + hybrid RAG + connectors + multimodal extractors in one ontology is broader than a key-value or pure-vector memory layer.
- **Real product surface.** TS + Python SDKs, hosted console, documented connectors and self-hosting — adoptable today, MIT-licensed.
- **Temporal/contradiction handling and automatic forgetting** target the failure modes (stale facts, conflicting updates) that naive memory stores ignore.

## What didn't work or surprised us

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

## Verdict

**CONDITIONAL** — supermemory is one of the most capable memory+context engines in this catalog: a benchmark-leading (self-reported), full-stack system with fact extraction, user profiles, hybrid RAG, connectors, and multimodal ingestion, MIT-licensed with TS/Python SDKs. Adopt it when you're **building an AI app or a personal/company "brain"** that needs the whole context stack — not just session memory. For a solo developer whose goal is Claude Code continuity, it's heavier and largely redundant with claude-mem + OMEGA, and the headline path leans on the hosted cloud. Pilot on your own data, confirm the self-host scope, and measure recall quality before depending on it.

Compared to neighbors: **mem0** is the broad universal memory layer; **cognee** a self-hosted knowledge-graph memory; **MemOS** a self-evolving "memory OS" with policy/skill layers; **Memori** drop-in production memory with multi-tenant attribution; **memsearch** a Milvus-backed shared layer. supermemory's distinguishing pitch is **benchmark-topping breadth — memory + profiles + RAG + connectors + multimodal in one engine** — closer to a context platform than a memory library.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [supermemory](https://github.com/supermemoryai/supermemory) | platform | Benchmark-leading memory + context engine (MIT) — auto fact extraction, user profiles, hybrid RAG+memory search, Gmail/Drive/Notion/GitHub connectors, and multimodal (PDF/OCR/video/code) ingestion; cloud API or self-hostable | AI forgets across conversations; want a full benchmark-topping context stack (memory + RAG + connectors + multimodal), not just key-value persistence | mem0, cognee, memsearch, claude-mem, OMEGA |
