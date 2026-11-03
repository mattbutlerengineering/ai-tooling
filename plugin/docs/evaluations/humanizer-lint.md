# Evaluation: humanizer-lint

**Repo:** [yanstd888/humanizer-lint](https://github.com/yanstd888/humanizer-lint)
**Stars:** 65 | **Last updated:** 2026-11-02 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Ship (prose artifacts — docs, commit messages, UI text); touches Review when the artifact under review is prose or code comments
**Layer:** Process

---

## What it does

A local, zero-dependency linter — explicitly "a style checker, not an AI detector" —
that flags stiff, AI-sounding prose, copywriting, UI text, and code comments (stock
phrases, flat sentence rhythm, repeated wording) and tells you what to revise. Ships
with 8 language packs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether its heuristics actually distinguish
AI-sounding prose from merely plain prose, across 8 languages, is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [humanizer-lint](https://github.com/yanstd888/humanizer-lint) | tool | Local linter (MIT) flagging stiff, AI-sounding prose, UI text, and code comments, in 8 languages | AI-written prose and code comments read as obviously machine-generated with no local, zero-dependency check to flag it | humanizer, stop-slop, sepia |
