# Evaluation: claude-code-routing

**Repo:** [ToolMonsters/claude-code-routing](https://github.com/ToolMonsters/claude-code-routing)
**Stars:** 22 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Rebuilds Spotify's published 90%-cheap-model Claude Code routing setup for plain Claude
Code, routing reading/boilerplate work to a cheaper model and measuring the result on 4
real tasks.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. P3 backlog — nothing structural flags it for a mechanical
disposition; stamping records that it was examined.

_Triaged 2026-09-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-code-routing](https://github.com/ToolMonsters/claude-code-routing) | tool | Spotify's 90% Claude Code model-routing setup (MIT), rebuilt for plain CC and measured on 4 real tasks | Every step of an agent task runs on the expensive model by default; want a cheap model routed to reading/boilerplate work | deadeye-cc, claude-code-router, litellm |
