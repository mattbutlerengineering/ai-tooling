# Evaluation: Remarc

**Repo:** [metedata/Remarc](https://github.com/metedata/Remarc)
**Stars:** 29 | **Last updated:** 2026-08-11 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A macOS feedback layer for AI collaboration — point at text, screenshots, web elements, or speak,
and the agent reads and resolves the comment over MCP.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby feedback/review tools, not enough for any
verdict, and none is offered.

## Triage note

Left at `discovery-log`. `facet` and `plannotator` both gate on human review, but neither offers
Remarc's specific input surface — pointing at arbitrary screen content or speaking, rather than
annotating a rendered plan or approving a gate. macOS-only, which narrows its audience; still worth
a real look rather than a mechanical dispose.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Remarc](https://github.com/metedata/Remarc) | tool | macOS feedback layer (MIT) for AI collaboration — point at text, screenshots, web elements, or speak, and the agent resolves it over MCP | Giving an agent visual/spoken feedback on what to fix means describing it in words; want to point and have the agent read the context directly | facet, plannotator |
