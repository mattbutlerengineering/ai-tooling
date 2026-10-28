# Evaluation: floorplan

**Repo:** [haydenschmitty/floorplan](https://github.com/haydenschmitty/floorplan)
**Stars:** 109 | **Last updated:** 2026-10-28 (pushed) | **License:** MIT
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

An interactive, plain-English map of how an app's codebase actually fits together, drawn by Claude — a narrative architecture explainer rather than a structural index.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It shares the "codebase understanding" job with `codegraph` (ADOPT, already in STACK) but takes a different approach — a plain-English, narrative map rather than an indexed knowledge graph — closer in spirit to `Understand-Anything` and `StructSmith`. That differentiation is enough to leave it for a real hands-on look rather than dispose it as a mechanical redundancy.

## Triage note

P2 challenger — cites `codegraph` in "Overlaps with". Left at `discovery-log` rather than SKIPped: floorplan's narrative, plain-English explainer is a distinct approach from codegraph's indexed graph, and dismissing it as redundant would discard a genuinely different angle on the same problem without a hands-on comparison.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [floorplan](https://github.com/haydenschmitty/floorplan) | tool | Interactive, plain-English map of how an app's codebase actually fits together, drawn by Claude (MIT) | Onboarding to an unfamiliar codebase means manually tracing structure instead of seeing an interactive architecture map | Understand-Anything, codegraph, StructSmith, codebase-map |
