# Evaluation: confluence (mcp-atlassian)

**Repo:** [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)
**Stars:** 5,422 | **Last updated:** 2026-06-18 (latest release v0.21.1, 2026-04-10) | **License:** MIT
**Dev loop stage:** Plan / Reflect (read team docs into context up front; write findings/runbooks back out) — touches Implement when a spec lives on the wiki
**Layer:** Infrastructure (network connector to a live external system — the team's Confluence instance)

---

## What it does

The catalog lists "confluence" as a standalone MCP server: "Confluence wiki integration" for when an "agent needs to read/write team documentation." There is no single canonical "confluence-only" server with the maturity to match that one-liner — the dominant, best-maintained implementation is **`sooperset/mcp-atlassian`, a combined Confluence + Jira MCP server.** Confluence is one of its two product surfaces, not a separate project. (See "Catalog note" below — this is the **same repo** that backs the catalog `jira` entry.)

Mechanically, mcp-atlassian is a Python MCP server (installed via `uvx mcp-atlassian`, Docker, or pip) that authenticates to an Atlassian instance and exposes the Confluence REST API as MCP tools. For Confluence specifically, the key tools are:

- `confluence_search` — CQL (Confluence Query Language) search across spaces/pages
- `confluence_get_page` — fetch a page's content (returned as Markdown)
- `confluence_create_page` — create a new page
- `confluence_update_page` — edit an existing page
- `confluence_add_comment` — comment on a page

These are read **and** write: the agent can pull onboarding docs / architecture notes / specs into context, and can write generated documentation, runbooks, or summaries back to the wiki. The server supports Confluence Cloud (fully) and Server/Data Center v6.0+ (the same binary covers Jira Cloud and Jira Server/DC v8.14+). Across both products it ships **72 tools total**. Auth is flexible: API token (Cloud), Personal Access Token (Server/DC), or OAuth 2.0 for multi-user HTTP deployments. Transports include stdio (local IDE) and SSE / streamable-http (hosted multi-user).

Atlassian also ships an **official** remote MCP server ([atlassian/atlassian-mcp-server](https://github.com/atlassian/atlassian-mcp-server), Apache-2.0, ~790 stars), which also covers Jira + Confluence via a hosted remote endpoint with OAuth. It is the vendor-blessed option but newer and far less adopted than mcp-atlassian. See the verdict for when to prefer it.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not connected to a live Confluence instance.** This evaluation is honest about its method: no MCP server was run, no Confluence pages were read or written, and no tool-call latencies or success rates were measured. Connecting would require a real Atlassian instance and an API token, neither of which was used. Findings come from repo metadata, the canonical-repo selection search, and the project README (tool list, auth model, deployment compatibility matrix). No metrics below are invented.

```bash
# Canonical repo selection (which "confluence MCP" is real?)
gh search repos confluence mcp --limit 20 --json fullName,description,stargazersCount,url

# Metadata for the two serious candidates
gh api repos/sooperset/mcp-atlassian --jq '{stars:.stargazers_count,license:.license.spdx_id,desc:.description,pushed:.pushed_at,open_issues:.open_issues_count,archived:.archived}'
gh api repos/sooperset/mcp-atlassian/releases --jq '.[0] | {tag:.tag_name,published:.published_at}'
gh api repos/atlassian/atlassian-mcp-server --jq '{stars:.stargazers_count,license:.license.spdx_id,desc:.description,pushed:.pushed_at}'

# README: tools, auth, compatibility
gh api repos/sooperset/mcp-atlassian/readme --jq '.content' | base64 -d

# Confirm catalog jira + confluence are the same upstream repo
grep -inE "jira|confluence|atlassian|sooperset" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Clear canonical winner among community options.** Of ~20 "confluence mcp" results, mcp-atlassian (5,422 stars) dwarfs every alternative (next community Confluence-specific server is ~78 stars; most are <15-star single-author experiments). It is actively maintained (pushed 2026-06-18, released v0.21.1 2026-04-10), MIT-licensed, on PyPI with download badges, and has CI tests — the maturity the catalog one-liner implies.
- **Covers the exact catalog problem on both sides.** `confluence_get_page` / `confluence_search` satisfy "read team documentation"; `confluence_create_page` / `confluence_update_page` / `confluence_add_comment` satisfy "write." Pages come back as Markdown, which is the format an LLM handles best.
- **Broad deployment + auth coverage.** Confluence Cloud and Server/Data Center (v6.0+); API token, PAT, and OAuth 2.0; stdio and HTTP/SSE transports. This handles enterprise self-hosted Confluence, which most thin alternatives do not.
- **One server, both products.** Because it bundles Jira, a team already running it for Jira gets Confluence for free (and vice versa) — no second server to install or authenticate. 72 tools total across the two.
- **Low-friction Claude Code setup.** `uvx mcp-atlassian` with a handful of `CONFLUENCE_URL` / `CONFLUENCE_USERNAME` / `CONFLUENCE_API_TOKEN` env vars; documented for Claude Desktop and Cursor, and the same MCP config applies to Claude Code.

## What didn't work or surprised us

- **The catalog "confluence" entry is not a distinct project — it is one facet of mcp-atlassian, the same repo as the catalog `jira` entry.** Listing them as two independent rows overstates the inventory. They should be cross-referenced as two surfaces of one server (see Catalog note).
- **Write access to the team wiki is a real safety surface.** `create_page` / `update_page` let an agent mutate shared team documentation. An over-eager agent can edit the wrong page or clobber content. This is materially riskier than a read-only docs source, and the catalog one-liner ("read/write") understates it.
- **Network + credential dependency.** It needs a live Atlassian instance, a valuable API token (broad Confluence access), and network reachability. The token's blast radius is whatever the user account can see/edit in Confluence — there is no built-in per-page scoping in the token model.
- **301 open issues.** Healthy activity, but a non-trivial backlog typical of a popular community connector wrapping a large, frequently-changing vendor API. It is community-maintained ("Not an official Atlassian product").
- **Value is entirely conditional on the team using Confluence.** For a team on Notion / Google Docs / a docs-in-repo setup, this server is dead weight — zero value, plus an unnecessary credential to manage.
- **Not source-tested here.** Tool reliability, Markdown-conversion fidelity on complex pages (tables, macros, attachments), and CQL-search quality were not verified hands-on.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Pulls authoritative team docs (specs, conventions, runbooks) into the agent's context so generated code/plans match documented intent instead of guessing. |
| Speed | + | Removes manual copy-paste of wiki pages into the prompt; the agent fetches the page (`get_page`) or finds it (`search`) directly during Plan/Reflect. |
| Maintainability | neutral / + | Can keep docs current by writing summaries/runbooks back to the wiki — but write access also risks degrading shared docs if the agent edits carelessly. Net depends on guardrails. |
| Safety | - | Write tools mutate shared team documentation; requires a broad Confluence API token with no per-page scoping. Largest risk in this evaluation. |
| Cost Efficiency | neutral | Avoids human time spent shuttling docs into context; adds a tool surface + token to manage. Roughly net-neutral, value gated on actual Confluence usage. |

## Verdict

**CONDITIONAL**

mcp-atlassian is the right, well-maintained implementation behind the catalog "confluence" entry, and it cleanly solves the stated problem — read/write access to team documentation during Plan and Reflect. But the value is entirely conditional on **the team actually using Confluence**, and it carries a real safety cost: write tools mutate shared team docs and require a broad API token. **Adopt it for teams whose source of truth lives in Confluence** (especially enterprise Server/Data Center shops, where mcp-atlassian's deployment coverage beats every alternative), and prefer wiring it **read-first** — start with `confluence_search` / `confluence_get_page` and only enable page-write tools once you trust the agent's behavior and have a way to review its edits. Teams that want the vendor-supported path with managed OAuth should evaluate **atlassian/atlassian-mcp-server** (official, Apache-2.0) instead, accepting its much smaller adoption and hosted-remote model. **Not ADOPT-everywhere** because it is dead weight for non-Confluence teams and adds a write surface to a shared system. **Not SKIP** because for a Confluence-centric team it is a genuine, low-friction context win.

## Catalog note (do not edit CATALOG.md as part of this evaluation)

The catalog lists `confluence` and `jira` as two separate MCP-server rows. Both are **the same upstream repo** — `sooperset/mcp-atlassian`, a single combined Confluence + Jira server (72 tools total). They are two product facets of one install, not two independent tools. A future catalog edit should link both rows to `sooperset/mcp-atlassian` and note in each "Overlaps with" column that they share one binary (install one, get both). The existing complementary overlaps (`confluence` ↔ `gentleman-book-mcp`: team wiki vs. architecture book) remain valid and are orthogonal to this consolidation.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [confluence](https://github.com/sooperset/mcp-atlassian) | MCP server | Confluence wiki integration via mcp-atlassian (read/search/create/update pages, comments) — same binary also serves Jira; Cloud + Server/DC; API token / PAT / OAuth | Agent needs to read/write team documentation during Plan & Reflect | Same repo as catalog `jira` (one combined server, 72 tools); complementary to gentleman-book-mcp (confluence = team wiki, gentleman = architecture book) |
