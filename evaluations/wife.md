# Evaluation: wife

**Repo:** [ma-nucho-pro/wife](https://github.com/ma-nucho-pro/wife)
**Stars:** 45 | **Last updated:** 2026-08-05 (pushed) | **License:** MIT
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Local, persistent, auditable memory layer (hooks-based, zero-dependency) for Claude Code, Codex, Cursor, and Gemini CLI — the agent remembers project context and preferences across sessions without a hosted service.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`: the Memory & Context category already has a dozen-plus
uninstalled leads (OMEGA, claude-mem, agentmemory, mem0, MemOS, cognee, …) and none
of them is a settled ADOPT/KEEP incumbent that wife would be cleanly redundant with —
the category itself is still an open P0 question, not something a bulk pass can
resolve by SKIPping newcomers. wife's differentiator (cross-tool: Claude Code, Codex,
Cursor, Gemini CLI in one memory layer) is real enough to deserve a first-time eval
rather than a mechanical SKIP.

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [wife](https://github.com/ma-nucho-pro/wife) | tool | Local, persistent, auditable memory layer (MIT) for Claude Code, Codex, Cursor & Gemini CLI — hooks-based, zero-dependency, local-first | Coding agents forget project context and preferences every session; want a cross-tool memory layer that doesn't phone home | OMEGA, claude-mem, agentmemory, memory-os |
