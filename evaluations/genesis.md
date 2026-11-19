# Evaluation: genesis

**Repo:** [GenesisAgentInfra/genesis](https://github.com/GenesisAgentInfra/genesis)
**Stars:** 52 | **Last updated:** 2026-11-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An agent skill for Claude Code and Codex that turns a codebase into a business flow
map, then overlays which agent-made changes are untested or risky against that map.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. That is sufficient to confirm the lead has no
overlap with a STACK pick (the "Overlaps with" cell names catalog-only peers), not to
judge the tool's own behavior. It would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`. No STACK incumbent does this specific job — `farol` scores PR
merge risk after review and `floorplan` draws a plain-English architecture map, but
neither combines a flow map with a risk/test-coverage overlay on agent-made changes
the way this does. Differentiated enough to deserve a real eval rather than a
mechanical SKIP.

_Triaged 2026-11-19 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [genesis](https://github.com/GenesisAgentInfra/genesis) | skill | Turns a codebase into a business flow map (Apache-2.0) flagging which agent changes are untested or risky | Seeing which agent-made changes are untested or risky means tracing the codebase's flow by hand, with no map-level signal | farol, floorplan, code-quality |
