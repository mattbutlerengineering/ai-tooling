# Evaluation: figma-maxxing

**Repo:** [thiagoxikota/figma-maxxing](https://github.com/thiagoxikota/figma-maxxing)
**Stars:** 7 | **Last updated:** 2026-10-06 (pushed) | **License:** MIT
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

8 agent skills for real Figma files, for Claude Code, Codex, Copilot CLI, and Gemini CLI — 90
Plugin API gotchas, checks before and after every write, and a design-handoff gate, per the repo
description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to place the lead, not to judge
the Plugin API checks hands-on.

## Triage note

Left at `discovery-log`. No `Overlaps with` cell names a STACK pick, so this is plain P3 backlog.
It is a skill (agent-driven, instruction-based) rather than an MCP server like the catalogued
`Figma-Context-MCP`/`design-extract`, so it is a different mechanism for an adjacent job, not a
clear mechanical redundancy.

_Triaged 2026-10-06 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [figma-maxxing](https://github.com/thiagoxikota/figma-maxxing) | skill | 8 agent skills (MIT) for real Figma files, for Claude Code/Codex/Copilot CLI/Gemini CLI — 90 Plugin API gotchas, pre/post-write checks, and a design-handoff gate | Agents editing live Figma files via the Plugin API hit undocumented gotchas and ship changes with no handoff checks before or after each write | Figma-Context-MCP, design-extract, airship |
