# Evaluation: frugent

**Repo:** [shinefuer/frugent](https://github.com/shinefuer/frugent)
**Stars:** 37 | **Last updated:** 2026-10-30 (pushed) | **License:** MIT
**Last verified:** 2026-11-01
**Last triaged:** 2026-11-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A cost-efficient coding-agent runtime (MIT, NumPy core, CPU-only torch extra): prefix-aware prompt-cache routing, a poisoning-safe semantic cache, budgeted context compression, request batching/dedup, cascading model routing with DP-optimal policies, hard budget scheduling, sandboxed tools, and span-level cost attribution.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (litellm, deadeye-cc, headroom). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead.

## Triage note

P2 challenger — cites `headroom` (ADOPT, in STACK) in "Overlaps with." Left at `discovery-log` rather than SKIPped: `headroom` compresses tool/log output before it reaches the model, which is one piece of what this tool claims (budgeted context compression) alongside several others headroom does not cover — prompt-cache routing, semantic caching, request batching/dedup, cascading model routing, and cost attribution. The scope is broader than a straight redundancy claim would require.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [frugent](https://github.com/shinefuer/frugent) | tool | Cost-efficient coding-agent runtime (MIT) — prompt-cache-aware routing, semantic caching, budgeted context compression, cascading model routing | Coding-agent runs burn budget on cache misses and uniform full-price model calls with no cost-aware runtime underneath | litellm, deadeye-cc, headroom |
