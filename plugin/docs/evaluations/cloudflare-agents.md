# Evaluation: cloudflare/agents

**Repo:** [cloudflare/agents](https://github.com/cloudflare/agents)
**Stars:** 5,353 | **Last updated:** 2026-08-04 (pushed) | **License:** MIT
**Dev loop stage:** Out of loop (application framework)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Cloudflare's framework for building and deploying AI agents on Workers and Durable Objects.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. That is
sufficient for a **scope** SKIP, which turns on what class of artifact this is rather than on how
well it works — and the repository's own one-sentence self-description settles the class. It is not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — app-building framework, no dev-loop bridge.** Its own description is "**Build and deploy AI Agents on Cloudflare**" — deployment infrastructure for agent applications, single-vendor.

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise` and `RAGFlow`. The test, per the `langchain` eval, is whether the
framework has a **dev-loop bridge**: `fast-agent` has one (it doubles as a runnable MCP-native coding
agent), `vercel/ai` has one (a coding-agent skill plus a harness-building primitive). This row has
none visible.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

Its `Overlaps with` cell names `sandcastle`, `agent-sandbox`, `LangGraph.js` and `moltworker`, which mixes two different things and is worth untangling: `sandcastle` and `agent-sandbox` isolate **coding agents working on your repo** and are in scope; this row and `LangGraph.js` build **agent products**. Sharing the word "agent" is not sharing a category — the same confusion `arrow-js`'s eval unpicked for the word "sandbox".

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cloudflare/agents](https://github.com/cloudflare/agents) | framework | TypeScript SDK for building and deploying persistent AI agents on Cloudflare Durable Objects (MIT, ★5.2K) | Deploying stateful AI agents to production requires durable storage and edge compute baked in | eve, sandcastle, LangGraph.js, moltworker |
