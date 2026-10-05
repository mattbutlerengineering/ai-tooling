# Evaluation: sieve

**Repo:** [iamalvisng/sieve](https://github.com/iamalvisng/sieve)
**Stars:** 0 | **Last updated:** 2026-10-05 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-05
**Last triaged:** 2026-10-05  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local Rust CLI that returns exact files, lines, and callers for a coding agent — no
API key, no network call.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. Day-one repo, 0 stars.

## Triage note

Left at `discovery-log`, not SKIPped — challenges `serena` (STACK) in overlap
pressure. `serena` is an LSP-backed semantic-retrieval MCP server; `sieve` pitches a
much smaller, local, no-API-key CLI for exact file/line/caller lookup, which could be
a lighter-weight complement rather than a substitute. 0 stars and days old, so there
is no usage signal yet to confirm the performance/simplicity trade-off actually holds.

_Triaged 2026-10-05 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sieve](https://github.com/iamalvisng/sieve) | tool | Local Rust CLI (Apache-2.0) returning exact files, lines, and callers for a coding agent, no API key | Agents grep/read whole files to locate code; want exact local code-search results without sending code to an API | serena, jevgrep, trace-mcp |
