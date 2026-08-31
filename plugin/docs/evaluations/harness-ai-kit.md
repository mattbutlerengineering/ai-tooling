# Evaluation: harness-ai-kit

**Repo:** [seed-forge/harness-ai-kit](https://github.com/seed-forge/harness-ai-kit)
**Stars:** 19 | **Last updated:** 2026-08-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-28
**Last triaged:** 2026-08-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A package manager and composition layer for AI agent assets: installs, resolves, locks, validates, and synchronizes skills, CLIs, MCP servers, plugins, hooks, subagents, and loops across Codex, Claude Code, Cursor, Kiro, and DeepSeek Harness, with the project manifest as source of truth. Ships 42 skills, 5 CLIs, 1 plugin; on PyPI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata, README, plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition below, which turns on catalog placement and redundancy questions, not on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Triage note

Cites `vercel-labs/skills` and `openskills` — both `discovery-log` leads, not STACK picks — so this lands in the P3 backlog band. Left at `discovery-log`: the manifest+lockfile reproducibility angle goes further than `npx skills`' installer (composition, validation, cross-harness sync), but ★19 is too early to promote on a README read.

_Triaged 2026-08-28 by the P3 backlog band._
