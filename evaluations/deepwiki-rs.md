# Evaluation: deepwiki-rs

**Repo:** [sopaco/deepwiki-rs](https://github.com/sopaco/deepwiki-rs)
**Stars:** 1,382 | **Last updated:** 2026-07-24 (pushed) | **License:** MIT
**Dev loop stage:** Plan (codebase comprehension)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Generates technical documentation and AI-ready context from a codebase in minutes — Rust,
local-first, no cloud service.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus the
CATALOG one-liner and "Overlaps with" cell (`docmd`, `PocketFlow-Tutorial-Codebase-Knowledge`, `deepwiki`).
Enough to place it against its larger twin; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, and the comparison that could have disposed it is the reason it stays.

The obvious call is supersession: `PocketFlow-Tutorial-Codebase-Knowledge` does the same job at ★12.4K
against this row's ★1.4K, and a size-based pass writes the SKIP without reading further. But the
differentiator is stated in the one-liner and it is real — **local-first, in Rust, without a cloud
service**, where PocketFlow drives an LLM API. For code that cannot leave the building, that is not a
smaller version of the same tool; it is the only version that can run at all.

It also names `deepwiki` (external, Cognition's hosted service) as a peer, which sharpens the point: this is
the self-hosted answer to a capability whose best-known implementation is a SaaS.

Both this row and PocketFlow were left standing, and the honest framing is that they answer the same question
under different constraints. A measured comparison would be about *output quality* — does the local pipeline
produce documentation as accurate as the model-driven one — which is exactly the sort of thing
`evaluations/measurement-protocols.md` describes and a source-only read cannot approximate.

MIT, pushed 2026-07-24.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deepwiki-rs](https://github.com/sopaco/deepwiki-rs) | tool | Generate accurate technical docs and AI-ready context from code in minutes (MIT, Rust, local-first) | Codebases lack up-to-date machine-readable documentation; generates structured docs locally without a cloud service | docmd, PocketFlow-Tutorial-Codebase-Knowledge, deepwiki (ext.) |
