# Evaluation: graphrelay

**Repo:** [openwt-vn/graphrelay](https://github.com/openwt-vn/graphrelay)
**Stars:** 6 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-11
**Last triaged:** 2026-11-11  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local binary that gives a coding agent a map of how a codebase connects — no cloud service
and no Python daemon, per the repo's own description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-11) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not to
judge the tool's actual behavior — it would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `codegraph` (STACK pick, ADOPT, MEASURED) — a pre-indexed,
auto-syncing code knowledge graph that already gives agents structural awareness of a
codebase without grepping, with a real run behind its verdict. graphrelay's one-liner
("a real map of how your code connects, no cloud or Python daemon") describes the identical
job with no stated differentiator, from a brand-new (★6, days old) repo against a measured
incumbent. A second tool for this job earns nothing until it shows one.

_Triaged 2026-11-11 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [graphrelay](https://github.com/openwt-vn/graphrelay) | tool | Local binary (MIT) giving a coding agent a real map of how the codebase connects, no cloud or Python daemon | Agents grep their way through a codebase for structure, with no local, dependency-free map of how the code actually connects | serena, codegraph, sieve |
