# Evaluation: unlazy

**Repo:** [Leonxlnx/unlazy](https://github.com/Leonxlnx/unlazy)
**Stars:** 37 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-13
**Last triaged:** 2026-08-13  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

An anti-laziness skill for AI agents built around a "Depth Tree" method: split a task N layers
deep and give every leaf the full time budget of the whole task, so effort multiplies with
depth instead of thinning out as the agent goes deeper.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell.

## Triage note

Sits in the same "agent behaviour discipline" cluster as `HERO-Anti-OverDefense`, `ratchet`, and
`pristine-skill`, but targets the opposite failure mode — *underthinking/premature completion*
rather than overbuilding or drift. It isn't redundant with any of those on a source read; a
mechanical SKIP would need a same-direction incumbent this lead doesn't have. Left for a real
hands-on look (or a with/without A/B per the skill measurement protocol) rather than disposed
here.

_Triaged 2026-08-13 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [unlazy](https://github.com/Leonxlnx/unlazy) | skill | Anti-laziness skill (MIT) using a Depth Tree method — splits a task N layers deep, giving every leaf the full task time budget | Agents underthink and prematurely complete work, cutting corners deeper into a task tree | HERO-Anti-OverDefense, ratchet, pristine-skill |
