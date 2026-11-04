# Evaluation: symbolhop

**Repo:** [stanczykwyatt/symbolhop](https://github.com/stanczykwyatt/symbolhop)
**Stars:** 2 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Plan (code navigation, used during Implement)
**Layer:** Tooling

---

## What it does

An MCP server and CLI giving coding agents go-to-definition and find-references,
answered from the project's real language servers rather than from grep or a
hand-built index. Read-only, no dependencies, and works across Codex, Claude Code,
Gemini CLI, and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether LSP-backed lookups are meaningfully more
accurate than grep in practice, across languages, is untested here.

## Triage note

Left at `discovery-log` (P2 challenger) — the `Overlaps with` cell cites `codegraph`
and `graphify`, both STACK picks, so this lands in P2. Not SKIPped as redundant: both
STACK incumbents are knowledge-graph tools (pre-indexed structure, cross-artifact
queries), while symbolhop answers from the project's actual language servers with no
index to build or keep in sync — a different mechanism for a related but distinct job
(precise lookup vs. broad structural understanding). That difference is enough to
leave it for a real hands-on eval rather than dispose of it as a duplicate. Left for
the P0/`eval-runner` lane.

_Triaged 2026-11-04 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [symbolhop](https://github.com/stanczykwyatt/symbolhop) | tool | Go-to-definition and find-references MCP server/CLI (MIT) for coding agents, answered from real language servers instead of grep | Agents navigate code by grepping for names instead of asking a language server for accurate definitions and references | codegraph, graphify, Understand-Anything |
