# Evaluation: server-filesystem (MCP reference filesystem server)

**Repo:** [modelcontextprotocol/servers](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem)
**Stars:** 87,449 (monorepo) | **Last updated:** 2026-06-19 | **License:** MIT (per-package; repo metadata reports NOASSERTION for the monorepo)
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "Local filesystem access with safety controls." It is the official MCP reference server for filesystem operations — a Node.js MCP server that exposes structured file tools (read, write, edit, list, search, move, metadata) to any MCP client, with all operations sandboxed to an explicitly allowed set of directories.

Mechanism: the server is started with one or more allowed directories, either as command-line arguments (`mcp-server-filesystem /path/to/dir1 /path/to/dir2`) or — the recommended path — dynamically via the MCP **Roots** protocol, where the client advertises roots and the server replaces its allowed-directory set at runtime (and on `roots/list_changed` notifications). Every filesystem tool call is checked against the allowed set; the server refuses to operate with zero allowed directories. It exposes ~14 tools including `read_text_file` (with `head`/`tail`), `read_media_file` (base64 + MIME), `read_multiple_files`, `write_file`, `edit_file` (pattern-match edits with git-style diff and `dryRun` preview), `create_directory`, `list_directory`, `list_directory_with_sizes`, `directory_tree`, `move_file`, `search_files` (glob with exclude patterns), `get_file_info`, and `list_allowed_directories`. Each tool carries MCP ToolAnnotations (`readOnlyHint`, `idempotentHint`, `destructiveHint`) so clients can distinguish reads from destructive writes.

## How we tested it

**Evidence:** REVIEW

Method (stated honestly): **inspected, not installed/run.** Investigated via `gh api` against `modelcontextprotocol/servers` — pulled repo metadata and read the full `src/filesystem/README.md` to enumerate the tool surface, the directory-access-control model (command-line args vs. Roots protocol), and the tool annotations. No server process was started and no MCP client was wired to it; the catalog framework decision below does not depend on runtime metrics, only on the capability surface and the overlap analysis against Claude Code's native tools.

```
gh api repos/modelcontextprotocol/servers --jq '{description, stars, license, updated, archived}'
gh api repos/modelcontextprotocol/servers/contents/src/filesystem/README.md --jq '.content' | base64 -d
```

## What worked

- Clean safety model: every operation is gated to an allowed-directory allowlist, and the server refuses to start with no allowed directory — a sensible fail-closed default for the "agent needs guardrails" problem.
- The Roots protocol integration is the modern, well-designed part: a client can hand the server its working directories at connect time and update them at runtime without a restart.
- Tool annotations (`readOnlyHint`/`destructiveHint`/`idempotentHint`) let a host UI flag destructive writes and auto-approve pure reads — genuinely useful for clients that surface tool-permission prompts.
- `edit_file` with `dryRun` produces a git-style diff before applying, mirroring the preview-before-write pattern Claude Code's own Edit tool enforces.

## What didn't work or surprised us

- **Heavy redundancy for Claude Code users.** Claude Code already ships native Read, Write, Edit, Glob, and Grep tools that cover this server's entire surface (and Grep is more capable than the server's filename-only `search_files`, which matches paths, not file contents). Installing this MCP server in Claude Code adds a second, parallel set of file tools, consuming context budget on tool definitions and inviting the model to pick the wrong one.
- The server's value is real only for MCP **clients that lack native file tools** — Claude Desktop, custom MCP hosts, IDE integrations built on the raw protocol. For those, it is the canonical way to give an agent guarded filesystem access.
- `search_files` is filename/path glob matching only — it does not search file contents, so it is not a Grep substitute even where a client has no native search.
- The repo-level license reports as NOASSERTION via the GitHub API (the monorepo mixes licenses); the filesystem package itself is MIT.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Same file operations Claude Code already performs natively; no correctness gain for CC users. |
| Speed | neutral / minus | Extra MCP hop and duplicate tool definitions add latency/context overhead vs. native tools for CC; neutral for clients with no alternative. |
| Maintainability | neutral | One more server process and config to maintain; offset only when it is the *only* way a client gets file access. |
| Safety | plus | Allowlist sandboxing + fail-closed default + destructive-hint annotations give real guardrails for clients without their own. |
| Cost Efficiency | minus | For CC, duplicate tool schemas burn context tokens with no offsetting benefit. |

## Verdict

**SKIP** (for Claude Code) / **CONDITIONAL** (keep for non-CC MCP clients).

For Claude Code users this server is redundant: native Read/Write/Edit/Glob/Grep already cover and in places exceed its surface, while adding it costs context and risks tool-selection confusion. It earns a place only for MCP clients that lack built-in file tools (Claude Desktop, custom hosts, raw-protocol IDE integrations), where its allowlist sandboxing and tool annotations make it the canonical safe-filesystem-access option. Catalog it as the reference filesystem server with that scope caveat; do not add it to the recommended Claude Code stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [server-filesystem](https://github.com/modelcontextprotocol/servers/tree/main/src/filesystem) | MCP server | Local filesystem access with safety controls (sandboxed to allowed dirs) | Agent needs structured file operations with guardrails — for MCP clients lacking native file tools | Claude Code native Read/Write/Edit/Glob/Grep (fully redundant for CC) |
