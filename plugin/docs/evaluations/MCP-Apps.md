# Evaluation: MCP Apps (ext-apps)

**Repo:** [modelcontextprotocol/ext-apps](https://github.com/modelcontextprotocol/ext-apps)
**Stars:** 2,552 | **Last updated:** 2026-07-08 (pushed) | **License:** NOASSERTION
**Dev loop stage:** Reference (MCP extension)
**Layer:** Process
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

The specification and SDK for MCP Apps — the extension that lets an MCP server serve interactive UI
embedded in an AI chat host rather than returning text and structured data only.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this — it is a spec plus SDK. Source-grounded only: GitHub metadata
(fetched 2026-08-04) plus the CATALOG one-liner and "Overlaps with" cell (`ag-ui`, `openui`,
`a2ui`). Enough to place it; not enough for any verdict, and none is offered.

## Triage note

Left at `discovery-log`, and the provenance is the reason: this lives in the
**`modelcontextprotocol` org itself**. It is not a third-party proposal competing with the protocol
this catalog's entire MCP Servers category rests on — it is an official extension to it.

That makes the "Overlaps with" banding misleading. `ag-ui` and `openui` are independent standards
solving adjacent problems; `ext-apps` is the first-party answer for MCP specifically, so its
relevance is decided by whether MCP wins, not by whether it beats them.

★2.6K is small in absolute terms and large for a spec repo weeks into its life. The licence resolves
to `NOASSERTION` — GitHub cannot parse the LICENSE file, which for an official protocol repo almost
certainly means an unusual file layout rather than an absent grant, and is worth confirming before
anything here is vendored.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [MCP Apps (ext-apps)](https://github.com/modelcontextprotocol/ext-apps) | reference | Spec + SDK for MCP Apps — MCP servers serve interactive UI embedded in AI chat hosts (★2K) | No standard way for MCP tools to ship their own UI into a host like ChatGPT/Claude | ag-ui, openui, a2ui |
