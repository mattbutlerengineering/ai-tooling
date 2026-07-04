# Evaluation: Memind

**Repo:** [openmemind/memind](https://github.com/openmemind/memind)
**Stars:** 902 | **Last updated:** 2026-06-14 (pushed; created 2026-03-19) | **License:** Apache-2.0 | **Language:** Java
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Memory & Context (memory + context engine)
**Layer:** Infrastructure (Java service; REST + MCP + SDKs + agent plugins)

---

## What it does

Memind is a **self-evolving cognitive memory and context engine for AI agents, written in Java.** It turns raw context — conversations, tool calls, documents, resolved tasks — into **structured memory and reusable experience**, continuously organizing it into **memory graphs, threads, and evolving "Insight Trees,"** then recalling the right context through **REST, MCP, SDKs, and first-party plugins** for popular agents. It claims **state-of-the-art results across all three mainstream long-memory benchmarks — LoCoMo, LongMemEval, and PersonaMem.**

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No service deployed, no memory ingested, benchmarks not reproduced. The SOTA claims are the project's own, reported here and unverified.

```bash
gh api repos/openmemind/memind --jq '{stars,license:.license.spdx_id,lang:.language,pushed:.pushed_at}'   # 902, Apache-2.0, Java
gh api repos/openmemind/memind/readme --jq '.content' | base64 -d | head -20   # memory graphs/threads/Insight Trees, REST/MCP/SDK, benchmark claims
```

## What worked

- **"Reusable experience," not just recall.** Turning tool calls and resolved tasks into structured, reusable experience (Insight Trees, threads) is a more ambitious model than conversation memory — closer to learning than remembering.
- **Strong access surface.** REST + MCP + SDKs + first-party agent plugins means it can slot into many stacks (MCP makes it directly usable from agents).
- **Benchmark-forward.** Claiming SOTA across LoCoMo + LongMemEval + PersonaMem is falsifiable positioning (still vendor-reported).
- **Java + Apache-2.0** fills an ecosystem gap — most memory layers are Python/TS; a JVM-native option suits Java shops.

## What didn't work or surprised us

- **Self-reported SOTA.** "State-of-the-art across all three benchmarks" is unverified here; memory benchmarks are also sensitive to setup.
- **Heavy crowded niche.** It competes directly with cognee, MemOS, supermemory, and MemPalace — differentiation is the Insight-Tree experience model + JVM-native, not a new category.
- **Service to run.** A Java memory engine is infrastructure (deploy, secure, maintain) versus a single-binary or plugin.
- **Self-evolving memory is opaque.** Continuously reorganizing memory graphs is powerful but a controllability/auditability surface — what it promotes into "insights" matters and isn't evaluated here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Structured memory + reusable experience + strong claimed recall keep accurate context available. |
| Speed | + / neutral | MCP/REST recall avoids re-explaining; running a JVM service adds deployment overhead. |
| Maintainability | neutral / − | Broad access surface (REST/MCP/SDK) is flexible; a self-evolving Java service is real infra to maintain. |
| Safety | neutral | Self-hostable (good); self-evolving memory promotion is an auditability surface to govern. |
| Cost Efficiency | neutral | Apache-2.0 core; infra cost to run; experience reuse can save re-derivation. |

## Verdict

**CONDITIONAL** — Memind is an Apache-2.0, **JVM-native self-evolving memory + context engine** whose distinctive idea is turning tool calls and resolved tasks into **reusable experience** (memory graphs, threads, Insight Trees), exposed over REST/MCP/SDKs with claimed SOTA on LoCoMo/LongMemEval/PersonaMem. Adopt it if you want an agent memory layer in a **Java** stack or value the experience-reuse model over plain recall, and are willing to run/govern a self-evolving service. Treat the SOTA claims as vendor-reported and pilot on your own data; for Python/TS shops, cognee/supermemory/MemPalace cover similar ground. The self-evolving promotion logic warrants observability before you trust what it surfaces.

Compared to neighbors: **cognee** is a knowledge-graph memory; **MemOS** a self-evolving memory OS; **supermemory**/**MemPalace** benchmark-forward memory engines. Memind's distinguishing pitch is **JVM-native, experience-reuse memory (Insight Trees) with REST/MCP/SDK access**.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memind](https://github.com/openmemind/memind) | platform | Self-evolving cognitive memory + context engine in Java (Apache-2.0) — turns conversations/tool-calls/tasks into reusable experience (memory graphs, threads, Insight Trees), recalled via REST/MCP/SDKs; claims SOTA on LoCoMo/LongMemEval/PersonaMem | Want a JVM-native agent memory layer that builds reusable experience, not just conversation recall | cognee, MemOS, supermemory, MemPalace |
