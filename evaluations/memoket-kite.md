# Evaluation: memoket-kite

**Repo:** [memoket/memoket-kite](https://github.com/memoket/memoket-kite)
**Stars:** 90 | **Last updated:** 2026-08-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

An open-source, vector-free long-term memory engine for AI agents, claiming SOTA results
on the LoCoMo and LongMemEval benchmarks with significantly less context than
vector-DB-backed approaches.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. It would not support an ADOPT, and this
eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped. None of its cited overlaps (mem0, cognee,
memU, memvid) are STACK picks, so there's no mechanical redundancy call to make. The
vector-free approach and claimed benchmark results are differentiated enough to deserve
a real hands-on eval rather than a bulk disposition.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [memoket-kite](https://github.com/memoket/memoket-kite) | tool | Vector-free long-term memory engine (Apache-2.0) claiming SOTA on LoCoMo and LongMemEval with less context | Vector-DB memory is heavy and lossy; want a lighter engine that beats it on standard long-term-memory benchmarks | mem0, cognee, memU, memvid |
