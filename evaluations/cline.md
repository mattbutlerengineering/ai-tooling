# Evaluation: cline

**Repo:** [cline/cline](https://github.com/cline/cline)
**Stars:** ~64,504 | **Last updated:** 2026-07-10 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

The most-starred open-source autonomous coding agent — a VS Code extension (also SDK + CLI) that plans and executes multi-file changes with human-in-the-loop diff approval at every step, terminal command execution, browser use, and any-model/MCP support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: `repo-metadata.json` (64.5K stars, Apache-2.0, pushed 2026-07-10) plus the CATALOG "Overlaps with" cell against continue/kilocode/opencode/aider.

## Triage note

P2 challenger band (overlaps claude-squad, a STACK pick), but the overlap is shallow: claude-squad multiplexes multiple agent sessions, while cline is a complete, independent editor-native coding-agent harness — the most-starred one in the catalog. Far too significant and differentiated to mechanically SKIP as redundant. Left at discovery-log for a future hands-on eval.
