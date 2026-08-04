# Evaluation: firecrawl

**Repo:** [firecrawl/firecrawl](https://github.com/firecrawl/firecrawl)
**Stars:** 148,503 | **Last updated:** 2026-07-10 (pushed) | **License:** AGPL-3.0
**Dev loop stage:** Research & Discovery (web ingestion)
**Layer:** Infrastructure
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

A scraping and crawling API that turns any URL into clean, LLM-ready Markdown at scale, with a
CLI, Python/JS SDKs and REST — the base tool behind `firecrawl-mcp`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`firecrawl-mcp`, `exa-mcp-server`, `webclaw`,
`Agent-Reach`). Enough to place it against its own MCP wrapper; not enough for a positive verdict,
and none is offered.

## Triage note

Left at `discovery-log`, and two things about it are worth recording rather than deciding.

**The AGPL does not dispose it.** P4 mechanical-skip scopes copyleft to *vendored* Types —
`skill` and `plugin`, whose text is copied into the consuming repo. firecrawl is a `tool` you run
behind an API; AGPL-3.0 imposes nothing on the code you write against it. This is precisely the
case CLAUDE.md names when it warns that a naive copyleft rule would SKIP the wrong rows. Self-hosting
a modified copy and offering it as a network service is where the licence bites, and that is not
this catalog's use.

**The relationship to `firecrawl-mcp` is layering, not duplication.** The MCP row is the agent-facing
wrapper; this row is the engine underneath. Both belong, and disposing either as redundant with the
other would misread the stack.

★148.5K and pushed today. Whether *any* general web-ingestion tool belongs in a dev-loop stack — as
opposed to being reached for during research — is the open question, and it applies equally to
`exa-mcp-server` and `webclaw`. That is a cluster call, not a per-row one.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [firecrawl](https://github.com/firecrawl/firecrawl) | tool | Web scraping/crawling API converting any URL to clean LLM-ready Markdown at scale — CLI, Python/JS SDKs, REST; the base tool behind firecrawl-mcp (AGPL-3.0) | Agents need clean, LLM-ready content from arbitrary sites at crawl scale, not raw HTML | firecrawl-mcp, exa-mcp-server, webclaw, Agent-Reach |
