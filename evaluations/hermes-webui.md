# Evaluation: hermes-webui

**Repo:** [nesquena/hermes-webui](https://github.com/nesquena/hermes-webui)
**Stars:** 16,948 | **Last updated:** 2026-07-31 (pushed) | **License:** MIT
**Dev loop stage:** Implement (agent frontend)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A web and mobile front end for driving the Hermes coding agent from a browser or phone.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Sufficient for
a **scope** call, which turns on what class of artifact this is rather than how well it works. Not
sufficient for any positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Fourteen rows were disposed in this pass as product-facing frameworks and
platforms; this one was checked against the same bar and **passes it**.

The distinction is which side of the agent the interface sits on. Everything SKIPped here builds the
UI of an application *you ship to end users*. This builds a UI for driving a **coding agent** — its own
description is "the best way to use **Hermes Agent** from the web or from your phone". That is
squarely in the dev loop, and the catalog already carries the same shape in `happy`, the mobile client
row its overlaps cell names.

Worth recording because the pattern recurs: "agent" appears in almost every row in this slice and
means something different in half of them. The same care was needed for "sandbox" (`arrow-js` vs
`sandcastle`) and "MCP" (`mcp-ui` vs the MCP Servers category). A scope pass that pattern-matched
vocabulary rather than reading direction would have disposed this row.

What it actually needs is a look at whether a phone-driven coding agent is useful in practice, which is
measurement, not triage.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hermes-webui](https://github.com/nesquena/hermes-webui) | platform | Web/mobile UI for the Hermes Agent harness (MIT) — drive a self-hosted agent from browser or phone | Want to use a self-hosted agent harness from a browser or phone, not just the CLI | Hermes Agent, happy, claudian |
