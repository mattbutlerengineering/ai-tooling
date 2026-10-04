# Evaluation: swe-sweep

**Repo:** [facebookresearch/swe-sweep](https://github.com/facebookresearch/swe-sweep)
**Stars:** 51 | **Last updated:** 2026-10-03 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A benchmark (Python, ★51, created 2026-10-01, by Meta's FAIR team) measuring how many
bugs language models can find and fix autonomously in large codebases, with no hints
given about bug type or location — a harder, more realistic framing than benchmarks
that point the model at a known issue.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `harbor` (discovery-log — agent evaluation + RL-environment framework, builds
benchmarks generally) and `deepeval` (discovery-log — "pytest for LLMs"); neither is a
STACK pick, so this does not band as a P2 challenger. Differentiator from harbor: this
is a fixed benchmark/dataset rather than a framework for building arbitrary benchmarks.
No archived flag, no disqualifying license, no `Ships inside` container. Left at
`discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [swe-sweep](https://github.com/facebookresearch/swe-sweep) | tool | Benchmark (MIT, by Meta) measuring how many bugs LMs can autonomously find and fix in large codebases, with no hints about bug type or location | Claims about an agent's autonomous bug-finding ability have no standardized, hint-free benchmark to back them | harbor, deepeval, EvoTrace |
