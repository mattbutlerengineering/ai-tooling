# Evaluation: sloptrim

**Repo:** [seyedehsanhadi/sloptrim](https://github.com/seyedehsanhadi/sloptrim)
**Stars:** 125 | **Last updated:** 2026-08-13 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-16
**Last triaged:** 2026-08-16  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Local detector for AI-writing patterns that scores every prose file an agent saves — stdlib
Python only, no network call, no model in the loop.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (anti-slop, taste-skill, unlazy). That is sufficient to
place the lead and note none of its named overlaps are STACK incumbents, not to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: anti-slop (AgriciDaniel) and taste-skill cover adjacent ground (prose/UI
slop) but neither is in STACK, and sloptrim's zero-dependency, no-model, no-network detector is a
distinct mechanism from an LLM-judged or structural-test approach. Not clearly dominated. Left
for the P0/eval-runner lane.

_Triaged 2026-08-16 by the P3 backlog band._
