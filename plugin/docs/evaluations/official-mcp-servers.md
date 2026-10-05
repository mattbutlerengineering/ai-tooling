# Evaluation: official-mcp-servers

**Repo:** [VoltAgent/official-mcp-servers](https://github.com/VoltAgent/official-mcp-servers)
**Stars:** 44 | **Last updated:** 2026-10-05 (pushed) | **License:** MIT
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Reference (discovery)
**Layer:** Process

---

## What it does

A curated directory of 280+ official MCP servers from the companies behind the
products — explicitly excluding unofficial forks and abandoned projects.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`, not SKIPped. `triage.py`'s pressure computation lists this
lead as "challenging" `code-review`, `feature-dev`, and `pr-review-toolkit`, which is
an artifact of this row's `claude-plugins-official` overlap citation resolving to
several STACK picks that ship inside that one monorepo slug (#465's shared-slug
shape) — not a real functional overlap between an MCP-server directory and code-review
plugins. The genuine peer is `awesome-mcp-servers` (90K-star community directory);
`official-mcp-servers`'s differentiator (official-only, no forks/abandoned) is real
but narrower in scope (280 vs. the full ecosystem), so this is a complement, not a
clear redundancy, and is left for a closer look rather than mechanically SKIPped.

_Triaged 2026-10-05 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [official-mcp-servers](https://github.com/VoltAgent/official-mcp-servers) | reference | Curated directory (MIT) of 280+ official MCP servers from the companies behind the products — no unofficial forks, no abandoned projects | Finding official (vs. unofficial fork/abandoned) MCP servers means checking each vendor's repo by hand | awesome-mcp-servers, claude-plugins-official |
