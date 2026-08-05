# Evaluation: activepieces

**Repo:** [activepieces/activepieces](https://github.com/activepieces/activepieces)
**Stars:** 23,577 | **Last updated:** 2026-08-04 (pushed) | **License:** NOASSERTION (GitHub could not parse the LICENSE file)
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An open-source workflow-automation platform with AI agents and a large MCP-server library.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description leads with "AI Agents & MCPs & **AI Workflow Automation**", and its `Overlaps with` cell names `dify`, `Flowise` and `langflow` — the first two already SKIPped, the third in this same pass. It is one of five agent/AI application platforms disposed together in this pass (`langflow`, `activepieces`, `onyx`, `mindsdb/minds`, `sim`), the same class as `dify` and `Flowise` — which the catalog already SKIPped with the note that they are "for building AI products, not for making developers more productive with AI coding agents".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

Its ~400-MCP-server library is the one thing that brushes against a category this catalog tracks, and it is not enough: those servers are wired into *automation workflows the platform runs*, not into a coding agent's tool surface. The catalog's MCP Servers section exists for the latter.

The `NOASSERTION` is not part of this disposal — it records that GitHub's parser could not read the LICENSE file, not that a grant is missing.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [activepieces](https://github.com/activepieces/activepieces) | platform | Self-hostable workflow automation with ~400 MCP integrations and AI agent support | Building AI agent workflows that connect to external services needs custom per-service integration code; want a visual, self-hostable, MCP-native automation platform | dify, Flowise, langflow |
