# Evaluation: Perenna

**Repo:** [scarletkc/Perenna](https://github.com/scarletkc/Perenna)
**Stars:** 15 | **Last updated:** 2026-08-23 (pushed) | **License:** MIT
**Last verified:** 2026-08-23
**Last triaged:** 2026-08-23  <!-- triaged: bulk -->
**Dev loop stage:** Cross-cutting (Memory & Context)
**Layer:** Infrastructure

---

## What it does

A lightweight, Git-backed permanent memory for AI agents, self-hosted and exposed over MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-mem` (STACK ADOPT, persistent memory with semantic search, timeline views, and knowledge graph management) and `ownmem` (already covers the git-native memory niche this tool targets). Perenna is a brand-new (created 2026-08-21), 15-star, minimal git-backed memory MCP server with no benchmark or differentiator over either incumbent beyond "git-backed" — a property ownmem already has. No capability gap here justifies a second tool in an already-dense category.

_Triaged 2026-08-23 by the P2 challenger band (daily discovery routine)._
