# Evaluation: Cloudflare MCP Server

**Repo:** [cloudflare/mcp-server-cloudflare](https://github.com/cloudflare/mcp-server-cloudflare)
**Stars:** 3,878 | **Last updated:** pushed 2026-06-08 (created 2024-11-27) | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Ship (deploy/operate Cloudflare infra from agent sessions) — with Verify/Reflect use (observability, logs, analytics)
**Layer:** Infrastructure (managed remote MCP servers fronting Cloudflare's account APIs)

---

## What it does

Catalog one-liner: *Cloudflare integration: workers, builds, bindings, observability.* The mechanism: this repo is not one server but a **fleet of ~13 official, Cloudflare-hosted remote MCP servers**, each scoped to a product area and reached at a distinct `*.mcp.cloudflare.com/mcp` URL over `streamable-http` (with deprecated `sse` fallback). You point an MCP client (Claude, Cursor, etc.) at the URL for the area you care about, authenticate against your Cloudflare account, and the agent can read configs, query analytics/logs, and make changes via natural language.

The included servers cover: Documentation (up-to-date Cloudflare reference), Workers Bindings (build Workers apps with storage/AI/compute primitives), Workers Builds (CI insight/management), Observability (logs + analytics debugging), Container/sandbox (spin up a dev environment), Browser Rendering (fetch pages → markdown, screenshots), Logpush (job health), AI Gateway (search prompt/response logs), Audit Logs, DNS Analytics, Digital Experience Monitoring, Cloudflare One CASB (SaaS security misconfig detection), and a GraphQL analytics server. Each is a separate connection — you wire up only the ones you need.

A second, newer official server lives in the companion repo **[`cloudflare/mcp`](https://github.com/cloudflare/mcp)** (559 stars, created 2026-01-29, Apache-2.0, `https://mcp.cloudflare.com/mcp`): the **Code Mode** server. Instead of registering ~2,500 Cloudflare API endpoints as individual tools (~244k tokens even with minimal schemas), it exposes just three tools — `docs`, `search`, `execute` — and the agent writes JavaScript to query the OpenAPI spec and call `cloudflare.request()`. The spec stays server-side; only execution results return to the agent (~1.1k tokens of tool surface). The README in `mcp-server-cloudflare` explicitly frames the two as complementary: **Code Mode** (`cloudflare/mcp`) for broad cross-API coverage via code execution; **domain-specific servers** (this repo) for curated, typed tools in one product area.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I verified repository identity and read the primary artifacts via the GitHub API and README. I did not connect a Cloudflare account, add any server to an MCP client, or invoke a tool. Therefore no latency, tool-call-success, or token-cost-in-practice metrics appear below — none are invented (the token figures cited are Cloudflare's own published comparison table from the `cloudflare/mcp` README, not my measurements).

The catalog name "cloudflare-mcp" is ambiguous — `gh search repos cloudflare mcp` returns several candidates including an unofficial `mattzcarey/cloudflare-mcp` (129 stars). The catalog already links to the official **`cloudflare/mcp-server-cloudflare`**, which the search and metadata confirm is the established Cloudflare-org hub (3,878 stars, Apache-2.0, actively pushed). The link is correct and live; this is not the broken/unlinked case it was flagged as. The newer `cloudflare/mcp` (Code Mode) is a genuinely distinct companion, not a rename.

```bash
gh search repos cloudflare mcp --limit 15 --json fullName,stargazersCount,description,url
gh api repos/cloudflare/mcp-server-cloudflare --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed_at,created_at,open_issues:.open_issues_count,archived,language}'
gh api repos/cloudflare/mcp --jq '{stars,license,homepage,created_at,pushed_at}'
gh api repos/cloudflare/mcp-server-cloudflare/readme --jq '.content' | base64 -d   # full README
gh api repos/cloudflare/mcp/readme --jq '.content' | base64 -d                      # Code Mode README
grep -inE "cloudflare" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Official, first-party, and current.** Cloudflare-org owned, Apache-2.0, created Nov 2024, pushed within the eval week. This is the canonical Cloudflare MCP offering, not a third-party wrapper — important because it touches production infra credentials.
- **Managed remote servers, near-zero setup.** The servers are hosted by Cloudflare at stable `*.mcp.cloudflare.com/mcp` URLs; you add a URL and OAuth into your account rather than running and maintaining a local binary. For clients without remote-server support, `mcp-remote` bridges it.
- **Broad, genuinely useful operational coverage for the Ship/Verify loop** — Workers bindings/builds, observability logs+analytics, DNS analytics, audit logs, browser rendering, AI Gateway log search. This spans deploy, debug, and review of Cloudflare-hosted apps.
- **The Code Mode companion is a real context-cost innovation.** Fronting ~2,500 endpoints with 3 code-execution tools (~1.1k tokens vs ~244k for native minimal schemas, per Cloudflare's table) directly addresses MCP tool-definition context bloat — the same class of problem several catalog entries target.
- **Scoped credentials per server.** OpenAI Responses-API usage and token setup are documented per-server with only the scopes that server needs (e.g. Browser Rendering token), encouraging least-privilege.

## What didn't work or surprised us

- **It's a fleet, not "a server."** The catalog one-liner ("workers, builds, bindings, observability") names four of ~13 servers. Each is a separate connection/auth; there's no single "Cloudflare MCP" you turn on. Picking and wiring the relevant subset is real configuration work.
- **Two official products under one fuzzy name.** "cloudflare-mcp" could mean the domain-specific hub (this repo) *or* the Code Mode server (`cloudflare/mcp`). They have different tradeoffs (typed/curated vs broad/code-execution). A catalog reader needs to know both exist.
- **Hard niche gate.** Value is exactly zero for anyone not on Cloudflare. This is infrastructure for Cloudflare accounts specifically — not a general dev-loop tool.
- **Write access to production infra is the standing risk.** These servers can *make changes* (create KV namespaces, add DNS records, manage Workers). An agent with a write-scoped token can mutate live production config. Scope tokens narrowly and treat write-capable servers with caution.
- **Documented context-blowup on chatty servers.** The README itself warns the observability server can chain many tool calls and hit Claude's context limit ("response was interrupted"), advising small, specific queries — a real usability footgun.
- **Some features require a paid Workers plan** (noted in README); not everything works on a free account.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agent reads real account config, logs, and analytics instead of guessing; Documentation server grounds answers in current Cloudflare reference. |
| Speed | + | Deploy/debug/inspect Cloudflare infra in natural language from the agent session instead of context-switching to dashboard or wrangler CLI. |
| Maintainability | neutral | Managed hosted servers mean nothing to maintain locally, but you must wire/auth each relevant server; no effect on your own codebase's maintainability. |
| Safety | − / + | Write-scoped tokens let an agent mutate production infra (DNS/Workers/KV) — real blast radius; mitigated by per-server least-privilege scopes and read-only token options. |
| Cost Efficiency | + | Code Mode server slashes tool-definition context cost (~1.1k vs ~244k tokens, per Cloudflare); servers themselves are free, though some features need a paid Workers plan. |

## Verdict

**CONDITIONAL**

The Cloudflare MCP servers are mature, official, and genuinely capable, but their value is entirely gated on being a Cloudflare user — so they cannot be ADOPT-everywhere. **Adopt conditionally when you operate apps on Cloudflare (Workers, Pages, DNS, R2/KV/D1) and want to deploy, debug, and inspect that infra from agent sessions.** In that case, wire up only the domain-specific servers you need (observability, bindings, builds, DNS analytics), scope tokens to least privilege, and prefer read-only tokens unless the agent genuinely needs to make changes. Consider the companion **Code Mode** server (`cloudflare/mcp`) when you want broad cross-API coverage at minimal context cost rather than a curated per-product tool set. Not SKIP — for Cloudflare shops this is the canonical, first-party way to give agents account access, and the Code Mode context-efficiency work is best-in-class. It overlaps with `awslabs/mcp` only as the analogous offering for a different cloud (complementary, not competing).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cloudflare-mcp](https://github.com/cloudflare/mcp-server-cloudflare) | MCP server | Official fleet of ~13 hosted Cloudflare MCP servers (Workers bindings/builds, observability, DNS analytics, audit logs, browser rendering, AI Gateway, CASB) plus a companion Code Mode server (`cloudflare/mcp`) exposing ~2,500 API endpoints via 3 code-execution tools at ~1k tokens (3.9K stars) | Cloudflare users need agents to deploy, debug, and inspect their Workers/Pages/DNS/R2/KV infra in natural language from the session — and to do it without leaking a 244k-token tool surface | awslabs/mcp (complementary: same job for AWS) |
