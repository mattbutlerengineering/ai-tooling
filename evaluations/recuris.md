# Evaluation: Recuris

**Repo:** [Gen-Verse/Recuris](https://github.com/Gen-Verse/Recuris)
**Stars:** 50 | **Last updated:** 2026-08-27 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-27
**Last triaged:** 2026-08-27  <!-- triaged: bulk -->
**Dev loop stage:** Reflect (memory evolution across sessions)
**Layer:** Infrastructure

---

## What it does

A recursive experiential/working-memory evolution framework (arXiv-backed) aimed
at long-horizon agent harnesses — encodes what an agent learns across a run into a
memory representation intended to self-evolve rather than accumulate as flat
context, per the linked paper (arxiv.org/abs/2608.24876).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place
the lead and check it against catalogued incumbents, not to validate the paper's
claims or measure a real memory-quality delta.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`. `triage.py` places this in P3 backlog — no catalogued
STACK pick's "Overlaps with" cell names it. It sits in the crowded Memory & Context
category alongside ACE, hivemind, and MemOS, all pursuing similar
experience-into-reusable-memory goals; a real hands-on eval would need to compare
it against those rather than a mechanical dispositon today.

_Triaged 2026-08-27 by the daily discovery pass (P3 backlog band)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Recuris](https://github.com/Gen-Verse/Recuris) | framework | Recursive experiential/working-memory evolution framework (Apache-2.0, arXiv-backed) for long-horizon agent harnesses | Long-horizon agents lose useful experience as context grows; want memory that self-evolves instead of flat accumulation | ACE, hivemind, MemOS |
