# Evaluation: codebase-map

**Repo:** [rdilruba/codebase-map](https://github.com/rdilruba/codebase-map)
**Stars:** 5 | **Last updated:** 2026-09-13 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

Agent skill that maps an unfamiliar repo's architecture, traces real execution flows, and writes the result to `docs/codebase-map/` — a plain-file, no-infrastructure alternative to a live graph index.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-11), catalogued from today's discovery scan.

## Triage note

P2 challenger: cites `codegraph` (STACK ADOPT pick, an auto-syncing pre-indexed knowledge graph) in Overlaps. codebase-map is a plain-file skill with no persistent index/database to maintain — a lighter-weight, lower-setup alternative rather than a strict subset. Left at discovery-log; very low star count (5) and 3-day-old repo also argue for waiting rather than judging redundancy this early.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [codebase-map](https://github.com/rdilruba/codebase-map) | skill | Agent skill (MIT) that maps an unfamiliar repo's architecture, traces real execution flows, and writes the result to `docs/codebase-map/` | Contributing to an unfamiliar repo means manually tracing how it's structured before making a safe change | Understand-Anything, codegraph, PocketFlow-Tutorial-Codebase-Knowledge |  |
