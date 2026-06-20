# Evaluation: claude-obsidian

**Repo:** [AgriciDaniel/claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian)
**Stars:** 7,151 | **Last updated:** 2026-05-28 (pushed; created 2026-04-07) | **License:** MIT | **Latest:** v1.9.2
**Dev loop stage:** Memory & Context (persistent knowledge base for Claude Code)
**Layer:** Skill pack / plugin (15 Claude Code skills over an Obsidian vault)

---

## What it does

claude-obsidian is a **self-organizing AI second brain for Obsidian + Claude Code** — "a running AI notetaker that builds and maintains a persistent, compounding wiki vault. Every source you add gets integrated; every question pulls from everything that has been read." It packages **15 Claude Code skills** plus multi-agent support and is explicitly based on **Andrej Karpathy's LLM Wiki pattern**.

Recent versions are substantive:
- **v1.7 "Compound Vault"** — Obsidian CLI transport, **hybrid retrieval** (contextual prefix + BM25 + cosine rerank, per Anthropic's contextual-retrieval research), and **per-file advisory locking** to close a multi-writer corruption hole.
- **v1.8** — first-class methodology modes (LYT / PARA / Zettelkasten / Generic).
- **v1.9** — a 10-principle thinking framework + audit hardening.

It's MIT; there's also a "Pro" community mirror offering earliest access to in-development features (same MIT core).

## How we tested it

**Source-grounded inspection — not installed, not run.** No vault built, no skills run, no retrieval measured. Behavior comes from the README/release notes and metadata, not observed usage.

```bash
gh api repos/AgriciDaniel/claude-obsidian --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 7.2K, MIT
gh api repos/AgriciDaniel/claude-obsidian/readme --jq '.content' | base64 -d | head -25   # second-brain, 15 skills, hybrid retrieval, methodology modes
```

## What worked

- **Compounding knowledge base is the right idea.** Integrating every source into a maintained wiki and answering from the whole vault ("knowledge compounds like interest") is a strong memory model, and grounding it in Karpathy's LLM Wiki pattern is credible.
- **Serious retrieval engineering.** Hybrid retrieval (contextual prefix + BM25 + cosine rerank) following Anthropic's contextual-retrieval research is well beyond naive embedding lookup.
- **Multi-writer safety.** Per-file advisory locking closing a corruption hole shows production-minded maturity (v1.7+).
- **Human-inspectable + portable.** It lives in a plain Obsidian vault with PKM methodology modes (LYT/PARA/Zettelkasten) — auditable, editable, not a black box. MIT, ~7.2K stars.

## What didn't work or surprised us

- **Obsidian-coupled.** It's built around an Obsidian vault and CLI; great if Obsidian is your PKM, otherwise a bigger commitment than a harness-native memory plugin.
- **Overlaps the catalog's Obsidian/memory tools.** It's the full-tool counterpart to the cataloged claude-code-memory-setup recipe (also Obsidian + Karpathy wiki), and competes with claude-mem/storybloq — same compounding-memory space.
- **Commercial adjacency.** A "Pro" community/mirror org alongside the MIT repo is fine but worth noting; install from the official MIT repo.
- **Maintenance/curation burden.** A self-organizing vault still needs vault hygiene, and retrieval quality depends on how well sources are integrated.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Answers grounded in an integrated, compounding wiki with strong hybrid retrieval reduce lost/forgotten context. |
| Speed | + | Pulling from a maintained vault beats re-reading sources each session. |
| Maintainability | + / neutral | Human-readable Obsidian notes + methodology modes are auditable; the vault needs upkeep. |
| Safety | + | Local vault + per-file locking (multi-writer safe); data stays on-box. |
| Cost Efficiency | + | Hybrid retrieval over a vault avoids re-ingesting sources; compounding reuse. |

## Verdict

**CONDITIONAL** — claude-obsidian is a mature (v1.9.x), MIT **self-organizing second brain for Obsidian + Claude Code**: 15 skills, a compounding wiki, genuinely strong hybrid retrieval (contextual prefix + BM25 + rerank), PKM methodology modes, and multi-writer safety. Adopt it if Obsidian is (or could be) your knowledge base and you want human-inspectable, compounding persistent memory grounded in Karpathy's LLM Wiki pattern. It overlaps the cataloged claude-code-memory-setup recipe (this is the full tool to that how-to) and claude-mem — pick by whether you want an Obsidian-centric compounding vault vs. a turnkey harness plugin. Install from the official MIT repo.

Compared to neighbors: **claude-code-memory-setup** is the Obsidian+Graphify setup *recipe*; **claude-mem** a turnkey memory plugin; **storybloq** tracks `.story/` context. claude-obsidian's distinguishing pitch is a **mature, retrieval-engineered, self-organizing Obsidian second brain** with PKM methodology modes.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-obsidian](https://github.com/AgriciDaniel/claude-obsidian) | plugin | Self-organizing AI second brain for Obsidian + Claude Code (MIT) — 15 skills build a compounding wiki vault with hybrid retrieval (contextual prefix + BM25 + rerank), PKM methodology modes (LYT/PARA/Zettelkasten), multi-writer safe; based on Karpathy's LLM Wiki | Want human-inspectable, compounding persistent knowledge that integrates every source and answers from the whole vault | claude-code-memory-setup, claude-mem, storybloq |
