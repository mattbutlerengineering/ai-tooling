# Evaluation: Memori

**Repo:** [MemoriLabs/Memori](https://github.com/MemoriLabs/Memori)
**Stars:** 15,333 | **Last updated:** 2026-06-15 (pushed; created 2025-07-24) | **License:** Apache-2.0 (GitHub classifies as "Other"/NOASSERTION, but the LICENSE file is verbatim Apache 2.0) | **Releases:** 30
**Dev loop stage:** Memory & Context (cross-cutting — persistent memory layer for agents across sessions)
**Layer:** Infrastructure (LLM/datastore/framework-agnostic; TypeScript + Python SDKs; Memori Cloud or self-host)

---

## What it does

Memori is **"agent-native memory infrastructure"** — an LLM-agnostic layer that turns agent execution and conversation into **structured, persistent state for production systems**. Its tagline is the differentiator: **"memory from what agents *do*, not just what they say."** It's designed to plug into the software/infra you already use (LLM-, datastore-, and framework-agnostic) rather than being a framework you build inside.

Usage is unusually frictionless: you **register your existing LLM client** (e.g. OpenAI) with Memori and add **attribution** (`entity_id`, `process_id` — e.g. `user_123`, `support_agent`), and from then on conversations are **persisted and recalled automatically in the background**:

```typescript
const mem = new Memori().llm.register(client).attribution('user_123', 'support_agent');
// later calls automatically recall prior context (e.g. "favorite color is blue")
```

It ships **TypeScript and Python SDKs** (`@memorilabs/memori`, `pip install memori`). The quickstart is **cloud-first** — sign up at app.memorilabs.ai, set `MEMORI_API_KEY` + your LLM key — though the core is Apache-2.0. It publishes a benchmark page positioning itself on memory performance.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No SDK wired in, no memory store exercised. Claims (including benchmark positioning) come from the repository (GitHub metadata, README, license file, 30 releases) — the project's own documentation, not observed behavior. The license was verified by reading the LICENSE file directly.

```bash
gh api repos/MemoriLabs/Memori --jq '{stars,created_at,pushed_at,lang:.language}'
gh api repos/MemoriLabs/Memori/contents/LICENSE --jq '.content' | base64 -d | head   # confirms Apache-2.0
gh api repos/MemoriLabs/Memori/readme --jq '.content' | base64 -d   # register/attribution model, SDKs, cloud quickstart
```

## What worked

- **Register-and-go ergonomics.** Wrapping an existing LLM client and getting automatic background persist/recall with one `.register().attribution()` call is the lowest-friction memory integration in this group — no schema, no manual store/retrieve calls in the hot path.
- **"Memory from what agents do" is a meaningful framing.** Capturing execution/state, not just chat turns, and structuring it for *production* systems (multi-tenant attribution by entity/process) is more ops-oriented than chat-memory libraries.
- **Genuinely agnostic.** LLM-, datastore-, and framework-independent means it slots into an existing architecture rather than dictating one — easier to adopt incrementally.
- **First-class TS + Python SDKs** cover the two dominant agent ecosystems; attribution by `entity_id`/`process_id` is the right primitive for multi-user/multi-agent systems.
- **Apache-2.0, mature, popular.** ~15K stars, 30 releases, permissive license (despite GitHub's misclassification) — credible and adoptable.

## What didn't work or surprised us

- **Cloud-first quickstart vs. open-source core.** The documented happy path requires `MEMORI_API_KEY` (Memori Cloud); the Apache-2.0 repo is the SDK/core, but self-hosting the full backend is not the front-and-center story. Confirm the self-host path before assuming "open source = run it all yourself."
- **Saturated, fast-moving niche.** Competes directly with mem0, cognee, MemOS, and agentmemory — all high-star memory layers. Differentiation is the register-and-go ergonomics + execution-state framing, not a unique category.
- **Benchmarks are self-reported.** Its performance positioning is the vendor's; unverified here.
- **Automatic background recall is convenient but opaque.** Memory injected "automatically" is great until it recalls the wrong thing — controllability/observability of what gets recalled matters and isn't evaluated here.
- **A memory layer is a real dependency.** Putting Memori under production agents (especially via the cloud) is a meaningful coupling and a state/privacy surface to govern.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Automatic persist/recall reduces context loss across sessions; opaque auto-recall could also surface wrong context. |
| Speed | + | Register-and-go means little integration effort; background recall avoids manual retrieval plumbing. |
| Maintainability | + / neutral | Agnostic layer slots into existing architecture; but adds an external memory dependency to maintain. |
| Safety | neutral / − | Multi-tenant attribution is sound; cloud-first default sends conversation/state off-box — privacy surface to govern (self-host mitigates). |
| Cost Efficiency | neutral | Apache-2.0 core; Memori Cloud is the paid path; recall can trim re-explanation tokens. |

## Verdict

**CONDITIONAL** — adopt if you want the **lowest-friction "wrap your LLM client and get automatic memory"** integration for production agents, value multi-tenant attribution (entity/process), and are comfortable with a cloud-first default (or can confirm the self-host path). The register-and-go ergonomics and "memory from what agents do" framing are genuine strengths, the SDK coverage (TS + Python) is strong, and it's Apache-2.0 despite GitHub's misclassification. Caveats: it's one of several strong memory layers (compare mem0, cognee, MemOS by integration fit), the headline path leans on Memori Cloud, and auto-recall opacity + the external-dependency/privacy surface warrant a pilot. Measure recall quality on your own data before relying on it.

Compared to neighbors: **mem0** is the broad universal memory layer; **cognee** a self-hosted knowledge-graph memory; **MemOS** a self-evolving "memory OS" with policy/skill layers; **agentmemory** a benchmarked persistent store. Memori's distinguishing pitch is **register-your-client, automatic background memory with production multi-tenant attribution** — the most "drop-in for production systems" ergonomics of the set, with a cloud-first default to weigh.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Memori](https://github.com/MemoriLabs/Memori) | platform | Agent-native memory infrastructure (Apache-2.0) — register your LLM client for automatic background persist/recall with multi-tenant attribution (entity/process); LLM/datastore/framework-agnostic, TS + Python SDKs, cloud or self-host | Agents lose state across sessions; want drop-in persistent memory for production systems without manual store/retrieve plumbing | mem0, cognee, MemOS, agentmemory |
