# Evaluation: Firecrawl MCP Server (firecrawl-mcp)

**Repo:** [firecrawl/firecrawl-mcp-server](https://github.com/firecrawl/firecrawl-mcp-server)
**Stars:** 6,629 | **Last updated:** 2026-06-19 (pushed) | **License:** MIT
**Dev loop stage:** Research/Discovery (gathering web content) — touches Plan when scraping docs/data to ground a task
**Layer:** Tooling (retrieval layer; the default cloud path is Infrastructure-adjacent — a remote paid API)

---

## What it does

Web scraping and crawling — the official MCP server for [Firecrawl](https://github.com/firecrawl/firecrawl), turning live web pages into clean, agent-ready Markdown/structured data. The mechanism: the MCP server is a thin client that forwards tool calls to the Firecrawl API (cloud by default, or a self-hosted instance via `FIRECRAWL_API_URL`), which does the heavy lifting — browser rendering, JS execution, content cleaning, and conversion to LLM-friendly formats. It exposes roughly a dozen tools spanning the full extraction surface:

- `firecrawl_scrape` — single URL → clean Markdown/structured content (the workhorse).
- `firecrawl_batch_scrape` / `firecrawl_check_batch_status` — many URLs asynchronously, polled by ID.
- `firecrawl_map` — discover all URLs on a site (sitemap-style).
- `firecrawl_search` / `firecrawl_search_feedback` / `firecrawl_feedback` — web search with optional content scraping of results; search costs 2 credits, feedback refunds 1.
- `firecrawl_crawl` / `firecrawl_check_crawl_status` — recursive multi-page crawl, async with job IDs.
- `firecrawl_extract` — schema-driven structured extraction (LLM-backed) from one or more pages.
- `firecrawl_agent` / `firecrawl_agent_status` — autonomous "deep research" agent that searches, follows links, and gathers data, returning a job ID to poll.

Notable operational features baked into the server (not just the API): automatic retries with exponential backoff (`FIRECRAWL_RETRY_*`), rate-limit handling, and credit-usage monitoring with configurable warning/critical thresholds (`FIRECRAWL_CREDIT_WARNING_THRESHOLD` / `_CRITICAL_THRESHOLD`). Transports include stdio (default), Streamable HTTP, and SSE. Auth is via `FIRECRAWL_API_KEY` (`fc-…`) or OAuth bearer access tokens (`fco_…`).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, no MCP client connected, no Firecrawl API call issued.** Evidence was gathered from the GitHub repo: metadata via `gh api` (stars, license, push date, creation date, open issues, tags) and a full read of the README, including the "Available Tools" section, the Configuration/Environment-Variables section, and the Claude Desktop / VS Code / Cursor setup blocks. I confirmed the tool inventory (scrape, batch_scrape, map, search, crawl, extract, agent and their status/feedback companions), the API-key requirement for the cloud default, the documented self-host path (`FIRECRAWL_API_URL`), the credit-monitoring and retry env vars, and the released version tags (`v3.2.1` latest). **No web page was scraped, no credits were spent, no setup was verified hands-on, and the "deep research agent" capability is a vendor claim cited from the README, not reproduced.** Pricing tiers were not fetched live and are not quoted; the only cost facts asserted here are the credit-cost relationships stated in the README itself (e.g., search = 2 credits). No metrics below are invented.

```bash
gh api repos/firecrawl/firecrawl-mcp-server --jq '{stars,license,description,pushed_at,forks,created_at,open_issues,language}'
gh api repos/firecrawl/firecrawl-mcp-server/readme --jq '.content' | base64 -d
gh api repos/firecrawl/firecrawl-mcp-server/tags --jq '.[0:5][].name'   # v3.2.1 latest
# Catalog overlap scan:
grep -niE "exa-mcp|firecrawl|playwright|web scrap|crawl" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Covers the whole extraction surface, not just "fetch a URL."** Scrape, recursive crawl, sitemap mapping, batch, schema-driven structured extraction, and web search are all first-class. For "go read these docs / pull this data into the task," that breadth is exactly the dev-loop need.
- **Clean, agent-ready output is the core value.** Firecrawl renders JS, strips chrome, and returns Markdown/structured data, so the agent doesn't drown in raw HTML — the recurring failure mode of naive fetch tools on modern, JS-heavy sites.
- **Schema-driven `firecrawl_extract`** lets the agent ask for typed fields rather than re-parsing prose, which is the right design for turning a page into usable data.
- **Operational maturity in the server itself:** built-in retries with backoff, rate-limit handling, and credit-usage monitoring with thresholds — uncommon polish for an MCP wrapper, and directly relevant to a metered paid API.
- **Genuine self-host escape hatch.** `FIRECRAWL_API_URL` points the server at a self-hosted Firecrawl instance; the API key becomes optional. This removes both the per-credit cost and the third-party-dependency objection for teams willing to run the (open-source) engine.
- **Strong adoption and release discipline.** 6.6K stars, 770 forks, official vendor maintenance, semver-tagged releases (`v3.2.1`), and broad client coverage (Cursor, Claude Desktop, VS Code, Windsurf, Smithery). Pushed the same day as this evaluation.

## What didn't work or surprised us

- **The default path is a paid, metered cloud API.** Cloud usage requires `FIRECRAWL_API_KEY` and consumes credits per operation (search explicitly costs 2). This is real, ongoing friction versus zero-cost grounding tools — every scrape/crawl/extract spends money, and crawl/agent jobs can spend a lot.
- **Credit anxiety is designed into the UX.** The server ships warning/critical credit thresholds and a search-feedback refund mechanic (refund 1 of 2 credits, capped per team per day) — useful, but a tell that cost management is a live concern users must actively manage.
- **Overlaps two catalog neighbors, not one.** It overlaps `exa-mcp-server` on `firecrawl_search` (both do paid-API web search) AND overlaps `playwright`/`agent-browser`/`browser-use` on the "interact with pages" / scrape axis. It's a broad tool that straddles search and browser-automation categories.
- **124 open issues.** Healthy for a 6.6K-star project but indicates real rough edges; not triaged here.
- **No Claude Code-specific setup block.** The README documents Cursor, Claude Desktop, VS Code, and Windsurf. Claude Code is a standard stdio MCP add (`claude mcp add` with `FIRECRAWL_API_KEY`), but this was not confirmed hands-on.
- **Self-hosting is non-trivial.** The escape hatch exists, but running the Firecrawl engine (browser pool, queues) is real infrastructure — most users will default to the paid cloud.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Clean, JS-rendered, structured extraction grounds the agent in actual current web content (docs, data) instead of stale training memory or broken raw-HTML parsing. Bounded by the target site's quality and Firecrawl's render fidelity. |
| Speed | + | One tool call returns agent-ready Markdown/structured data; batch + async crawl handle bulk without the human pasting pages. Cloud round-trips and async polling add latency for large jobs. |
| Maintainability | neutral | Current scraped facts age better than hardcoded assumptions, but adds a metered external dependency (or self-hosted infra) to the toolchain. |
| Safety | neutral / - | Read-only web access (no push/exec). New exposure: scraped URLs and (cloud) queries pass through a third-party service, and an API key/credit balance is a managed secret/cost surface. Self-host removes the third-party hop. |
| Cost Efficiency | - | Default cloud path spends credits per operation (search = 2); crawl/agent jobs can be expensive. Mitigated by self-hosting (compute cost instead) or by reserving it for when free tools can't get clean content. |

## Verdict

**CONDITIONAL**

Firecrawl MCP is a mature, well-maintained, official MCP server that solves a real dev-loop problem — getting clean, agent-ready content out of modern JS-heavy web pages — with unusually broad coverage (scrape, crawl, map, batch, schema extraction, search, deep-research agent) and genuine operational polish (retries, rate limiting, credit monitoring). The decisive trade-off is cost: the default path is a paid, metered cloud API where every operation spends credits, which is real friction next to zero-cost grounding tools. **Adopt it per-project when the task genuinely needs robust extraction from JS-rendered or anti-scraping sites and simpler/free tools fall short — and seriously consider the self-host path (`FIRECRAWL_API_URL`) for teams doing this at volume, which removes both the per-credit cost and the third-party dependency.** Versus [exa-mcp-server](https://github.com/exa-labs/exa-mcp-server) the two are complementary, not redundant: Exa is search-first (find current information across the web); Firecrawl is extraction-first (turn specific known pages/sites into clean data), with web search as a secondary feature. For "ground the agent in *this* documentation site or scrape *this* data," reach for Firecrawl; for "search the web for current info," reach for Exa. Not ADOPT-everywhere because of the paid-API friction and overlap with both search and browser-automation tools; not SKIP because the clean-extraction value and maturity are concrete and unmatched on the extraction axis in the catalog.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [firecrawl-mcp](https://github.com/firecrawl/firecrawl-mcp-server) | MCP server | Official MCP server for Firecrawl — scrape, crawl, map, batch, schema-extract, and search the live web into clean agent-ready Markdown/structured data; cloud (paid, metered) or self-hosted | Agent needs clean, structured content extracted from modern JS-heavy web pages/sites (docs, data) rather than raw HTML | exa-mcp-server (complementary: exa = search-first, firecrawl = extraction-first). Adjacent: playwright, agent-browser, browser-use (page interaction/scrape) |
