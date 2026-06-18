# Evaluation: GitHub MCP Server

**Repo:** [github/github-mcp-server](https://github.com/github/github-mcp-server)
**Stars:** 30,769 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan, Ship
**Layer:** Tooling

---

## What it does

GitHub's official MCP server providing full API coverage for repositories, issues, pull requests, code search, file content retrieval, actions, and organization management. Agents call MCP tools to interact with GitHub without needing the `gh` CLI.

## How we tested it

Added the GitHub MCP server to Claude Code with a personal access token. Used it for repository search, issue creation and management, PR operations, and cross-repo code navigation.

```bash
claude mcp add github-mcp-server -- npx @github/mcp-server
```

Tested against three repos: a public open-source project (issue triage), a private repo (PR review and code search), and cross-repo code search to find usage patterns.

## What worked

- More complete API coverage than the community server-github — supports code search, file content at specific refs, and advanced PR operations (review comments, merge methods)
- Code navigation features are unique: search across repos by language, file path patterns, and content — `server-github` doesn't offer this
- Auth via GitHub personal access token — simple setup, no OAuth dance
- First-party support means it tracks GitHub API changes quickly

## What didn't work or surprised us

- Adds ~20 tools to the agent's context, which is a lot — increases prompt size and can confuse tool selection on simpler models
- Some operations overlap with `gh` CLI that's already available in Claude Code's bash tool — the MCP version doesn't add value for basic `gh issue list` type commands
- Rate limiting follows your PAT's limits — heavy use in parallel agent sessions can exhaust the quota
- No webhook support — can't subscribe to events, only poll

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same GitHub API data as `gh` CLI |
| Speed | + | Code search across repos is faster than manual `gh api` queries |
| Maintainability | neutral | No impact on code quality |
| Safety | neutral | Operates within PAT permission scope |
| Cost Efficiency | neutral | Token overhead from 20 tools in context |

## Verdict

**ADOPT**

The official server with broader coverage than the community alternative. The code navigation features — search across repos, read file at specific ref — justify the switch from server-github. For basic issue/PR operations, `gh` CLI via bash is equivalent, but for cross-repo search and advanced PR workflows, this is the better tool.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [github-mcp-server](https://github.com/github/github-mcp-server) | MCP server | GitHub's official MCP server — repos, issues, PRs, actions, search, code navigation | Need first-party GitHub integration with full API coverage and official support | server-github |
