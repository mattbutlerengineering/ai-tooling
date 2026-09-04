# Evaluation: groundhog

**Repo:** [dmytrome/groundhog](https://github.com/dmytrome/groundhog)
**Stars:** 0 | **Last updated:** recent (exact push date not captured from the repo page; checked 2026-09-04) | **License:** MIT
**Last verified:** 2026-09-04
**Last triaged:** 2026-09-04  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Self-hosted web research for agents via a real stealth-patched Chrome instead of a basic HTTP fetcher. Finds pages, extracts clean content, strips hidden text before a model reads it, and returns provenance receipts for sources.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. Source-grounded only, from the repo's own README description. Not enough for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log`. Zero overlap pressure (P3 backlog). Adjacent to `browser-use`/`firecrawl-mcp`/`ref-tools-mcp`, but the stealth-Chrome-plus-provenance-receipt angle is a real, if unverified, differentiator (sites that block plain fetchers, source attribution for claims). Brand new (★0); leaving for a real eval.

_Triaged 2026-09-04 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [groundhog](https://github.com/dmytrome/groundhog) | MCP server | Self-hosted web research for agents (MIT) via a real stealth-patched Chrome — finds pages, extracts clean content, strips hidden text, and returns provenance receipts for sources | Basic HTTP fetchers get blocked or return junk on real sites; want browser-grade web research with source provenance over MCP | browser-use, firecrawl-mcp, ref-tools-mcp |
