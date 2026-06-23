# Evaluation: GitHub MCP Server

**Repo:** [github/github-mcp-server](https://github.com/github/github-mcp-server)
**Stars:** 30,891 | **Last updated:** 2026-06-22 (pushed) | **License:** MIT
**Last verified:** 2026-06-22
**Dev loop stage:** Plan, Ship
**Layer:** Tooling

---

## What it does

GitHub's official MCP server (written in **Go**) providing API coverage for repositories, issues, pull requests, code search, file content retrieval, actions, security, and organization management. Agents call MCP tools to interact with GitHub without shelling out to the `gh` CLI. It ships three ways: a local **stdio** server (the Homebrew/Go binary), a local **HTTP** server, and GitHub's hosted remote endpoint (`https://api.githubcopilot.com/mcp/`). The local binary reads a `GITHUB_PERSONAL_ACCESS_TOKEN` env var; tool enumeration (`tools/list`) is static and works before any authenticated call.

The tool surface is organized into **toolsets** (`repos`, `issues`, `pull_requests`, `actions`, `code_security`, `secret_protection`, `orgs`, `users`, etc.) that you enable selectively, plus a `--read-only` flag that filters the surface down to non-mutating tools.

## How we tested it

**Evidence:** MEASURED

**Ran hands-on** on 2026-06-22 (macOS arm64, macOS 26.3). Installed the native binary via **Homebrew** (`brew install github-mcp-server` → **v1.4.0**, build date 2026-06-17), then **drove the local `stdio` server with a real JSON-RPC handshake** (`initialize` → `notifications/initialized` → `tools/list` / `tools/call`) piped over stdin, capturing the live tool catalog and two read-only API responses. The PAT came from `gh auth token` and was passed only via the `GITHUB_PERSONAL_ACCESS_TOKEN` env var — it was never printed, logged, or written to the eval. **No mutating tool was called.**

```bash
brew install github-mcp-server              # → v1.4.0 (bottled, arm64), ~20s
github-mcp-server --version                 # Version: 1.4.0  Build Date: 2026-06-17T16:04:18Z
export GITHUB_PERSONAL_ACCESS_TOKEN="$(gh auth token)"   # token never echoed

# Drive stdio mode: feed JSON-RPC with small delays so stdin stays open past each response
{
  printf '%s\n' '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2024-11-05","capabilities":{},"clientInfo":{"name":"eval-runner","version":"1.0"}}}'
  sleep 1; printf '%s\n' '{"jsonrpc":"2.0","method":"notifications/initialized"}'; sleep 0.5
  printf '%s\n' '{"jsonrpc":"2.0","id":2,"method":"tools/list","params":{}}'; sleep 2
} | github-mcp-server stdio --toolsets all   # → 83 tools
```

**Install (measured).** The Homebrew formula exists and installed a native arm64 bottle in **~20 s wall** (18.7 MB, 10 files) — no Go toolchain on the host (`go` was absent; `docker` present but not needed). `--version` reported **v1.4.0**, commit "Homebrew", build date **2026-06-17**. (The earlier draft's `npx @github/mcp-server` was correctly noted as non-existent; the real local entry points are the Homebrew/Go binary or the Docker image.)

**Handshake + tool catalog (measured, live — not README-paraphrased).** The stdio server completed the MCP `initialize` handshake reporting `serverInfo {name: github-mcp-server, version: 1.4.0}`, `protocolVersion: 2024-11-05`, and capabilities `{tools, prompts, resources, logging, completions}`. `tools/list` returned, by configuration:

| Invocation | Tools returned |
|---|---|
| default toolsets, `--read-only` | **25** |
| default toolsets, write-enabled | **43** |
| `--toolsets all`, write-enabled | **83** |
| `--toolsets all --read-only` | **53** |

The **default read-only 25** were: `get_me`, `get_commit`, `get_file_contents`, `get_label`, `get_latest_release`, `get_release_by_tag`, `get_tag`, `get_team_members`, `get_teams`, `issue_read`, `pull_request_read`, `list_branches`, `list_commits`, `list_issues`, `list_issue_types`, `list_pull_requests`, `list_releases`, `list_repository_collaborators`, `list_tags`, `search_code`, `search_commits`, `search_issues`, `search_pull_requests`, `search_repositories`, `search_users`. The full 83-tool surface adds 18+ write tools (`create_or_update_file`, `create_pull_request`, `create_branch`, `merge_pull_request`, `delete_file`, `add_issue_comment`, `fork_repository`, `assign_copilot_to_issue`, …).

**The `--read-only` filter actually works (measured).** `--toolsets all` exposed **83** tools of which **exactly 53 carry the `annotations.readOnlyHint: true` flag**; passing `--read-only` returned **exactly those 53** and **zero** `create_*`/`update_*`/`delete_*`/`merge_*` tools. So the safety filter is annotation-driven and verifiably drops every mutating tool — a real, checkable safety property, not a doc claim.

**Two read-only `tools/call`s against the live API (measured).** With the PAT supplied:
- `get_me` → `isError: null`, returned the authenticated profile (`login: mattbutlerengineering`, plus `id`/`avatar_url`/`profile_url`/`details`). (Only the non-sensitive `login` field is reproduced here.)
- `search_repositories {"query":"repo:github/github-mcp-server"}` → `isError: null`, returned `github/github-mcp-server | stars: 30891 | lang: Go`, which **matches `gh api repos/github/github-mcp-server`** (30,891 stars, Go, MIT, pushed 2026-06-22) — confirming the MCP tool returns the same live data the API does.

**`list-scopes` (measured).** `github-mcp-server list-scopes` printed the per-tool OAuth scope requirements grouped by toolset (e.g. `get_me: (no scope required)`, `get_teams: read:org`, `assign_copilot_to_issue: repo`), with read 👁 / write 📝 markers — a useful pre-flight for least-privilege PAT scoping.

**What required a token / a full MCP client and was NOT exercised:** tool *enumeration* and the *handshake* need no valid token (static catalog), but the two `tools/call`s above did use the PAT. No **write/mutating** tool was invoked (by design and policy). The full agentic loop — an LLM client selecting and chaining these tools across a multi-step task — was not driven; that is the MCP *client's* job, and this eval measures the *server surface* (catalog, read-only filtering, auth path, live read calls) rather than agent task success. The hosted remote endpoint and the Docker image were not separately exercised (the native binary covers the same tool surface).

## What worked

- **Installs natively via Homebrew on macOS arm64** — `brew install github-mcp-server` poured a v1.4.0 bottle in ~20 s; no Go toolchain or Docker required. The formula (1.4.0) tracks the repo closely (build date 2026-06-17).
- **Live tool catalog enumerated over real JSON-RPC stdio** — 25 (default read-only) / 43 (default) / 53 (all read-only) / **83 (all)** tools, captured from the running server, not the README. Toolsets and `--read-only` compose predictably.
- **`--read-only` is a verifiable safety boundary** — the 53 read-only tools map exactly to the 53 tools annotated `readOnlyHint: true`; the flag removes every mutating tool. This is a concrete, auditable safety property.
- **Read-only API path works end-to-end** — `get_me` and `search_repositories` returned live, correct data (cross-checked against `gh api`), proving the PAT auth path and the server's GitHub-API plumbing function.
- **Least-privilege tooling** — `list-scopes` enumerates the exact OAuth scope each enabled tool needs, with read/write markers; easy to scope a PAT down per use case.
- **First-party, broad coverage** — 83 tools across repos, issues, PRs, actions, code/secret security, orgs, gists, notifications, discussions, projects — wider and more current than the community `server-github`.

## What didn't work or surprised us

- **stdio needs stdin kept open** — naïvely piping all JSON-RPC lines at once makes the server hit EOF and exit (`server is closing: EOF`) before responding; a real MCP client holds the pipe open. Driving it by hand required interleaved `sleep`s. (A client-loop concern, not a defect.)
- **Large default surface** — even the default toolset is 43 tools (25 read-only); `--toolsets all` is 83. That is a lot of tool descriptions in context and can degrade tool selection on smaller models. Scoping toolsets is effectively mandatory.
- **Overlaps with `gh` already in the bash tool** — for `gh issue list` / `gh pr view`-style tasks the MCP adds little; its edge is cross-repo `search_code`/`search_*` and structured PR/security workflows.
- **Auth still PAT-scoped rate limits** — heavy parallel-agent use shares one PAT's quota; no built-in fan-out.
- **No webhook/event subscription** — read tools poll; there is no event stream.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | `search_repositories`/`get_me` returned the same live data as `gh api` (30,891 stars cross-checked); same GitHub API source as the CLI. |
| Speed | + | One `search_code`/`search_*` tool spans all of GitHub's native search; faster than scripting multi-step `gh api` queries. Handshake + tool enumeration completed sub-second. |
| Maintainability | neutral | No effect on the codebase being worked on. |
| Safety | + | `--read-only` verifiably filters to the 53 `readOnlyHint` tools (0 mutating tools remain); `list-scopes` enables least-privilege PAT scoping. Offsetting risk: the full surface includes 18+ write tools, so toolset/read-only scoping is required to bound blast radius. |
| Cost Efficiency | neutral | 25–83 tool descriptions in context is real token overhead; mitigated by enabling only needed toolsets. |

## Verdict

**ADOPT**

Confirmed hands-on: the official GitHub-maintained server installs as a native arm64 Homebrew binary (v1.4.0), completes a real MCP handshake over stdio, and exposes a **live, enumerated catalog of 83 tools** (25 read-only by default), with a **verifiable `--read-only` safety filter** that maps exactly to the 53 `readOnlyHint`-annotated tools and drops every mutating tool. Two read-only calls (`get_me`, `search_repositories`) returned live data matching `gh api`, proving the auth and API path. It earns its place over the community `server-github` on coverage breadth (code/secret security, actions, discussions, projects) and the cross-repo `search_*` tools; for basic issue/PR operations the `gh` CLI in the bash tool is equivalent, so scope the enabled toolsets to avoid loading all 83 tools into context. The agentic client loop (an LLM chaining these tools) and write/mutating tools were not exercised here — this eval measures the server surface, auth, and read path, all of which check out.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [github-mcp-server](https://github.com/github/github-mcp-server) | MCP server | GitHub's official MCP server — repos, issues, PRs, actions, search, code navigation | Need first-party GitHub integration with full API coverage and official support | server-github |
