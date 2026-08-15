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

## Verdict

**SKIP** — the repo and its author account (`0xwilliamortiz`) are both gone (404 via the GitHub
API) as of 2026-08-15, caught by the link-rot sweep after detector C moved onto authenticated
`gh api` (#498). Nothing left to install or evaluate, and no successor is evident. It belonged to
the cross-model-review cluster with `codex-plugin-cc` and `claude-octopus`, both still
`discovery-log` — this SKIP is about this repo's own disappearance, not a redundancy call against
either of them.

_Triaged 2026-08-15 after the account/repo was found gone during a repo audit._

## Triage note (superseded)

Previously left at `discovery-log` (triaged 2026-08-04): it belonged to the cross-model-review
cluster with `codex-plugin-cc` (OpenAI official, thin, one second opinion) and `claude-octopus`
(heavy consensus engine, up to nine models) — and every member of that cluster was
`discovery-log`, so there was no "redundant with X" to write. Moot now that the repo is gone.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agents-council](https://github.com/0xwilliamortiz/agents-council) | plugin | Multi-agent collaboration plugin for Claude Code — orchestrates Codex CLI, Gemini CLI, etc. for diverse perspectives | Single-vendor agent sessions miss other models' perspectives; want one plugin to fan a task across multiple CLI agents | codex-plugin-cc, architect-loop, claude-octopus |
