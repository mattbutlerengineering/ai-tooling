# Evaluation: strands-agents (harness-sdk)

**Repo:** [strands-agents/harness-sdk](https://github.com/strands-agents/harness-sdk)
**Stars:** 6,794 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Implement (harness construction)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An open-source SDK for building an agent harness end-to-end, in Python and TypeScript, across any model and any cloud.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: the GitHub repository description and
metadata (fetched 2026-08-04) plus the `CATALOG.md` one-liner and "Overlaps with" cell. Enough to
place and band it; not enough for any verdict, and none is offered.

## Triage note

Twenty-one rows in this slice were SKIPped as app-building frameworks with no dev-loop bridge, per `WORKFLOW.md`'s **Tools Deliberately Excluded** rule and the `langchain` precedent. This row was **not**, and the reason is specific rather than generous.

Its own description is "**Build an agent harness and control it end-to-end**" — and *harness-building*
is precisely the bridge the `langchain` eval names as an exception. `vercel/ai` was kept at
`discovery-log` in this same pass because `ToolLoopAgent` is "a documented substrate for building a
coding harness"; a whole SDK whose stated purpose is that substrate has at least as strong a claim.

Whether the claim survives contact is the open question, and it is a real one: an SDK for building
*any* agent harness is not the same as one for building a *coding* harness, and the difference is
exactly what separates the kept row from the twenty-one disposed ones. Settling it needs a read of
what the SDK actually exposes — measurement work, not a triage guess.

Left at `discovery-log` deliberately rather than by omission. A false SKIP here would remove the
catalog's clearest example of the exception that makes the scope bar a test instead of a ban.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [strands-agents (harness-sdk)](https://github.com/strands-agents/harness-sdk) | framework | Model-driven agent SDK (Apache-2.0, Python + TS) — build and control an agent harness end-to-end: agent loop, any model/cloud (Bedrock/Anthropic/OpenAI/Gemini), built-in context management, execution limits, hooks/steering, guardrails, MCP, and multi-agent patterns | Building production agents means hand-stitching the loop, providers, observability, and guardrails; want a controllable SDK that scales local→prod without rewrites | fastmcp, mcp-use, ruflo, phantom |
