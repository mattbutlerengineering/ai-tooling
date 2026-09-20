# Evaluation: jolo

**Repo:** [jolo-build/jolo](https://github.com/jolo-build/jolo)
**Stars:** 30 | **Last updated:** 2026-09-13 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Coding workspace for AI agents — a desktop app, a terminal CLI, and shared tasks in one place.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-10), catalogued from today's discovery scan.

## Triage note

P3 backlog (no STACK overlap flagged). Distinguishable from `agent-launcher` (launches existing CLIs) and `agentic-stack-desktop` (shared knowledge graph) by the "shared tasks" coordination angle across a desktop app and a terminal CLI. Left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [jolo](https://github.com/jolo-build/jolo) | tool | Coding workspace for AI agents (MIT) — desktop app, terminal CLI, and shared tasks in one place | Coordinating AI-agent work across a desktop app and terminal means separate tools with no shared task state | agentic-stack-desktop, agent-launcher, ai-terminal-manager |  |
