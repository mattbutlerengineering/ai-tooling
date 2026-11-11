# Evaluation: lot-map

**Repo:** [alexeyw/lot-map](https://github.com/alexeyw/lot-map)
**Stars:** 234 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A live map rendered beside the chat that lights up Claude Code's tool calls, model steps,
hooks, skills, and subagents as they happen. Local only, per the repo's own description, with
a UI in five languages.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell
(`claude-super-sidebar`, `shoulder`, `agent-orchestration-standard`). That is enough to place
it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log` — P3 backlog, zero overlap pressure against any STACK pick. A crowded
but undifferentiated niche (live Claude Code activity panes: `claude-super-sidebar`, `shoulder`,
`agent-orchestration-standard`, `rexpad` already catalogue similar ground), and nothing in the
source-only read distinguishes this one enough for either a confident SKIP or a priority bump.
Stamped and left for a future pass with more signal (stars, a hands-on look).

_Triaged 2026-11-11 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [lot-map](https://github.com/alexeyw/lot-map) | tool | Live map beside the chat (MIT) lighting up Claude Code's tool calls, model steps, hooks, skills, and subagents as they happen, local only | A bare terminal gives no at-a-glance live view of what a running Claude Code session's tools, hooks, and subagents are doing | claude-super-sidebar, shoulder, agent-orchestration-standard |
