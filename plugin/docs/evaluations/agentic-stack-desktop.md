# Evaluation: agentic-stack-desktop

**Repo:** [codejunkie99/agentic-stack-desktop](https://github.com/codejunkie99/agentic-stack-desktop)
**Stars:** 55 | **Last updated:** 2026-09-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-11
**Last triaged:** 2026-09-11  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A native macOS workspace app that builds one local knowledge graph shared across
Claude Code, Codex, OpenCode, and Cursor sessions, so context learned in one CLI is
visible to the others.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is enough to place it and
note nearby entries, not to judge whether the cross-CLI graph actually stays
consistent in practice.

## Triage note

Left at `discovery-log` rather than SKIPped: `claude-mem` (a STACK ADOPT pick) is
Claude-Code-only persistent memory; `ownmem` shares a memory store across CLIs but as
flat Markdown files, not a knowledge graph, and has no desktop UI; `okf-agent-memory`
is a git-native MCP memory server, not a native app. agentic-stack-desktop's
cross-CLI-graph-plus-desktop-UI combination isn't a clean match for any single
incumbent, so this deserves a real eval rather than a mechanical SKIP.

_Triaged 2026-09-11 — daily discovery pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentic-stack-desktop](https://github.com/codejunkie99/agentic-stack-desktop) | tool | Native macOS workspace (Apache-2.0) building one local knowledge graph shared across Claude Code, Codex, OpenCode, and Cursor sessions | Session context and learned knowledge are siloed per coding-agent CLI; want one shared local graph across all of them | ownmem, okf-agent-memory, ECC |
