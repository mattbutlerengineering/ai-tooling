# Evaluation: cross-code-organizer

**Repo:** [mcpware/cross-code-organizer](https://github.com/mcpware/cross-code-organizer)
**Stars:** 375 | **Last updated:** 2026-09-12 (pushed) | **License:** MIT
**Last verified:** 2026-09-12
**Last triaged:** 2026-09-12  <!-- triaged: bulk -->
**Dev loop stage:** Verify / Outer Loop
**Layer:** Tooling

---

## What it does

A cross-harness config dashboard (formerly "Claude Code Organizer") for Claude Code,
Codex CLI, MCP servers, skills, memories, agents, and sessions — adds security
scanning (tool-poisoning detection), a context-budget view, and backups on top of
the inventory/dashboard job.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Not clearly redundant with a single named STACK incumbent — it spans the inventory
job (`geiger`), the trace/log job (`tracecrate`), and the config-dashboard job
(`claude-code-templates`) without being a strict subset of any one. Substantial and
established (375 stars, active since March) rather than a fresh clone; left at
`discovery-log` for a real hands-on eval rather than a mechanical SKIP.
