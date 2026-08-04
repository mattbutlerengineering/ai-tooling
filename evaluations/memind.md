# Evaluation: Memind

**Repo:** [openmemind/memind](https://github.com/openmemind/memind)
**Stars:** 902 | **Last updated:** 2026-06-14 (pushed; created 2026-03-19) | **License:** Apache-2.0 | **Language:** Java
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
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

**SKIP** — wrong ecosystem, and covered where it counts. The distinguishing pitch in the read above is
that it is **JVM-native**, and the same paragraph names the alternative for everyone else: *"for
Python/TS shops, cognee/supermemory/MemPalace cover similar ground."*

This catalog's stack is Python and TypeScript; a Java-native memory service is a runtime dependency
with no reason to exist in it. And the crowded field is exactly why the ecosystem fit decides it —
Memory & Context is one of the largest categories here, `cognee`, `supermemory`, `mem0` and `MemOS`
are all P0 leads, and adding a fifth memory layer that additionally requires a JVM clears no bar.

The idea worth remembering is experience reuse — turning resolved tasks and tool calls into Insight
Trees rather than storing transcripts — which is the same bet `ACE`, `evolver` and `hivemind` make in
other forms. That bet is being tracked; this implementation of it is not the one to track it through.

The SOTA claims on LoCoMo/LongMemEval/PersonaMem are vendor-reported and unverified here, so they
carry no weight in either direction.

Re-open for a JVM-stack project.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memind](https://github.com/openmemind/memind) | platform | Self-evolving cognitive memory + context engine in Java (Apache-2.0) — turns conversations/tool-calls/tasks into reusable experience (memory graphs, threads, Insight Trees), recalled via REST/MCP/SDKs; claims SOTA on LoCoMo/LongMemEval/PersonaMem | Want a JVM-native agent memory layer that builds reusable experience, not just conversation recall | cognee, MemOS, supermemory, MemPalace |
