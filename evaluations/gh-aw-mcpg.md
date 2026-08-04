# Evaluation: gh-aw-mcpg

**Repo:** [github/gh-aw-mcpg](https://github.com/github/gh-aw-mcpg)
**Stars:** 143 | **Last updated:** 2026-07-10 (pushed) | **License:** MIT
**Dev loop stage:** MCP Servers (gateway)
**Layer:** Infrastructure
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

An MCP gateway that brokers tool access for agentic workflows running inside GitHub Actions — the
runtime companion to GitHub's gh-aw workflow framework.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04) plus
the CATALOG one-liner and "Overlaps with" cell (`mcp-context-forge`, `bifrost`, `Portkey-gateway`).
Enough to place it; not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`, and it is a low-star row where the star count is close to meaningless:
★143 on a first-party GitHub repository published alongside a framework, not a community project
competing for adoption. Disposing it on size would be the error the `plumb-mcp` note in this same pass
warns about.

What makes it worth keeping is where it sits. Every other gateway row here — `mcp-context-forge`,
`bifrost`, `Portkey-gateway` — brokers MCP access for agents you run. This one brokers it for agents
running **inside CI**, which is a governance problem rather than a routing one: what may a workflow
reach, with whose credentials, audited how. That is the outer loop, and it is thinly covered.

The honest caveat is that its value is conditional on adopting `gh-aw` itself, so this is really a
question about that framework with the gateway as an implementation detail — the same
facet-of-a-larger-artifact shape found elsewhere in this slice.

No eval file existed before this pass; this stub is the placeholder, not an evaluation.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [gh-aw-mcpg](https://github.com/github/gh-aw-mcpg) | MCP server | GitHub Agentic Workflows MCP Gateway (MIT, official GitHub) — a gateway that brokers MCP tool access for agentic workflows running in GitHub Actions, the runtime companion to GitHub's gh-aw workflow framework | Running agents inside GitHub Actions need governed, CI-native access to MCP tools rather than ad-hoc per-workflow server wiring | mcp-context-forge, bifrost, Portkey-gateway |
