# Evaluation: GitHub MCP Server

**Repo:** [github/github-mcp-server](https://github.com/github/github-mcp-server)
**Stars:** 30,769 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan, Ship
**Layer:** Tooling

---

## What it does

GitHub's official MCP server providing full API coverage for repositories, issues, pull requests, code search, file content retrieval, actions, and organization management. Agents call MCP tools to interact with GitHub without needing the `gh` CLI.

## How we tested it

**Evidence:** REVIEW

**README/install review — not run hands-on.** Note the install: an earlier draft showed `npx @github/mcp-server`, which does not exist (no such npm package). GitHub ships this as a **remote hosted HTTP server** and as a local Go binary / Docker image — there is no npx entry point. The correct ways to add it:

```bash
# Remote hosted (easiest): GitHub-managed, OAuth/PAT auth
claude mcp add --transport http github https://api.githubcopilot.com/mcp/

# Local (self-hosted): Go binary or Docker
docker run -i --rm -e GITHUB_PERSONAL_ACCESS_TOKEN ghcr.io/github/github-mcp-server
```

Capabilities below are drawn from the official repo/README (toolsets for repos, issues, PRs, actions, code search), not from an observed session.

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

**ADOPT** (review-based)

The official, GitHub-maintained server with broader coverage than the community alternative; the code-navigation toolset (cross-repo search, read file at a specific ref) justifies it over server-github. For basic issue/PR operations, `gh` CLI via the bash tool is equivalent, so the MCP earns its place mainly for cross-repo search and advanced PR workflows. Verdict is on merits + official status, not a recorded run here — install via the hosted `https://api.githubcopilot.com/mcp/` endpoint, not the non-existent `npx @github/mcp-server`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [github-mcp-server](https://github.com/github/github-mcp-server) | MCP server | GitHub's official MCP server — repos, issues, PRs, actions, search, code navigation | Need first-party GitHub integration with full API coverage and official support | server-github |
