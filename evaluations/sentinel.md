# Evaluation: SENTINEL

**Repo:** [GarvitAgrawal04/SENTINEL](https://github.com/GarvitAgrawal04/SENTINEL)
**Stars:** 12 | **Last updated:** 2026-09-25 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A static analyzer, merge gate, and signed lockfile (Apache-2.0) that shows what a file would
actually make an AI coding agent do — covering `CLAUDE.md`, `AGENTS.md`, `.cursorrules`, hooks,
and MCP configs — before it merges.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (agnix, agent-scan, geiger). That is sufficient to note the
overlap with existing agent-config linters/scanners, not to judge whether its merge-gate and
signed-lockfile mechanics are materially better or redundant — it would not support an ADOPT,
and this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped as redundant: `agnix` lints agent-config files for
validity and `agent-scan` flags known risk patterns in installed configs, but neither is a STACK
pick, and neither ships a merge gate with a signed lockfile recording what changed between
approvals — a distinct mechanism from a one-shot lint or scan. Worth a first-time hands-on eval
before any redundancy call.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [SENTINEL](https://github.com/GarvitAgrawal04/SENTINEL) | tool | Static analyzer, merge gate, and signed lockfile (Apache-2.0) showing what CLAUDE.md/AGENTS.md/.cursorrules/hooks/MCP configs would make an agent do | Agent instruction files and MCP configs merge with no static check on what they'd actually make the agent do, or a signed record of what changed | agnix, agent-scan, geiger |
