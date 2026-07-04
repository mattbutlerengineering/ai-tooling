# Evaluation: MemOS (Memory Operating System)

**Repo:** [MemTensor/MemOS](https://github.com/MemTensor/MemOS)
**Stars:** 9,928 | **Last updated:** 2026-06-18 (pushed; created 2025-07-06) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Memory & Context (cross-cutting — persistent memory layer for agents across sessions)
**Layer:** Infrastructure (TypeScript; cloud service or self-hosted; npm `@memtensor/memos`, plugins)

---

## What it does

MemOS is a **"memory operating system" for LLMs and AI agents** — a persistent, self-evolving memory layer that sits under your agent and provides ultra-persistent memory, hybrid retrieval, and **cross-task skill reuse**. Its v2.0 ("Stardust") headline is a layered, self-evolving architecture: **L1 trace** (what happened), **L2 policy** (how to act), **L3 world model**, plus **crystallized Skills** distilled from feedback — i.e. it doesn't just store conversation, it turns repeated experience into reusable policy/skills.

It's offered as a **cloud service or self-hosted**, with concrete integrations: a `memos-local-plugin` (local-first memory core for Hermes Agent and OpenClaw) and an OpenClaw Cloud plugin with multi-agent memory sharing by `user_id`. It publishes aggressive, research-style benchmark claims: **+43.70% accuracy vs. OpenAI Memory**, **35.24% memory-token savings** (72% via the cloud plugin), and scores on standard long-term-memory evals (LoCoMo 75.80, LongMemEval +40.43%, PrefEval, PersonaMem +40.75%). Docker deployment is supported (with a `MEMOS_HOME` config note).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No memory store deployed, no agent wired in. Claims — including all benchmark numbers — come from the repository (GitHub metadata, README, linked docs) and are the project's own; **not independently reproduced here**.

```bash
gh api repos/MemTensor/MemOS --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/MemTensor/MemOS/readme --jq '.content' | base64 -d   # L1/L2/L3 + Skills, plugins, benchmark claims
```

## What worked

- **Memory-as-policy/skills is a real conceptual step up.** Most memory layers store facts/conversation; MemOS's L1-trace → L2-policy → L3-world-model + crystallized Skills explicitly converts *experience* into *reusable behavior*. That's the "compounding improvement" the catalog's outer-loop thesis is about, applied to memory.
- **Cross-task skill reuse + token savings** target two real pains at once: agents re-learning the same thing every session, and context bloat. The claimed 35–72% token reduction, if it holds, is materially valuable.
- **Self-host or cloud, Apache-2.0.** Clean permissive license and a self-hostable core (Docker) — you can keep memory on your own infra, unlike cloud-only memory products.
- **Benchmark-forward and research-backed.** Standard long-term-memory evals (LoCoMo/LongMemEval/PersonaMem) and a clear comparison to OpenAI Memory show the team is measuring, not just asserting.
- **Concrete agent integrations** (Hermes Agent, OpenClaw) rather than a bare library.

## What didn't work or surprised us

- **All performance claims are self-reported.** "+43.70% vs OpenAI Memory," "35.24% token savings," and the eval scores are the project's own numbers, unverified here; treat as indicative, and the comparison baseline/setup matters.
- **Saturated, fast-moving niche.** It competes head-on with mem0, cognee, agentmemory, and Memori — all high-star memory layers. Differentiation is the self-evolving L1/L2/L3 + Skills framing, not a unique capability category.
- **Operational + lock-in considerations.** A "memory OS" under your agents is a significant dependency; the most convenient path (cloud, dashboards) is the commercial surface, and self-hosting carries real ops (datastore, config, Docker `MEMOS_HOME`).
- **Integration scope is uneven.** First-class plugins exist for Hermes Agent / OpenClaw; using it under Claude Code / other agents is possible (it's a layer) but less turnkey than the marketed paths.
- **Complexity risk.** A layered self-evolving memory with policy/world-model/skills is powerful but a lot of moving parts to reason about and debug when memory goes wrong.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Persistent policy/world-model + skill reuse should reduce repeated mistakes and context loss across sessions (claimed accuracy gains unverified). |
| Speed | + / neutral | Cross-task skill reuse avoids re-deriving solutions; retrieval adds a lookup step. |
| Maintainability | neutral | Affects agent memory, not your codebase structure. |
| Safety | neutral / − | Self-host keeps memory on your infra (+); a persistent self-evolving store of agent behavior is a new state surface to govern (−). |
| Cost Efficiency | + | Claimed 35–72% token savings via memory reuse; Apache-2.0 self-host avoids per-call fees (cloud tier is paid). |

## Verdict

**CONDITIONAL** — adopt if you need a serious, persistent memory layer for agents and are drawn to the **self-evolving policy/skills** model (not just fact storage), want self-host + Apache-2.0, and run (or can integrate with) its supported agents. The L1/L2/L3 + crystallized-Skills architecture is genuinely more ambitious than a vector-store memory, and the token-savings + accuracy claims target real pain. Caveats: all benchmarks are self-reported and unverified; it's one of several strong memory layers (compare mem0, cognee, Memori) so pick by integration fit and how much the skill-reuse model matters; and a "memory OS" is a meaningful dependency to take on. Pilot and measure against your own workload before committing.

Compared to neighbors: **mem0** is the broad "universal memory layer"; **cognee** an open-source memory platform; **agentmemory** a persistent store. MemOS's distinguishing pitch is **self-evolving, layered memory (trace→policy→world-model) with crystallized skill reuse and published long-term-memory benchmarks** — the most "turns experience into behavior" framing of the group, at the cost of more moving parts and unverified claims.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MemOS](https://github.com/MemTensor/MemOS) | platform | Self-evolving "memory OS" for agents — layered L1-trace/L2-policy/L3-world-model + crystallized Skills, hybrid retrieval, cross-task skill reuse, cloud or self-hosted (claims 35%+ token savings) | Agents re-learn the same things every session and bloat context; want persistent memory that turns experience into reusable policy/skills | mem0, cognee, agentmemory |
