# Evaluation: loci

**Repo:** [cmoraes10/loci](https://github.com/cmoraes10/loci)
**Stars:** 20 | **Last updated:** 2026-10-01 (pushed) | **License:** MIT
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

Typed long-term memory for AI agents: one core library plus an MCP server adapter and a Hermes
plugin adapter. Eight memory categories with importance tiers and lifecycle management; extracts
facts from conversations via both LLM analysis and regex patterns, then injects relevant memories
back into context. The MCP adapter is manually invoked, the Hermes adapter extracts automatically.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. Cites `claude-mem` (STACK, ADOPT/MEASURED) in "Overlaps with", which
bands this P2, but the two aren't a clean substitution: `claude-mem` is a Claude-Code-specific
plugin built around semantic search and timeline views, while `loci` is cross-harness by design
(a standalone core plus separate MCP-server and Hermes-plugin adapters) and organizes memory into
typed categories with importance tiers and explicit lifecycle management rather than a single
semantic index. One day old (20 stars) with no adoption signal yet, but the typed/lifecycle design
and cross-harness adapters are different enough from `claude-mem`'s approach to deserve a real
look rather than a mechanical SKIP.

_Triaged 2026-10-01 by the P2 challenger band (today's new lead)._
