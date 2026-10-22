# Evaluation: LeanKG

**Repo:** [FreePeak/LeanKG](https://github.com/FreePeak/LeanKG)
**Stars:** 221 | **Last updated:** 2026-10-22 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-22
**Last triaged:** 2026-10-22  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Infrastructure

---

## What it does

An enterprise code knowledge graph for AI coding agents (Apache-2.0, Go) — multi-repo
indexing, environment governance, incidents/services, and requirement↔code links. The
project claims −65% tokens / −85% tool calls (self-reported, unverified here).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.
The −65%/−85% figures are the vendor's own self-reported claim and are **not** verified
by this eval; any future eval should run `token-savings-protocol.md` before repeating
them as fact.

## Triage note

Bands as a P2 challenger against `codegraph` (ADOPT, pressure 0). `codegraph` is a
single-repo code graph; LeanKG's differentiator is explicit multi-repo indexing plus
env/incident/service governance and requirement↔code links — a broader, enterprise-scoped
job that `codegraph` does not claim to do. Not clearly redundant. Left at `discovery-log`
for a real hands-on eval (and a check of the unverified token-savings claim).

_Triaged 2026-10-22 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [LeanKG](https://github.com/FreePeak/LeanKG) | MCP server | Enterprise code knowledge graph for AI coding agents (Apache-2.0, Go) — multi-repo indexing, env governance, incidents/services, and requirement↔code links; claims −65% tokens / −85% tool calls (self-reported) | Agents re-derive multi-repo structure, ownership, and requirement↔code links from scratch each session; want a persistent, queryable knowledge graph | codegraph, Understand-Anything, graphify |
