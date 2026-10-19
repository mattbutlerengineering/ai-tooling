# Evaluation: graphicle

**Repo:** [Graphicle-AI/graphicle](https://github.com/Graphicle-AI/graphicle)
**Stars:** 276 | **Last updated:** 2026-10-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A single Rust binary that maps a repository into a code graph and keeps a memory of the
project's docs, decisions, and past agent sessions, then hands a coding agent cited excerpts
(exact file + line) from both. Runs locally with no API key, no account, and no telemetry;
works with Claude Code, Cursor, Codex, VS Code, Claude Desktop, or any MCP client. Ships a
migration doc from `Graphify-Labs/graphify` (already catalogued), positioning itself as a
successor/alternative in the same code-graph niche.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow
clone's README and LICENSE. That confirms the license and the claimed scope (code graph +
session memory, cited retrieval), not the benchmark numbers the README itself links to.

## Verdict

**discovery-log — tentative read** — newly catalogued this pass; not previously examined.

## Triage note

New lead, added today. Not a P2 challenger: the catalog's existing code-graph tools
(`codegraph`, `graphify`, `Understand-Anything`) are leads too, not STACK picks, so there is no
incumbent to be redundant with — and graphicle's explicit migrate-from-`graphify` doc plus the
added session-memory half make it worth a first-time look rather than a mechanical SKIP. Left
at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [graphicle](https://github.com/Graphicle-AI/graphicle) | tool | Local-first Rust code-graph + memory engine (Apache-2.0) giving coding agents cited file/line excerpts from the repo graph and past sessions | Agents answer from guesses instead of cited source; want a local, no-API-key graph+memory layer any MCP client can query | codegraph, graphify, Understand-Anything |  |
