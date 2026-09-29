# Evaluation: jevmem

**Repo:** [Avinash-jetwani/jevmem](https://github.com/Avinash-jetwani/jevmem)
**Stars:** 98 | **Last updated:** 2026-09-29 (pushed) | **License:** MIT
**Last verified:** 2026-09-29
**Last triaged:** 2026-09-29  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Automatic project memory for Claude Code, distributed as an npm package with a CLI, MCP server, and Claude Code plugin/hooks; also works with Cursor and Codex.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a bulk-triage disposition, not for an ADOPT/KEEP call — this eval offers none.

## Triage note

Cites claude-mem (STACK ADOPT) in Overlaps with, which bands this P2 challenger. Not SKIPped as redundant: jevmem's stated differentiator is cross-harness reach (Cursor and Codex, not just Claude Code), the same class of differentiation already kept ownmem out of a mechanical SKIP against claude-mem. Fast star growth for its age (98 stars, 7 days old) is worth a second look before a deeper eval rather than dismissing it on job-description overlap alone. Left at discovery-log.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jevmem](https://github.com/Avinash-jetwani/jevmem) | tool | Automatic project memory (MIT) for Claude Code, also Cursor and Codex | Project memory across coding-agent sessions requires manual setup or a hand-rolled store | claude-mem, compact-adviser, OMEGA |
