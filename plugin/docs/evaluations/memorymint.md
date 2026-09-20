# Evaluation: MemoryMint

**Repo:** [anasse-hassala/MemoryMint](https://github.com/anasse-hassala/MemoryMint)
**Stars:** 43 | **Last updated:** 2026-09-08 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Memory & Context
**Layer:** Tooling

---

## What it does

Grades the retrieval policies that decide what a long-running agent remembers —
comparative scorecards over fixed, inspectable sessions, rather than a memory
implementation itself.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies. MemoryMint is a benchmark/
evaluation harness *for* memory-retrieval policies, not a memory system competing with
mem0/cognee/memoket-kite — different layer of the stack (meta-evaluator vs. implementation),
comparable to how `assay` evaluates skills/MCP servers rather than being one. Worth a look if
this catalog wants an independent check on memory-tool benchmark claims.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MemoryMint](https://github.com/anasse-hassala/MemoryMint) | tool | Grades agent memory-retrieval policies (Apache-2.0) via comparative scorecards over fixed, inspectable sessions | Choosing a retrieval policy for a long-running agent's memory is guesswork; want a benchmarked, reproducible comparison instead | memoket-kite, mem0, cognee |
