# Evaluation: deslop-GPT

**Repo:** [MrZoyo/deslop-GPT](https://github.com/MrZoyo/deslop-GPT)
**Stars:** 32 | **Last updated:** 2026-08-27 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A deletion-first Agent Skill for removing test bloat, verification theater, and speculative fallbacks from an agent's own output, while preserving behavior.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`HERO-Anti-OverDefense`, `unlazy`, `ratchet`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. The catalog already carries several anti-overbuild skills (`HERO-Anti-OverDefense`, `stop-that-shit`, `unlazy`, `pristine-skill`) covering similar ground from slightly different angles; whether this one's specific deletion-first framing is differentiated enough to earn a seat, or is redundant with that cluster, needs a real comparison.

_Triaged 2026-08-30 by the P3 backlog band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deslop-GPT](https://github.com/MrZoyo/deslop-GPT) | skill | Deletion-first Agent Skill (MIT) removing test bloat, verification theater, and speculative fallbacks while preserving behavior | Agents accrete defensive scaffolding and fake verification that never gets deleted | HERO-Anti-OverDefense, unlazy, ratchet |
