# Evaluation: agents-council

**Repo:** [0xwilliamortiz/agents-council](https://github.com/0xwilliamortiz/agents-council)
**Stars:** 296 | **Last updated:** 2026-07-30 (pushed) | **License:** MIT
**Dev loop stage:** Review — fans one task across several vendors' CLIs for diverse perspectives
**Layer:** Plugin (Claude Code)
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A Claude Code plugin that orchestrates other vendors' agent CLIs — Codex CLI, Gemini CLI and others —
so one task collects several models' perspectives instead of a single vendor's.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and its "Overlaps with" cell. Enough to place and to band it; not enough for
any verdict, and none is offered.

## Triage note

Left at `discovery-log`. It belongs to the cross-model-review cluster with `codex-plugin-cc` (OpenAI
official, thin, one second opinion) and `claude-octopus` (heavy consensus engine, up to nine models)
— and **every member of that cluster is `discovery-log`**. With no incumbent decided, there is no
"redundant with X" to write, and picking a winner is a measured comparison rather than an
elimination. All three were left in this pass for that reason.

MIT, ★296, pushed 2026-07-30. The open question, common to the cluster, is whether the cross-model
payoff is real or asserted — nobody has benchmarked it, and it costs a second vendor's budget per
run.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents-council](https://github.com/0xwilliamortiz/agents-council) | plugin | Multi-agent collaboration plugin for Claude Code — orchestrates Codex CLI, Gemini CLI, etc. for diverse perspectives | Single-vendor agent sessions miss other models' perspectives; want one plugin to fan a task across multiple CLI agents | codex-plugin-cc, architect-loop, claude-octopus |
