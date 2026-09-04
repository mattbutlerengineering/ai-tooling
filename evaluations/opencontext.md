# Evaluation: opencontext

**Repo:** [slxca/opencontext](https://github.com/slxca/opencontext)
**Stars:** 6 | **Last updated:** 2026-08-31 (pushed) | **License:** MIT
**Last verified:** 2026-08-31
**Last triaged:** 2026-08-31  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

A Model Context Protocol server giving coding agents persistent, project-specific context across sessions.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (thedotmack/claude-mem, STACK ADOPT — persistent memory with semantic search, timeline views, and knowledge-graph management, already installed for Claude Code). opencontext is a brand-new (created 2026-08-29), 6-star, minimal MCP server offering plain persistent project context with no semantic search, timeline, or knowledge graph — a thinner version of the same "context resets between sessions" job claude-mem already covers, with no stated differentiator beyond being MCP-native. This matches the same pattern as `Perenna` and `claude-db`: a brand-new, minimal memory server with no benchmark or capability gap over the incumbent earns nothing as a second tool.

_Triaged 2026-08-31 by the P2 challenger band._
