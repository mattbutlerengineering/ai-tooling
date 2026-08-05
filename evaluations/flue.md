# Evaluation: flue

**Repo:** [withastro/flue](https://github.com/withastro/flue)
**Stars:** 7,692 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Implement (sandboxed execution)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Described by its authors as "the sandbox agent framework" — from the Astro team.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to
place and band it; not enough for any verdict, and none is offered.

## Triage note

Twenty-one rows in this slice were SKIPped as app-building frameworks with no dev-loop bridge, per `WORKFLOW.md`'s **Tools Deliberately Excluded** rule and the `langchain` precedent. This row was **not**, and the reason is specific rather than generous.

The word doing the work is **sandbox**, and its `Overlaps with` cell names `sandcastle`,
`agent-sandbox` and `daytona` — all three of which are in scope, because they isolate coding agents
working on your repository. If flue is in that lane it belongs; if it is a framework for building
sandboxed *product* agents it does not.

A one-line self-description cannot tell those apart, and this slice has just demonstrated why guessing
is unsafe: `arrow-js` was SKIPped only after its eval established that its sandbox isolates a
*rendering realm* rather than an agent process, and `cloudflare/agents`' overlaps cell was found to
mix in-scope repo sandboxes with out-of-scope agent-deployment infrastructure under the same word.

Left pending a read of what it actually sandboxes. That question is the whole verdict.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [flue](https://github.com/withastro/flue) | framework | The sandbox agent framework (Apache-2.0) — run agent code in isolated sandboxes | Need programmatic, isolated sandboxes to run agent code safely | sandcastle, agent-sandbox, daytona |
