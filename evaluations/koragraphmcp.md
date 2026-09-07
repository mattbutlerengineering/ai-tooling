# Evaluation: KoragraphMCP

**Repo:** [Koragraph/KoragraphMCP](https://github.com/Koragraph/KoragraphMCP)
**Stars:** 11 | **Last updated:** 2026-09-07 (pushed) | **⚠️ no license**
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A local MCP memory server that anchors what broke, why, and what depended on what to the code itself, so context survives as the code moves — works with Claude Code, Cursor, and Codex.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. A fresh (created this week), tiny (11★) entrant into an already-crowded local project-memory-MCP space (mex, opencontext, delx-memory all do variations of persistent project context over MCP). No LICENSE file is recorded, which would block an eventual ADOPT/KEEP outright, but that is a question for a real eval, not a mechanical P3 stamp. Not clearly redundant enough with any single incumbent to name one as dominating; leaving it for a differentiated first look.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [KoragraphMCP](https://github.com/Koragraph/KoragraphMCP) | MCP server | Local memory layer (⚠️ no license) anchoring what broke, why, and what depended on what to your code as it moves | Tribal knowledge about past decisions and gotchas never makes it into docs and is lost across sessions | mex, opencontext, delx-memory |
