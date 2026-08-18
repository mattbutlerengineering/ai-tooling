# Evaluation: ctxwise

**Repo:** [FramY2/ctxwise](https://github.com/FramY2/ctxwise)
**Stars:** 4 | **Last updated:** 2026-08-17 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local-first context audit tool for Codex — see what context is loaded, get drift
detection against what was intended, and honest token receipts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. It would not support an ADOPT, and this
eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped. `headroom` (in STACK) *compresses* tool
output before it reaches the context window; ctxwise *audits/observes* what's already
loaded and flags drift — a different job (inspection vs. compression), and complementary
rather than competing. Very early (4 stars) — not enough signal yet to weigh further, so
left rather than promoted.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ctxwise](https://github.com/FramY2/ctxwise) | tool | Local-first context audit for Codex (Apache-2.0) — see what's loaded, drift detection, and honest token receipts | Codex context loading is opaque; want visibility into what's loaded and when it drifts from what was intended | headroom, context-mode, lean-ctx |
