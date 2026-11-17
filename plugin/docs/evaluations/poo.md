# Evaluation: poo

**Repo:** [morajabi/poo](https://github.com/morajabi/poo)
**Stars:** 66 | **Last updated:** 2026-11-16 (pushed) | **License:** MIT
**Last verified:** 2026-11-17
**Last triaged:** 2026-11-17  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A macOS menu-bar app, CLI, and MCP server that finds and safely frees the disk space dev
work eats — build artifacts, caches, simulators, and agent worktrees.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner. That is sufficient to place the lead, not to judge
whether its "safe" reclamation actually avoids deleting anything live — it would not
support an ADOPT, and this eval offers none.

## Triage note

No STACK pick does disk-space reclamation specifically; `worktrunk` and `h5i` manage
worktree *isolation* for parallel agents, not disk hygiene after the fact, so there is no
incumbent this is redundant with. Left at `discovery-log` per the P3 band's default
disposition; the "safely" claim in its own description (avoiding live builds/caches) is
exactly what a hands-on eval would need to verify before any adoption call.

_Triaged 2026-11-17 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [poo](https://github.com/morajabi/poo) | tool | Menu-bar app, CLI, and MCP server (MIT) that safely frees the disk space dev work eats — builds, caches, simulators, agent worktrees | Builds, caches, simulators, and agent worktrees silently consume disk space with no safe way to find and reclaim it | worktrunk, h5i |
