# Evaluation: DesktopCommanderMCP

**Repo:** [wonderwhy-er/DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP)
**Stars:** ~6,200 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (agent execution / MCP server)
**Layer:** Infrastructure

---

## What it does

An MCP server that gives MCP clients (Claude Desktop and others) terminal and filesystem capabilities: run shell commands, search the filesystem, and edit files via surgical diffs — turning a chat client into something that can actually do work on your machine.

Mechanically it exposes MCP tools for: executing terminal commands, including managing **long-running / background processes** (start, read output, terminate); filesystem search; and **diff-based file editing** (apply targeted edits rather than rewriting whole files). The pitch is that it works "using host client subscriptions instead of API token costs" — i.e. when driven from Claude Desktop, you pay your existing subscription, not per-token API. There's also an optional Desktop Commander **App** (beta, macOS/Windows) that adds any-model support, live visual file previews, and custom MCP/context, but the MCP server itself works standalone with any MCP client.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the documented tool surface (terminal exec incl. long-running processes, filesystem search, diff editing). Confirmed the standalone MCP-server install path and the "use host subscription, not API tokens" cost model. Did not connect it to a live client and execute commands — granting an agent shell + filesystem write is a real safety decision and is environment-specific — so verdict is condition-gated.

```bash
gh api repos/wonderwhy-er/DesktopCommanderMCP --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/wonderwhy-er/DesktopCommanderMCP/readme --jq '.content' | base64 -d
```

## What worked

- **Agentic capabilities for non-agentic clients.** Brings terminal + file editing to Claude Desktop and other MCP clients that otherwise can't touch the local system — useful where you live in a chat client, not a coding CLI.
- **Diff-based editing + background processes.** Surgical diffs avoid whole-file rewrite errors, and long-running process management handles servers/builds that don't return immediately.
- **Subscription-cost model.** Driven from a subscription client, you avoid per-token API spend for heavy file/terminal work.

## What didn't work or surprised us

- **Powerful = dangerous.** Shell execution + filesystem writes from an LLM is exactly the surface tools like cc-safety-net and agentlint guard against; run it only in trusted contexts with appropriate approval/sandboxing.
- **Redundant for Claude Code users.** Claude Code already has native Bash/Edit/Read tools; this MCP's value is mainly for chat clients that lack them.
- **App upsell.** The richest experience (any-model, live previews) is the separate beta app, not the OSS MCP server.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Diff-based edits reduce whole-file-rewrite corruption |
| Speed | + | Background-process control handles long-running builds/servers |
| Maintainability | neutral | A capability bridge, not a change to your codebase |
| Safety | - | Shell + filesystem write access from an LLM is high-risk without guards |
| Cost Efficiency | + | Uses host client subscription instead of per-token API billing |

## Verdict

**CONDITIONAL**

Adopt if you primarily work inside Claude Desktop or another chat MCP client and want real terminal + file-editing power on a subscription cost model — paired with command-safety guards (cc-safety-net/agentlint) and run only in trusted directories. For Claude Code users it's largely redundant with the native Bash/Edit tools. Treat the shell-access safety implications deliberately before enabling.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [DesktopCommanderMCP](https://github.com/wonderwhy-er/DesktopCommanderMCP) | MCP server | Terminal + filesystem control for AI clients (MIT, ★6.2K) — shell exec (incl. long-running processes), filesystem search, and diff-based file editing for Claude Desktop and other MCP clients, on host-subscription cost | Chat AI clients can't run commands or edit files locally; want agentic terminal/file automation without per-token API costs | serena, claude-context, chrome-devtools-mcp, mcp-run-python |
