# Evaluation: jira (MCP server)

**Repo:** [sooperset/mcp-atlassian](https://github.com/sooperset/mcp-atlassian)
**Stars:** 5,422 | **Last updated:** 2026-06-18 (active) | **License:** MIT (not an official Atlassian product)
**Dev loop stage:** Plan (read tickets → scope work) and Ship (update status / close tickets); touches Reflect when summarizing what shipped
**Layer:** Tooling (team-workflow integration; connects the agent to a live Jira instance)

---

## What it does

One-liner from the catalog: "Jira issue tracking integration." The catalog entry was **UNLINKED**; this evaluation resolves it.

The canonical Jira MCP server is **`sooperset/mcp-atlassian`** — by a wide margin the most adopted (5,422 stars vs. the next candidate's 790), actively maintained (pushed 2026-06-18), and the one most install guides point to. It is a Python MCP server (run via `uvx mcp-atlassian`, Docker, or pip) that connects an agent to **both Jira and Confluence**, across **Cloud and Server/Data Center** deployments. It exposes ~72 tools; the load-bearing Jira ones are `jira_search` (JQL), `jira_get_issue`, `jira_create_issue`, `jira_update_issue`, and `jira_transition_issue` (status changes). The mechanism: the agent issues JQL or an issue key, the server calls the Atlassian REST API with your credentials, and returns issue fields / accepts writes — so the agent can read a ticket's description and acceptance criteria before coding, and move the ticket to Done after shipping.

**Authentication** spans the real-world spread: API token + username (Cloud), Personal Access Token (Server/Data Center), and OAuth 2.0. Configuration is environment-variable driven (`JIRA_URL`, `JIRA_USERNAME`, `JIRA_API_TOKEN`, plus Confluence equivalents) wired into the MCP client config block.

**Canonical-repo decision (stated honestly):** Two defensible candidates exist.
- **`sooperset/mcp-atlassian`** — community, MIT, 5,422 stars, self-hosted (uvx/Docker/pip), Cloud + Server/DC, API token / PAT / OAuth. **Recommended canonical.**
- **`atlassian/atlassian-mcp-server`** — Atlassian's *official* remote MCP server, Apache-2.0, 790 stars, created 2025-08, OAuth-based hosted endpoint. The "vendor-blessed" option, newer and lower-adoption, and Cloud-oriented (remote).

I am confident in recommending `sooperset/mcp-atlassian` as the catalog link: highest adoption, broadest deployment coverage (critical because many enterprises run Jira Server/DC, which the official remote server does not target), and it is the repo the ecosystem's setup guides resolve to. Teams that require an Atlassian-official, vendor-hosted, OAuth-only path should prefer `atlassian/atlassian-mcp-server`. Both are real; neither URL is fabricated (verified via `gh api`).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not connected to a live Jira instance.** Connecting would require real Atlassian credentials and a tenant, which were not used. Evidence comes from GitHub repo metadata, the full README, and the published tool surface for both candidate repos. No issues were read or written, so no throughput/latency metrics are claimed below. The calibration reference was `evaluations/pg-aiguide.md` (another domain-integration MCP scored CONDITIONAL).

```bash
gh search repos jira mcp --limit 20 --json fullName,description,stargazersCount,url
gh api repos/sooperset/mcp-atlassian --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed_at,open_issues,archived}'
gh api repos/atlassian/atlassian-mcp-server --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed_at,open_issues}'
gh api repos/sooperset/mcp-atlassian/readme --jq '.content' | base64 -d
```

## What worked

- **Directly serves the catalog's stated problem.** "Agent needs to read/update Jira tickets during development" maps 1:1 onto `jira_get_issue` / `jira_search` (read) and `jira_create_issue` / `jira_update_issue` / `jira_transition_issue` (update). The dev-loop value is concrete: pull a ticket's description + acceptance criteria into context at Plan, transition it to Done at Ship.
- **Broadest deployment coverage of any candidate.** Cloud *and* Server/Data Center (Jira v8.14+), which matters because many enterprise Jira tenants are self-hosted DC — the segment the official remote server does not serve.
- **Full auth spread:** API token (Cloud), PAT (Server/DC), and OAuth 2.0 — so it fits both individual-dev and managed-enterprise setups.
- **Strong maintenance and adoption signal:** 5,422 stars, MIT, pushed the day before evaluation, published to PyPI with a hosted docs site and `llms.txt`. Low-friction `uvx mcp-atlassian` install.
- **Complementary to github-mcp-server, exactly as the catalog notes:** Jira = issues/work-tracking, GitHub = code/PRs. A team using both gets ticket-aware coding (read the Jira story) plus code-aware shipping (open the PR) in one agent.

## What didn't work or surprised us

- **Niche by definition.** Zero value to any team that does not use Jira. This is the single biggest constraint on the verdict — utility is entirely conditional on the team's tracker being Jira.
- **Not an official Atlassian product.** The recommended repo is community-maintained (it says so in its own README). The official alternative exists but trades adoption and Server/DC coverage for vendor backing.
- **Live write access to a system of record = real safety surface.** `jira_update_issue` / `jira_transition_issue` let an agent mutate tickets other humans depend on. Scoping the API token's permissions and preferring read-only where possible is a genuine concern, unlike the read-only/no-DB pg-aiguide.
- **Large tool surface (72 tools).** Loading the full Jira+Confluence toolset adds nontrivial context and tool-choice noise; teams that only want issue read/update pay for Confluence tools they may not use.
- **Network + credential dependency.** Requires a reachable Atlassian instance and stored tokens — operational and secret-management overhead that a knowledge-only MCP does not incur.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Agent codes against the actual ticket (description, acceptance criteria, linked context) instead of a paraphrased prompt, reducing scope drift. |
| Speed | + | Removes manual copy-paste of ticket details into the prompt and manual status updates after shipping; tighter Plan→Ship loop. |
| Maintainability | neutral | Does not affect code structure; mild context cost from a 72-tool surface. |
| Safety | - (manageable) | Live write access to a shared system of record; mitigate with scoped/least-privilege API tokens and read-only use where possible. |
| Cost Efficiency | neutral / + | Saves human round-trips on ticket reading/updating; adds context tokens for the tool surface and operational cost of credential management. |

## Verdict

**CONDITIONAL**

A Jira MCP server is a genuine dev-loop aid — for teams that use Jira. Reading a ticket's description and acceptance criteria into the agent at Plan, and transitioning the ticket at Ship, is real work-tracking integration that tightens the loop and keeps the agent coding against the source of truth rather than a lossy prompt. But it is **niche by definition**: utility is entirely contingent on the team running Jira, so it cannot be ADOPT-everywhere, and it is not SKIP because for Jira teams the value is concrete and the tooling is mature. **Adopt it when your team tracks work in Jira and you want the agent ticket-aware** — pair it with github-mcp-server (Jira = issues, GitHub = code) for full Plan→Ship coverage. Use the recommended community repo `sooperset/mcp-atlassian` for the broadest deployment/auth coverage (especially Server/Data Center); choose `atlassian/atlassian-mcp-server` if you require an Atlassian-official, OAuth-only hosted server. Scope the API token to least privilege given the live write access to a shared system of record.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jira (mcp-atlassian)](https://github.com/sooperset/mcp-atlassian) | MCP server | MCP server connecting an agent to live Jira (and Confluence), Cloud + Server/DC, to read/search and create/update/transition issues | Agent needs to read/update Jira tickets during development instead of working from a lossy paraphrased prompt | github-mcp-server (complementary: Jira = issues, GitHub = code); official alternative `atlassian/atlassian-mcp-server` |
