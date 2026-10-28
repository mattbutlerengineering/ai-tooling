# Evaluation: Vesalius

**Repo:** [haplollc/Vesalius](https://github.com/haplollc/Vesalius)
**Stars:** 79 | **Last updated:** 2026-10-26 (pushed) | **License:** none declared (proprietary; the bundled VS Code extension is separately MIT-licensed)
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An on-device map of a codebase for Claude Code: a code graph reachable from an MCP server, a CLI, a native Mac app, and a VS Code extension.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (codegraph, serena). That is sufficient for a SKIP that turns on redundancy with catalogued incumbents, not on the tool's behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `codegraph` and `serena` (both ADOPT, MEASURED). All three solve the same job — a persistent, structural map of the codebase an agent or editor can query — and codegraph/serena already cover it with run-backed evidence in this catalog. Vesalius also ships with no declared top-level license (all rights reserved outside its VS Code extension), which is a real adoption blocker on its own even setting the overlap aside.

_Triaged 2026-10-28 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Vesalius](https://github.com/haplollc/Vesalius) | tool | On-device codebase map for Claude Code (⚠️ no license, VS Code ext only MIT) — code graph via MCP server, CLI, Mac app, and VS Code extension | Agents and developers lack a persistent, cross-tool map of a codebase's structure reachable from the CLI, editor, and a native Mac app | Understand-Anything, codegraph, graphify, serena |
