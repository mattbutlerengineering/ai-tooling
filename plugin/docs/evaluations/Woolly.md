# Evaluation: Woolly

**Repo:** [rjcuff/Woolly](https://github.com/rjcuff/Woolly)
**Stars:** 12 | **Last updated:** 2026-11-13 (pushed) | **License:** MIT
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Infrastructure

---

## What it does

A local, private memory layer shared across Claude, Cursor, Ollama, and any
other MCP-speaking app, kept up to date across tools rather than siloed per
tool.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier. Sits in an already-dense cross-tool local-memory
cluster (`delx-memory`, `mex`, `ai-memory`) but at 12 stars and days old there
isn't yet a basis to call it dominated. Left at `discovery-log` for a full
hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Woolly](https://github.com/rjcuff/Woolly) | tool | Local, private memory layer (MIT) shared across Claude, Cursor, Ollama, and any MCP app | Each AI tool keeps its own memory with nothing shared, local, or kept up to date across them | delx-memory, mex, ai-memory |
