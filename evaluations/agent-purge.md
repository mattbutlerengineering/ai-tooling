# Evaluation: agent-purge

**Repo:** [ZiChuanLan/agent-purge](https://github.com/ZiChuanLan/agent-purge)
**Stars:** 988 | **Last updated:** 2026-11-02 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local web console that replaces or injects system prompts/personas across eight-plus
coding-agent CLIs at once (Codex, Claude, opencode, Grok, OMP, Hermes, Pi, ZCode),
instead of hand-editing each tool's own config format.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient to
place the lead in a triage band; it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log` — newly catalogued today, no STACK-pick overlap (P3 backlog).
Cross-agent persona/system-prompt management is adjacent to `agent-harness`'s rule/skill
checkout but targets a different artifact (raw system prompt vs. rules/skills/hooks);
worth a first-time look, not examined further in this pass.

_Triaged 2026-11-02 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-purge](https://github.com/ZiChuanLan/agent-purge) | tool | Local web console (MIT) replacing or injecting system prompts across 8+ coding agents — Codex, Claude, opencode, Grok, OMP, Hermes, Pi, ZCode | Maintaining one persona or system prompt across many coding-agent CLIs means hand-editing each one's own config format | agent-harness, gentle-ai, superpowers |
