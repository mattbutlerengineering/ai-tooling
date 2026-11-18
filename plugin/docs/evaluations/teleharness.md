# Evaluation: teleharness

**Repo:** [al3x4kov/teleharness](https://github.com/al3x4kov/teleharness)
**Stars:** 6 | **Last updated:** 2026-11-16 (pushed) | **License:** MIT
**Last verified:** 2026-11-18
**Last triaged:** 2026-11-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A self-hosted web UI for Claude Code and OpenCode that switches between the two AI coding CLIs
within the same chat, preserving conversation context through the handoff, and lets you continue
after hitting a usage limit. Mobile-first, with agent/MCP/skill/memory support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and repo metadata. Not sufficient to support an ADOPT, which this eval does not offer.

## Triage note

Newly discovered and catalogued today (daily discovery pass; 6 stars, brand new, no overlap
pressure against a STACK pick yet). `cli-continues`/`hermes` already solve cross-tool handoff via
CLI export/import across many more harnesses; teleharness's distinguishing claim is doing the
same inside one live, mobile-first web chat rather than a file handoff. Too early and too thin a
signal (6 stars) to call it a defensible SKIP against that cluster — left at `discovery-log` for
a later pass once it has more track record.
