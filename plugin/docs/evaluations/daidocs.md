# Evaluation: daidocs

**Repo:** [Kerneta/daidocs](https://github.com/Kerneta/daidocs)
**Stars:** 17 | **Last updated:** 2026-09-14 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Open plain-text `.dai` file format for AI memory — a spec plus an engine and an MCP server, all Apache-2.0. Memory lives on disk as grep-readable files rather than a database, so any model or tool (Claude, GPT, Gemini, Cursor, local models, or a human with `grep`) can read it directly. Ships an MCP server and hooks for Claude Code, Claude Desktop, Cursor, Windsurf, and Codex. Publishes self-reported LongMemEval-S numbers (83% GPT-4o, 92% Claude Fable 5) and a 10x-fewer-tokens claim.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool, and did not attempt to verify the published benchmark numbers. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-13), catalogued from today's discovery scan.

## Triage note

P2 challenger: cites `claude-mem` (STACK ADOPT pick) in Overlaps. daidocs' pitch is an open, plain-text, cross-model **file format** rather than a structured plugin/database like claude-mem — a genuinely different design point (portability and human/grep-readability vs. semantic search and timeline views). Left at discovery-log rather than SKIPped as redundant; the self-reported benchmark claims are unverified and would need a real run before any stronger verdict.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [daidocs](https://github.com/Kerneta/daidocs) | MCP server | Open plain-text `.dai` file format (Apache-2.0) for AI memory — one grep-readable file readable by Claude, GPT, Gemini, Cursor, and local models; ships an MCP server + hooks for Claude Code, Desktop, Cursor, Windsurf, Codex | Agent memory formats are proprietary and per-tool; want one plain-text, cross-model, cross-harness memory file | claude-mem, ownmem, okf-agent-memory |  |
