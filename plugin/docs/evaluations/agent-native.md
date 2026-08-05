# Evaluation: agent-native

**Repo:** [BuilderIO/agent-native](https://github.com/BuilderIO/agent-native)
**Stars:** 4,408 | **Last updated:** 2026-08-05 (pushed) | **License:** **none declared**
**Dev loop stage:** Out of loop (product UI / app platform)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A framework for structuring applications so that AI agents can operate them by design.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Verdict

**SKIP — product-facing framework, no dev-loop bridge.** Its own description is "a framework for building **agent-native applications**". It is one of seven generative-UI rows disposed together in this pass (`tambo`, `agent-native`, `assistant-ui`, `hashbrown`, `OpenGenerativeUI`, `json-render`, `mcp-ui`), all answering how an agent drives the interface of an application you ship. The reasoning was already on file before this pass: the `openui` triage note records that this family "matter[s] when you are building an agent-backed product, not when you are using an agent to write code", and `CopilotKit` — the cluster's reference implementation — was SKIPped in the preceding pass on its own admission that it is "not relevant to in-terminal coding workflows".

`WORKFLOW.md`'s **Tools Deliberately Excluded** table states the rule — "Flowise, LangGraph —
visual/programmatic agent builders: for building AI products, not for your own dev workflow" — and the
catalog has applied it to `langchain`, `LangChain.js`, `LangGraph`, `LangGraph.js`, `crewAI`,
`aisuite`, `dify`, `Flowise`, `RAGFlow`, and to twenty-one further framework rows in the pass
immediately before this one. Per the `langchain` eval the test is a **dev-loop bridge**: `fast-agent`
has one (it doubles as a runnable MCP-native coding agent), `vercel/ai` has one (a coding-agent skill
plus a harness-building primitive). This row has none.

The SKIP removes nothing — per the `Flowise` precedent the entry stays in `CATALOG.md` as a reference
row. Re-open if a dev-loop bridge appears; nothing here disputes the project's quality.

**~~A second, independent ground: no license.~~ Withdrawn 2026-08-05.** That paragraph read: the `CATALOG.md` row carries "⚠️ no license = not adoptable", re-verified rather than trusted by a live fetch on 2026-08-04 returning `license: null`, and *"a cached `NONE` is not evidence; a same-day confirmed absence is."*

The instinct was right and the check was still wrong. `license: null` is not a confirmed absence — GitHub's licensee detector reads a root `LICENSE` file and nothing else, and this repo's README carries a `## License` section reading `MIT` (#372). The re-fetch confirmed the API's answer a day fresher, which is not the same as confirming the repo's terms. That the paragraph re-checked *because* `vercel-labs/skills` had survived exactly this trap makes the point sharper, not softer: a second look in the same place finds the same blind spot.

This row is also the set's one genuine **conflict** — the README says MIT and `package.json` says **ISC** — and the standing tiebreak from #26 ("the LICENSE file governs, not the README badge or package metadata") has nothing to govern with when there is no LICENSE file. Both are permissive, so nothing turns on it here; it is recorded because the next row where it happens may not be so lucky.

**The scope ground is untouched and decides the row on its own** — which is why the verdict does not move. It was recorded as independent precisely so that one ground failing would not take the other with it, and that is what happened.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-native](https://github.com/BuilderIO/agent-native) | framework | Framework for building agent-native applications (MIT per README, ISC in package.json, no LICENSE file; ★3.2K) — structure apps so AI agents can operate them by design | Apps aren't built for agents to drive; want a framework that makes an app agent-operable by design | CopilotKit, tambo, CLI-Anything |
