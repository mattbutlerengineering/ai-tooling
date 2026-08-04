# Evaluation: obsidian-second-brain

**Repo:** [eugeniughelbur/obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain)
**Stars:** ~2,570 | **Last updated:** 2026-06-17 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04
**Dev loop stage:** Reflect (knowledge management / Memory & Context)
**Layer:** Process / Tooling

---

## What it does

A cross-CLI skill (Claude Code, Codex, Gemini, OpenCode) that turns an Obsidian vault into a **self-rewriting AI second brain** — an evolution of Karpathy's LLM-Wiki pattern: "a vault that rewrites itself."

The defining mechanic: every new source **updates existing pages** instead of just appending new ones, and contradictions **reconcile automatically** — so the vault compounds and stays coherent rather than accumulating redundant, conflicting notes. It ships 45 commands, auto-synthesis, "thinking tools that argue with you," live research from X/web/YouTube, 4 scheduled agents, 4 role presets, a write-time AI-first validator, a `/create-command` interview flow, and a multilingual trigger schema. There's also a `/obsidian-architect` to document your codebase into the vault.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and feature list (self-rewriting/reconciling vault, 45 commands, scheduled agents, live research, write-time validator, codebase documentation). Confirmed the "update-not-append + auto-reconcile" mechanic that distinguishes it from append-only note systems, and the cross-CLI compatibility. Not installed/run live, so condition-gated.

```bash
gh api repos/eugeniughelbur/obsidian-second-brain --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/eugeniughelbur/obsidian-second-brain/readme --jq '.content' | base64 -d
```

## What worked

- **Update-and-reconcile, not append.** Rewriting existing pages and auto-reconciling contradictions is the key improvement over append-only memory/notes — it fights knowledge rot directly.
- **Plain Markdown in Obsidian.** Memory lives in an inspectable, user-owned Obsidian vault, not an opaque store — auditable and portable.
- **Rich, cross-CLI feature set.** 45 commands, scheduled agents, live research, and codebase documentation across Claude Code/Codex/Gemini/OpenCode make it a substantial knowledge system.

## What didn't work or surprised us

- **Auto-rewriting is double-edged.** A vault that rewrites itself can also overwrite or "reconcile" away things you wanted kept — trust requires reviewing its edits (Obsidian's version history helps).
- **Obsidian-bound + setup.** Value assumes you live in Obsidian; the broad feature set (scheduled agents, presets) takes setup.
- **Overlaps memU/claude-mem/karpathy-llm-wiki.** Several file-based memory systems exist; this one's edge is the self-reconciling Obsidian vault.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Auto-reconciling contradictions keeps the knowledge base coherent |
| Speed | + | Auto-synthesis + scheduled agents compound knowledge unattended |
| Maintainability | + | Plain Markdown in Obsidian; update-not-append curbs note sprawl |
| Safety | - | Self-rewriting can overwrite wanted content — review its edits |
| Cost Efficiency | neutral | OSS; scheduled agents + live research consume tokens |

## Verdict

**discovery-log — tentative read**

Adopt if you live in Obsidian and want an AI second brain that compounds and reconciles itself (update-not-append) rather than an append-only note pile — the self-rewriting mechanic is its standout. Review its edits (lean on Obsidian version history) since auto-rewriting can remove wanted content. For a solo user already on claude-mem + OMEGA it overlaps existing memory; the draw is the coherent, user-owned Obsidian vault.

## Triage note

Left at `discovery-log`, not SKIPped. Its eval notes that for a solo
user already on claude-mem this overlaps existing memory — but its draw is stated in the same
breath: a coherent, **user-owned Obsidian vault** that reconciles itself (update-not-append) rather
than accumulating an append-only note pile. That is a knowledge-base question, not an agent-memory
one, and no STACK pick answers it.

Relevant here specifically: an Obsidian vault is already part of this operator's setup. The eval's
own caution stands — review its edits, since auto-rewriting can remove wanted content.

_Triaged 2026-08-04 by the P2 challenger band ([#264](https://github.com/mattbutlerengineering/ai-tooling/issues/264))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [obsidian-second-brain](https://github.com/eugeniughelbur/obsidian-second-brain) | skill | Self-rewriting Obsidian vault as an AI second brain (MIT, ★2.6K) — cross-CLI skill evolving Karpathy's LLM-Wiki pattern: every source updates existing pages (not just appends), contradictions auto-reconcile; 45 commands, scheduled agents, live research, write-time validator | Append-only notes/memory rot and contradict; want a vault that compounds, reconciles, and rewrites itself into a navigable second brain | memU, claude-mem, supermemory, karpathy-llm-wiki |
