# Evaluation: dsh-context-bridge

**Repo:** [GibouLJB/dsh-context-bridge](https://github.com/GibouLJB/dsh-context-bridge)
**Stars:** 4 | **Last updated:** 2026-11-15 (pushed) | **License:** none specified
**Last verified:** 2026-11-20
**Last triaged:** 2026-11-20  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A DeepSeek Harness plugin that imports ChatGPT and Claude Code conversations into
local project workspaces and generates handoff summaries.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell. That is
sufficient to place the lead against its closest catalog peers, not to support any
verdict, and none is offered here.

## Triage note

Newly catalogued from today's discovery pass. No STACK overlap or archived status
bands this lead for a mechanical disposition, but it carries no declared license
(⚠️ no LICENSE file, no README/manifest grant found at cataloguing time) — this is
a vendored `plugin` Type, so a future triage pass should re-check for a license
declaration and, absent one, apply the P4 mechanical-skip disposition rather than
leaving it indefinitely. Left at `discovery-log` for now since this pass found no
declared license to act on yet, not because the license question is settled.

_Triaged 2026-11-20 by the daily discovery-and-triage routine (bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dsh-context-bridge](https://github.com/GibouLJB/dsh-context-bridge) | plugin | DeepSeek Harness plugin (⚠️ no license) importing ChatGPT and Claude Code conversations into local project workspaces with handoff summaries | Conversations with ChatGPT or Claude Code live outside the project and are lost switching tools or starting a new session; want them imported with a handoff summary | ctx-handoff-mod, project-sentinel, claude-rein |
