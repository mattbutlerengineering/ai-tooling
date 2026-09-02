# Evaluation: weave

**Repo:** [Ataraxy-Labs/weave](https://github.com/Ataraxy-Labs/weave)
**Stars:** 1,266 | **Last updated:** 2026-09-01 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-02
**Last triaged:** 2026-09-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An entity-level git merge driver — resolves false conflicts Git invents by understanding
code structure via tree-sitter, so two branches editing different functions in the same
file no longer collide.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata and the CATALOG "Overlaps with" cell.

## Triage note

Bands as a P2 challenger against `resolving-merge-conflicts` (a STACK pick, MEASURED), but
the jobs differ: `resolving-merge-conflicts` is a skill guiding an agent through resolving
conflicts it hits, while weave is a structure-aware git *merge driver* that prevents false
conflicts from being raised at all — a different point in the workflow (automatic,
pre-conflict vs. assisted, at-conflict). Not clearly redundant; left at `discovery-log`.

_Triaged 2026-09-02 by the P2 challenger band (daily discovery-and-triage routine, bulk,
eliminate-only). Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [weave](https://github.com/Ataraxy-Labs/weave) | tool | Entity-level git merge driver (Apache-2.0, Ataraxy Labs) — resolves false conflicts Git invents by understanding code structure via tree-sitter, so two branches editing different functions in the same file no longer collide | Git merges by line ranges and flags conflicts on edits to unrelated functions in one file; want structure-aware automatic resolution | sem, resolving-merge-conflicts (skill), worktrunk |
