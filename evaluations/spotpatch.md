# Evaluation: spotpatch

**Repo:** [huanglvjing/spotpatch](https://github.com/huanglvjing/spotpatch)
**Stars:** 35 | **Last updated:** 2026-08-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A local-first, development-only tool: click any React UI element to jump straight to
its exact JSX/TSX source, inspect the proven API data flow behind it, and prepare
reviewable AI patches from that context.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. It would not support an ADOPT, and this
eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped. It overlaps `code-review`/`brooks-lint`/`vet`
by topic (review tooling) but does a genuinely different job — element-to-source-to-patch
navigation scoped to React UIs, not PR-level review. That's differentiated enough to
deserve a real hands-on look rather than a mechanical "redundant with code-review" call.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [spotpatch](https://github.com/huanglvjing/spotpatch) | tool | Click a React UI element to jump to its JSX/TSX source, trace API data flow, and prepare reviewable AI patches (MIT) | Reviewing AI-generated React changes means hunting for the source by hand; want element-to-source-to-patch in one click | code-review, brooks-lint, vet |
