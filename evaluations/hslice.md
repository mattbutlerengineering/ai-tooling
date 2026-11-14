# Evaluation: hslice

**Repo:** [Hephaestus-Zero/hslice](https://github.com/Hephaestus-Zero/hslice)
**Stars:** 1 | **Last updated:** 2026-11-14 (pushed) | **License:** MIT
**Last verified:** 2026-11-14
**Last triaged:** 2026-11-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A sub-2ms C11 mmap 3-gram indexer and structural AST code slicer for AI coding agents, claiming a 93–96% cut in context tokens by returning a structural slice of relevant code instead of whole files.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — catalogued today; no hands-on run yet.

## Triage note

Left at `discovery-log`, not SKIPped. It challenges `serena` (STACK, LSP-based symbol-level retrieval/editing) in "Overlaps with", but hslice's own pitch is a lighter-weight, index-free structural slicer rather than a language-server-backed editor — a different technical approach to the same context-reduction problem, and the 93–96% token-cut claim is specific enough to be worth checking rather than dismissing as redundant on a single star and no hands-on run.

_Triaged 2026-11-14 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hslice](https://github.com/Hephaestus-Zero/hslice) | tool | Sub-2ms C11 mmap 3-gram indexer and structural AST code slicer (MIT) cutting agent context tokens 93–96% | Feeding whole files to a coding agent burns context tokens when only a structural slice of the code is actually relevant | serena, semble, gortex |
