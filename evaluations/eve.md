# Evaluation: eve

**Repo:** [vercel/eve](https://github.com/vercel/eve)
**Stars:** 4,354 | **Last updated:** 2026-08-05 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Implement (agent framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Vercel's "open framework for building agents".

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to
place and band it; not enough for any verdict, and none is offered.

## Triage note

Twenty-one rows in this slice were SKIPped as app-building frameworks with no dev-loop bridge, per `WORKFLOW.md`'s **Tools Deliberately Excluded** rule and the `langchain` precedent. This row was **not**, and the reason is specific rather than generous.

On its description alone — "The Open Framework for **Building Agents**" — this reads like a
straightforward member of the disposed class. Two things stop it being disposed on that basis.

First, it is catalogued under **Agent Harnesses** ("frameworks that structure, enhance, or optimize
how a single coding agent operates"), not Agent Orchestration. The section placement is a claim that
someone judged it to be about coding agents, and this lane should not silently overturn a placement
call it cannot check.

Second, its stablemate `vercel/ai` is the one framework in this slice that *cleared* the bar, on a
coding-agent skill and a harness-building primitive. A Vercel agent framework is therefore exactly the
case where the vendor's other row proves a bridge is possible — and `vercel/workflow`, disposed in this
same pass, proves it is not automatic. Same vendor, three rows, and the disposition has to be decided
per row rather than by association.

Left pending a read. Of the four framework rows this pass declined to dispose, this is the one most
likely to be a scope SKIP once someone looks.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [eve](https://github.com/vercel/eve) | harness | TypeScript framework for building stateful, sandboxed AI agents on Vercel (Apache-2.0, ★3K) | Building production agents needs sandboxing, state management, and cloud deployment built in | cloudflare/agents, agno, strands-agents (harness-sdk), moltworker |
