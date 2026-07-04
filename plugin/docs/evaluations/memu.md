# Evaluation: memU

**Repo:** [NevaMind-AI/memU](https://github.com/NevaMind-AI/memU)
**Stars:** 13,890 | **Last updated:** 2026-06-19 (pushed) | **License:** see repo (no SPDX detected) | **Language:** Python
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Memory & Context — file-structured agent memory
**Layer:** Infrastructure (memory framework/service)

---

## What it does

memU is **a "memory file system" for AI agents** — "File System as Memory, Memory Shapes the Agent." Instead of flattening everything an agent learns into one giant prompt or an opaque vector blob, memU organizes memory the way you organize a computer: **a navigable tree of human-readable Markdown files.** Core files: **`MEMORY.md`** (the living memory — who the user is, preferences, goals, events extracted from every source), **`SKILL.md`** (learned skills and tool patterns — what worked, what to avoid, how to repeat recurring tasks), and **`INDEX.md`** (a table-of-contents/map across every memory file, so the agent knows where to look before reading). The agent **`memorize()`s** new sources into these files and **`retrieve()`s** only the relevant sections on demand.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No memory ingested, no retrieval exercised.

```bash
gh api repos/NevaMind-AI/memU --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 13890, NOASSERTION, pushed 2026-06-19
gh api repos/NevaMind-AI/memU/readme --jq '.content' | base64 -d | head -40               # MEMORY.md/SKILL.md/INDEX.md, memorize()/retrieve()
```

## What worked

- **Human-readable, navigable memory.** The Markdown-tree model (MEMORY/SKILL/INDEX) is inspectable and auditable in a way vector blobs aren't — you can open the files and see exactly what the agent "knows," which is a real trust/debuggability win. (It mirrors the file-based memory pattern good agent setups converge on.)
- **INDEX-before-read retrieval.** Consulting a map/table-of-contents before reading sections is a sensible, token-frugal retrieval strategy — load only what matters, not the whole store.
- **Skills as memory.** Capturing learned tool patterns in `SKILL.md` (what worked / what to avoid) blends memory with experience reuse, more useful than pure conversation recall.
- **Very strong traction.** 13.9K stars; actively pushed; multilingual docs.
- **Clean API.** `memorize()` / `retrieve()` is a legible interface.

## What didn't work or surprised us

- **License undeclared (NOASSERTION).** No standard SPDX detected — confirm terms before non-personal/commercial use.
- **Crowded, and overlaps the user's existing stack.** Memory is the most saturated catalog category (cognee, MemOS, supermemory, memind, claude-mem, MemPalace). The Markdown-FS model also closely resembles patterns already in use (e.g. OMEGA's `MEMORY.md`/file-based memory, Letta's MemFS) — differentiation is the specific FS structure, not a new category.
- **Markdown FS has scaling questions.** Human-readable files are great for inspection; at very large scale, retrieval quality vs. embedding-based stores (and INDEX maintenance) is the open question, unverified here.
- **Writeback governance.** An agent that `memorize()`s from "every source" needs care about what it promotes into MEMORY.md — an auditability surface (mitigated by the files being readable).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Persistent, structured profile/events/skills keep relevant context available across sessions. |
| Speed | + | INDEX-guided retrieval loads only relevant sections, avoiding whole-store reads. |
| Maintainability | + | Human-readable Markdown memory is inspectable and editable — no opaque blob. |
| Safety | neutral | Readable files aid auditing; what gets memorized from "every source" needs governance. |
| Cost Efficiency | + | Retrieve-only-relevant-sections avoids stuffing the whole memory into context. |

## Verdict

**CONDITIONAL** — memU is a popular, well-conceived **file-structured memory framework** whose strength is making agent memory a **human-readable, navigable Markdown tree** (MEMORY/SKILL/INDEX) with INDEX-guided, retrieve-only-what-matters access — inspectable and auditable where vector stores are opaque. Adopt it if you want transparent, file-based agent memory (and like the skills-as-memory angle) and can confirm the (currently undeclared) license. It's CONDITIONAL because memory is heavily saturated, the Markdown-FS model overlaps patterns you may already run (OMEGA-style file memory, Letta MemFS), and large-scale retrieval quality vs. embeddings is unproven here. Strong fit for "I want to read my agent's memory"; less differentiated if you already have a file-based memory system.

Compared to neighbors: **cognee** is knowledge-graph memory; **MemOS**/**memind** crystallize experience into policy; **supermemory** is a benchmark-forward context engine; **claude-mem** is Claude-Code-native recall. memU's distinguishing pitch is **memory as a navigable, human-readable Markdown file system (MEMORY/SKILL/INDEX) with memorize()/retrieve().**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memU](https://github.com/NevaMind-AI/memU) | platform | "File system as memory" for agents (★13.9K) — organizes memory as a navigable tree of human-readable Markdown (MEMORY.md profile/events, SKILL.md learned patterns, INDEX.md map); the agent `memorize()`s sources and `retrieve()`s only the relevant sections | Flattening agent memory into one giant prompt or an opaque vector blob is unnavigable; want inspectable, file-structured memory | cognee, MemOS, supermemory, memind, claude-mem |
