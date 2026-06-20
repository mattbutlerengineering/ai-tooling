# Evaluation: Memory OS (Hermes Agent)

**Repo:** [ClaudioDrews/memory-os](https://github.com/ClaudioDrews/memory-os)
**Stars:** 1,170 | **Last updated:** 2026-06-10 (pushed; created 2026-05-31) | **License:** MIT | **Install:** one-command `setup.sh`
**Dev loop stage:** Memory & Context (memory infrastructure for a specific agent)
**Layer:** Infrastructure (local Docker + Qdrant + SQLite, as a Hermes Agent plugin)

---

## What it does

Memory OS is a **7-layer memory operating system for [Hermes Agent](https://github.com/NousResearch/hermes-agent)** — local memory infrastructure that gives Hermes persistent long-term memory. It provides automatic, intelligent context injection; **structured facts with trust scoring**; a **self-curating wiki pipeline**; and **semantic search across every conversation you've ever had**, backed by Qdrant + SQLite. It's **API-provider-agnostic** (OpenRouter, OpenAI, Anthropic, Ollama, or local models), runs **entirely on your machine**, and has no memory subscription / vendor lock-in. v0.2.0 added a one-command installer (`setup.sh`) that brings up the Docker services, databases, and the "Icarus" plugin.

## How we tested it

**Source-grounded inspection — not installed, not run.** No stack set up, no Hermes session run, no recall measured. Behavior comes from the README and metadata, not observed usage.

```bash
gh api repos/ClaudioDrews/memory-os --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 1.2K, MIT
gh api repos/ClaudioDrews/memory-os/readme --jq '.content' | base64 -d | head -15   # 7 layers, Qdrant, trust scoring, self-curating wiki, local
```

## What worked

- **Purpose-built for Hermes Agent.** It's the dedicated memory layer for a specific (and newly popular) own-it agent — tight integration rather than a generic bolt-on, which the catalog's Hermes Agent entry can pair with.
- **Trust-scored structured facts + self-curating wiki** is a more disciplined memory model than raw recall — it tries to keep memory accurate and organized, not just large.
- **Local-first, provider-agnostic, no subscription.** Qdrant + SQLite on your machine with any LLM provider is the right privacy/cost posture.
- **One-command install,** MIT, healthy fork ratio (~111 forks / 1.2K stars).

## What didn't work or surprised us

- **Tied to Hermes Agent.** Its value is conditional on using Hermes; it's not a general drop-in memory layer for Claude Code/Codex (those have their own options in this catalog).
- **Operational footprint.** Docker services + Qdrant + SQLite is more infrastructure to run than a single-binary or plugin memory tool.
- **Young (created late May 2026).** Promising but early; trust-scoring/self-curation efficacy is unverified here.
- **Overlaps the memory cluster conceptually** (MemOS, OMEGA) but is Hermes-scoped.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Trust-scored structured facts + self-curating wiki + semantic recall keep the right, accurate context available to Hermes. |
| Speed | + | Automatic context injection avoids re-explaining; "surgically token-efficient" per its pitch. |
| Maintainability | neutral / − | Disciplined memory model, but Docker + Qdrant + SQLite is a stack to run and maintain. |
| Safety | + | Runs entirely local, provider-agnostic — memory data stays on-box. |
| Cost Efficiency | + | No memory subscription; local infra; token-efficient context injection. |

## Verdict

**CONDITIONAL** — Memory OS is a thoughtfully-designed, MIT, **local-first 7-layer memory operating system specifically for Hermes Agent**: trust-scored structured facts, a self-curating wiki, and semantic search over all past conversations, on Qdrant + SQLite with any LLM provider and no subscription. Adopt it **if Hermes Agent is your agent** and you want disciplined, on-box long-term memory — it's the natural memory companion to the cataloged Hermes Agent. If you're on Claude Code/Codex, use this catalog's harness-native memory tools instead; Memory OS's value is its Hermes integration. Young, so pilot recall quality before depending on it.

Compared to neighbors: **MemOS** is a general self-evolving "memory OS"; **OMEGA** a cross-session memory MCP; **Hermes Agent** is the agent this serves. Memory OS's distinguishing pitch is being the **dedicated, local, trust-scored 7-layer memory layer for Hermes Agent**.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memory-os](https://github.com/ClaudioDrews/memory-os) | tool | Local-first 7-layer memory OS for Hermes Agent (MIT) — Qdrant + SQLite, trust-scored structured facts, self-curating wiki, semantic search over all conversations; provider-agnostic, no subscription | Hermes Agent forgets across sessions; want disciplined, on-box long-term memory with accuracy controls | MemOS, OMEGA, Hermes Agent |
