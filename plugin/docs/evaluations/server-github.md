# Evaluation: server-github (modelcontextprotocol reference GitHub server)

**Repo:** [modelcontextprotocol/servers-archived (src/github)](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github)
**Stars:** N/A (lives in `servers-archived`, an archived monorepo; the parent `servers` repo had ~87.4K stars at evaluation time but the GitHub server has been removed from it) | **Last updated:** Archived — no longer maintained | **License:** MIT
**Dev loop stage:** Plan / Ship (GitHub operations for agents: repos, issues, PRs, actions, search)
**Layer:** Tooling

---

## What it does

Catalog one-liner: "GitHub operations (repos, issues, PRs, actions)." It is an MCP server that exposes the GitHub API to an agent — `create_or_update_file`, repository management, issue/PR operations, and code/issue/user search — so an agent can act on GitHub beyond what local `git` allows.

The catalog entry `server-github` refers to the original `@modelcontextprotocol/server-github` reference implementation that historically shipped in `modelcontextprotocol/servers` under `src/github`. **That implementation is deprecated.** It has been moved out of the active `servers` repo into `modelcontextprotocol/servers-archived` (a repo whose GitHub description is literally "Reference MCP servers that are no longer maintained" and whose `archived` flag is `true`). Its README opens with: *"Deprecation Notice: Development for this project has been moved to GitHub in the http://github.com/github/github-mcp-server repo."* In other words, `server-github` is the superseded predecessor of `github-mcp-server`, which is already a separate entry in CATALOG.md and is the one listed in STACK.md.

## How we tested it

**Evidence:** REVIEW

Method: inspected the upstream repositories via `gh api` (GitHub REST API). I did **not** install or run the server — this is a repo/deprecation-status investigation, not a hands-on runtime evaluation. All findings below are read directly from the live API responses, not paraphrased from memory.

```
# 1. Active servers repo no longer contains a github server
gh api repos/modelcontextprotocol/servers/contents/src --jq '.[].name'
#  -> everything, fetch, filesystem, git, memory, sequentialthinking, time  (no "github")
gh api repos/modelcontextprotocol/servers/contents/src/github
#  -> 404 Not Found

# 2. The servers README lists GitHub under "now archived" pointing to servers-archived
gh api repos/modelcontextprotocol/servers/contents/README.md --jq '.content' | base64 -d
#  -> "**[GitHub](.../servers-archived/tree/main/src/github)** - Repository management..."

# 3. The archived server's own README carries the deprecation notice
gh api repos/modelcontextprotocol/servers-archived/contents/src/github/README.md --jq '.content' | base64 -d
#  -> "Deprecation Notice: Development for this project has been moved to
#      GitHub in the http://github.com/github/github-mcp-server repo."
gh api repos/modelcontextprotocol/servers-archived --jq '{archived, description}'
#  -> {"archived": true, "description": "Reference MCP servers that are no longer maintained"}

# 4. The successor is the one already in the catalog + STACK
gh api repos/github/github-mcp-server --jq '{stars, description, archived, license, lang}'
#  -> {"stars": 30818, "description": "GitHub's official MCP Server",
#      "archived": false, "license": "MIT", "lang": "Go"}
```

## What worked

- The deprecation chain is unambiguous and self-documenting: active repo (server removed) -> README "now archived" pointer -> archived repo (`archived: true`) -> server README deprecation notice naming the exact successor. No guesswork required.
- The successor it points to, `github/github-mcp-server`, is healthy and first-party: ~30.8K stars, MIT, Go, actively pushed (commit activity same day as evaluation), and already covered in the catalog (CATALOG.md line 273) and STACK.md (line 33).

## What didn't work or surprised us

- `server-github` is a near-duplicate / superseded entry. The catalog already carries `github-mcp-server` as a distinct row, and the two rows already cross-reference each other in their "Overlaps with" columns — but neither row flags that `server-github` is the *deprecated, archived predecessor* of the other. A reader could reasonably install the wrong one.
- This mirrors the rename/duplicate situations previously flagged in the catalog (e.g., ECC / GSD rename-dups): two entries that are really one tool across a maintenance handoff, not two independent options.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | - | Archived/unmaintained code accrues API drift against GitHub's evolving API; the successor gets the fixes. |
| Speed | neutral | Functionally similar surface to the successor; no speed advantage to justify the older server. |
| Maintainability | - | Repo is `archived: true`, "no longer maintained" — adopting it is taking a dependency on dead code. |
| Safety | - | No ongoing security maintenance on an archived reference server; the first-party successor is the safer dependency. |
| Cost Efficiency | neutral | Not a differentiator versus the successor. |

## Verdict

**SKIP (deprecated / superseded — use `github-mcp-server` instead)**

`server-github` is the original `@modelcontextprotocol/server-github` reference implementation, which has been **deprecated and archived**. Its own README and the parent repo both redirect development to `github/github-mcp-server` — GitHub's official MCP server, which is already a separate catalog entry and the one listed in STACK.md. There is no reason to adopt `server-github`: it is dead code that points at the entry the catalog already recommends.

Recommendation for the catalog (not applied here — instructed not to edit CATALOG.md/COMPARISON.md): mark the `server-github` row as **deprecated/superseded**, annotating it as the archived predecessor of `github-mcp-server` (analogous to the ECC/GSD rename-dup handling), or merge it into the `github-mcp-server` entry. Keep `github-mcp-server` as the canonical GitHub MCP entry.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [server-github](https://github.com/modelcontextprotocol/servers-archived/tree/main/src/github) | MCP server | DEPRECATED/ARCHIVED — original reference GitHub MCP, superseded by github-mcp-server | (Historical) agent GitHub operations — now use the first-party successor | github-mcp-server (this is its archived predecessor) |
