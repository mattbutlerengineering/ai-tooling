# Evaluation: jevcrawl

**Repo:** [RayenMlayeh/jevcrawl](https://github.com/RayenMlayeh/jevcrawl)
**Stars:** 72 | **Last updated:** not verified (pushed date not fetched this pass) | **License:** Apache-2.0
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server and CLI web crawler that scores links and passages so an agent reads only the
answer, not whole pages — requires a Jev API key. The README claims it finds the answer page
2x more often than Crawl4AI and costs 10x less per answer than letting Claude crawl directly
(benchmarked against 50 tasks on 2026-10-12 and 20 different tasks on 2026-10-13, per the repo's
own figures — not independently verified here).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool, and did not independently verify its benchmark claims.
Source-grounded only: the public GitHub repo page (description, star count, license) plus the
CATALOG one-liner and "Overlaps with" cell.

## Triage note

Left at `discovery-log`. Its "Overlaps with" cell (`firecrawl-mcp`, `exa-mcp-server`, `groundhog`)
names catalog peers, not STACK picks — no structural redundancy signal. It needs a paid Jev API
key, which the existing peers (`firecrawl-mcp`, `exa-mcp-server`) also require in some form, so
that alone isn't a reason to SKIP. The self-reported 2x/10x figures are exactly the kind of claim
this repo's token-savings/claim-drift detectors exist to catch once this graduates to a real eval —
not something a bulk pass can verify or credit.

_Triaged 2026-10-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jevcrawl](https://github.com/RayenMlayeh/jevcrawl) | MCP server | MCP server + CLI web crawler (Apache-2.0) scoring links/passages so an agent reads only the answer, not whole pages (needs a Jev API key) | Letting an agent crawl raw pages burns tokens on irrelevant text; want a crawler tuned for answer-finding, not full-page scraping | firecrawl-mcp, exa-mcp-server, groundhog |
