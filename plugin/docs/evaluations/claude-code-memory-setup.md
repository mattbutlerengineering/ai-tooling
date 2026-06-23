# Evaluation: claude-code-memory-setup

**Repo:** [lucasrosati/claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup)
**Stars:** 785 | **Last updated:** 2026-06-01 (pushed; created 2026-04-12) | **License:** MIT
**Dev loop stage:** Memory & Context (a *setup recipe*, not an installable tool)
**Layer:** Reference (guide wiring existing tools together)

---

## What it does

claude-code-memory-setup is **a documented setup recipe** — "The Definitive Guide to Token Savings & Persistent Memory" — that turns Claude Code into an agent with long-term memory and codebase awareness by **wiring together existing tools** rather than shipping a new one. The stack:

- **Obsidian as persistent memory** — a Zettelkasten vault for durable, linked notes across sessions.
- **A chat-import pipeline** — pulls past conversations into the vault.
- **Graphify (codebase knowledge graph)** — structural awareness so the agent queries the graph instead of re-reading files.

It claims **71.5× fewer tokens per session** plus permanent cross-session memory, with a complete workflow, real-results section, and troubleshooting.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not built, not run.** No vault set up, no pipeline run, no token savings measured. The "71.5×" figure and "permanent memory" claims are the author's, reported here and unverified. Note that **Graphify**, a core component, is itself already cataloged.

```bash
gh api repos/lucasrosati/claude-code-memory-setup --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 785, MIT
gh api repos/lucasrosati/claude-code-memory-setup/readme --jq '.content' | base64 -d | head -20   # Obsidian + import pipeline + Graphify recipe
```

## What worked

- **Composition over yet-another-tool.** It assembles Obsidian + a chat-import pipeline + Graphify into one coherent workflow — useful precisely because it shows *how the pieces fit*, not just that they exist.
- **Obsidian-Zettelkasten as memory is a real, human-inspectable approach.** Durable linked notes you can read and edit are a different (and auditable) posture from opaque vector stores.
- **Addresses both axes at once** — persistent memory *and* token savings (via graph queries instead of file re-reads).
- **MIT, well-documented** (workflow + troubleshooting + real-results sections), decent traction (~785 stars).

## What didn't work or surprised us

- **It's a guide, not a tool.** There's no single install; you stand up Obsidian, the import pipeline, and Graphify and maintain them. Value depends on your willingness to run that stack.
- **Self-reported, eye-catching metric.** "71.5× fewer tokens" is a specific claim from one setup; unverified and workload-dependent.
- **Overlaps the catalog's memory tools.** It competes conceptually with claude-mem, storybloq, and context-infrastructure — but as a recipe layered on Graphify, not a turnkey product.
- **Maintenance burden.** A multi-component memory pipeline (vault hygiene, import freshness, graph sync) is more to keep running than a single plugin.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Codebase graph + persistent notes give the agent durable context, reducing lost-context errors. |
| Speed | + | Querying the graph instead of re-reading files cuts context-gathering effort (claimed 71.5× token savings). |
| Maintainability | neutral / − | Human-readable Obsidian notes are auditable; but a 3-component pipeline is more to maintain. |
| Safety | neutral | Local vault keeps memory on-box; no notable new risk. |
| Cost Efficiency | + | Token savings via graph-first retrieval is the core pitch (self-reported magnitude). |

## Verdict

**CONDITIONAL (reference / setup recipe)** — a well-documented, MIT recipe for **persistent Claude Code memory + token savings** by composing **Obsidian Zettelkasten + a chat-import pipeline + Graphify**. Its value is the integration blueprint: if you want human-inspectable, file-based memory plus a codebase graph and are willing to run/maintain the stack, it's a credible alternative to a turnkey memory plugin. Treat the "71.5×" headline as one setup's self-reported result, and weigh the multi-component maintenance against a single plugin like claude-mem. Best read as a *how-to* that leans on the already-cataloged Graphify, not a drop-in product.

Compared to neighbors: **claude-mem** is a turnkey memory plugin; **storybloq** tracks cross-session context in `.story/`; **Graphify** is the codebase-graph component this recipe builds on. claude-code-memory-setup's distinguishing pitch is the **Obsidian-Zettelkasten + Graphify integration blueprint** for memory *and* token savings.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-memory-setup](https://github.com/lucasrosati/claude-code-memory-setup) | reference | Setup recipe (MIT) wiring Obsidian Zettelkasten + a chat-import pipeline + Graphify for persistent Claude Code memory and token savings (claims 71.5× fewer tokens; self-reported) | Want human-inspectable persistent memory + a codebase graph without re-reading files, assembled from existing tools | claude-mem, graphify, storybloq |
