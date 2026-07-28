# Evaluation: weave

**Repo:** [Ataraxy-Labs/weave](https://github.com/Ataraxy-Labs/weave)
**Stars:** ~1,217 | **Last updated:** 2026-07-09 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Ship
**Layer:** Tooling

---

## What it does

An entity-level git merge driver that resolves false conflicts Git invents by understanding code structure via tree-sitter, so two branches editing different functions in the same file no longer collide.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: `repo-metadata.json` (1.2K stars, Apache-2.0, pushed 2026-07-09) plus the CATALOG "Overlaps with" cell against sem/resolving-merge-conflicts/worktrunk.

## Triage note

P2 challenger band (overlaps `resolving-merge-conflicts`, a STACK pick), but the two are complementary rather than redundant: `resolving-merge-conflicts` is an agent skill that resolves conflicts intent-preservingly after they occur, while weave is a structural git merge driver that prevents Git from inventing false conflicts in the first place. Different point in the pipeline; not dominated. Left at discovery-log for a future hands-on eval.
