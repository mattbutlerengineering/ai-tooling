# Evaluation: unslop-design

**Repo:** [marcosnovo/unslop-design](https://github.com/marcosnovo/unslop-design)
**Stars:** 14 | **Last updated:** 2026-11-05 (pushed) | **License:** MIT
**Last verified:** 2026-11-05
**Last triaged:** 2026-11-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process (skill)

---

## What it does

An agent skill for Claude Code, Codex, Cursor, Copilot, and Gemini CLI that applies 64
numbered design fixes to make an app or site stop looking AI-generated, and scores the
UI from 0 to 100 before and after so the fix is measured rather than asserted.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The claimed 0-100 scoring (e.g. its own README
example of 26 → 100) is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Overlaps a cluster
already covered in depth (`ui-ux-pro-max`, `impeccable`, `taste-skill`), none of which
is a STACK pick; its distinguishing claim is the scored before/after, which the
incumbents don't carry. Not examined further in this pass.

_Triaged 2026-11-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [unslop-design](https://github.com/marcosnovo/unslop-design) | skill | Agent skill (MIT) with 64 numbered design fixes and a 0-100 UI-slop scorer, for Claude Code, Codex, Cursor, Copilot, and Gemini CLI | AI-built UIs look AI-generated with no scored before/after proving the fix actually worked | ui-ux-pro-max, impeccable, taste-skill |
