# Evaluation: ownmem

**Repo:** [grpcer/ownmem](https://github.com/grpcer/ownmem)
**Stars:** 81 | **Last updated:** 2026-08-19 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-21
**Last triaged:** 2026-08-21  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Local, git-native persistent memory for coding agents — one set of Markdown files, read/written deterministically (no vector DB, no embeddings), shared across Claude Code, Codex, Gemini CLI, Cursor, and Grok CLI.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the
triage note below, not for an ADOPT, and this eval offers none.

## Triage note

Cited as overlapping `claude-mem`, the STACK/ADOPT incumbent for Claude Code
memory. Left at discovery-log rather than SKIPped: ownmem's architecture is
genuinely different (deterministic Markdown files, no semantic search/knowledge
graph) and it is agent-agnostic where claude-mem is Claude-Code-specific —
matching this catalog's existing precedent of leaving other claude-mem-adjacent
memory tools (memU, agentmemory, beads, staffetta) undisposed rather than
mechanically SKIPping every memory tool against one incumbent.

_Triaged 2026-08-21 by the P2 challenger band._
