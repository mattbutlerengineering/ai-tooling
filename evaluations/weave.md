# Evaluation: weave

**Repo:** [Ataraxy-Labs/weave](https://github.com/Ataraxy-Labs/weave)
**License:** Apache-2.0
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Entity-level git merge driver — resolves false conflicts Git invents by understanding code
structure via tree-sitter, so two branches editing different functions in the same file no
longer collide.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (sem, resolving-merge-conflicts skill, worktrunk). That is
sufficient to place the lead and note none of its named overlaps are STACK incumbents, not to
support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: none of sem, resolving-merge-conflicts, or worktrunk is in STACK, and
none does what weave does — an automatic, structure-aware git merge *driver* rather than an
agent skill or worktree manager. Parallel-agent workflows hitting false merge conflicts is a
real and growing problem; deserves a real hands-on eval rather than a mechanical SKIP. Left for
the P0/eval-runner lane.

_Triaged 2026-07-31 by the P3 backlog band._
