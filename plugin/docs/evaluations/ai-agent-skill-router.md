# Evaluation: ai-agent-skill-router

**Repo:** [KRISH-exe-29/ai-agent-skill-router](https://github.com/KRISH-exe-29/ai-agent-skill-router)
**Stars:** 3 | **Last updated:** 2026-11-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An AI agent skill router and skill manager — auto-picks the right skills, subagents,
plugins, and MCP servers for a given task across Claude Code, Codex, Cursor, Gemini CLI,
Copilot, and Antigravity, and audits for duplicate or unused skills with cleanup/undo.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and its "Overlaps with" cell (`jump-skills`, `Only-Skill-You-Need`,
`skillranker`). That is sufficient to check for a named STACK redundancy; it is not
sufficient to support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — very new (created 2026-11-04) and tiny (3 stars).
None of its cited peers is a STACK pick. Its cross-harness scope (6 harnesses) plus a
duplicate/unused-skill audit distinguishes it from the single-harness routers it is
grouped with, enough to be worth a first look despite the low star count, rather than a
mechanical SKIP.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-agent-skill-router](https://github.com/KRISH-exe-29/ai-agent-skill-router) | tool | Skill/subagent/MCP/plugin router (Apache-2.0) auto-picking the right one per task, and auditing for duplicate or unused skills | Choosing the right skill, subagent, plugin, or MCP server per task across harnesses is manual, and duplicates or unused ones accumulate unnoticed | jump-skills, Only-Skill-You-Need, skillranker |
