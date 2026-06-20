# Evaluation: Acontext

**Repo:** [memodb-io/Acontext](https://github.com/memodb-io/Acontext)
**Stars:** ~3,500 | **Last updated:** 2026-06-16 | **License:** Apache-2.0
**Dev loop stage:** Reflect (Memory & Context)
**Layer:** Infrastructure

---

## What it does

A skill-as-memory layer for AI agents (from the Memobase team). Instead of storing memory as opaque embeddings, Acontext automatically captures learnings from agent runs and persists them as **editable Markdown skill files** — the same format as agent skills you'd download or write by hand.

Mechanically the store loop is: session messages → task complete/failed (by agent report or auto-detection) → an LLM **distillation** pass that infers what worked, what failed, and user preferences → a **Skill Agent** that decides where to write (an existing skill or a new one) according to a schema you define in `SKILL.md` → skills updated. Recall is deliberately *not* semantic top-k: the agent uses `get_skill` / `get_skill_file` tool calls and progressive disclosure to fetch what it needs by reasoning. Memory is plain Markdown — git/grep-able, mountable into a sandbox, framework-agnostic (LangGraph, Claude, AI SDK, anything that reads files), and exportable as a ZIP with no re-embedding or migration.

## How we tested it

Architecture review against the README, the store/recall flow diagrams, and the design philosophy. Confirmed the distillation→skill-agent→update pipeline, the `SKILL.md`-defined schema, the tool-use recall model (`get_skill`/`get_skill_file`), and the plain-file/no-embedding/ZIP-export properties. Not run against a live agent loop (requires wiring task-outcome signals and an LLM for distillation), so condition-gated.

```bash
gh api repos/memodb-io/Acontext --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/memodb-io/Acontext/readme --jq '.content' | base64 -d
```

## What worked

- **Inspectable, correctable memory.** Storing learnings as Markdown skill files means you can read, edit, diff, and share them — directly addressing the "opaque vector blob" failure mode of embedding memory.
- **Retrieval by reasoning, not similarity.** Progressive-disclosure tool calls (`get_skill`) avoid top-k noise and keep the context clean — conceptually aligned with how Claude Code skills already work.
- **No lock-in.** Plain files, ZIP export, framework-agnostic; portable across agents and LLMs with no migration step.

## What didn't work or surprised us

- **Needs task-outcome signals.** The learning trigger is "task complete/failed," so value depends on reliable outcome reporting or detection — weak signals mean weak distillation.
- **Crowded memory space.** Overlaps ACE, evolver, memU, pro-workflow, and letta-code; the differentiator is the skill-file representation, which is conceptually close to memU's "files as memory."
- **Distillation costs LLM calls.** Each learning pass spends tokens; quality of skills depends on the distillation prompt/model.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agents reuse distilled "what worked," reducing repeated mistakes |
| Speed | neutral | Recall is tool-use fetch; distillation adds background LLM work |
| Maintainability | + | Memory is human-readable Markdown — auditable and editable |
| Safety | + | No opaque memory polluting context; learnings are inspectable |
| Cost Efficiency | neutral | Free/OSS, but distillation passes consume tokens |

## Verdict

**CONDITIONAL**

Adopt for agents that run repeated tasks and benefit from compounding, inspectable learnings — especially in skill-file-native ecosystems (Claude Code, AI SDK). For a solo user already on claude-mem + OMEGA, it overlaps existing memory; the draw is the skill-file representation if you want portable, hand-editable learnings. Re-evaluate hands-on against memU and ACE for a memory-layer decision.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Acontext](https://github.com/memodb-io/Acontext) | tool | Skill-as-memory layer (Apache-2.0, ★3.5K) — auto-distills what worked/failed into editable Markdown skill files; recall by `get_skill` tool use and progressive disclosure, not top-k; ZIP-exportable, framework-agnostic | Opaque vector memory is hard to inspect, debug, or correct; want learnings as plain shareable skill files | ACE, evolver, memU, pro-workflow, letta-code |
