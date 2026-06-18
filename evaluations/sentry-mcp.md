# Evaluation: Sentry MCP Server

**Repo:** [getsentry/sentry-mcp](https://github.com/getsentry/sentry-mcp)
**Stars:** 731 | **Last updated:** 2026-06-18 | **License:** Proprietary (Sentry BSL)
**Dev loop stage:** Verify / Reflect
**Layer:** Infrastructure

---

## What it does

MCP server that connects Claude Code (and other coding agents) to your Sentry account, exposing 35+ tools for querying issues, events, traces, replays, alerts, monitors, and releases. Ships as both a remote HTTP MCP server (mcp.sentry.dev) and a local stdio transport for self-hosted Sentry. Also ships as a Claude Code plugin via the official marketplace, bundling 5 setup skills (tracing, logging, metrics, AI monitoring, code review), an issue-summarizer agent, and two commands (/getIssues, /seer).

When invoked, the MCP tools let you pull Sentry issue details, stack traces, event context, and AI analysis (via Seer) directly into the coding agent's context — no browser tab-switching needed. The plugin skills automate the setup of Sentry SDKs in your project, and the code-review skill processes Sentry bot comments on GitHub PRs.

## How we tested it

Installed the plugin via the Claude Code marketplace (sentry@claude-plugins-official). Verified the MCP tools are registered in this session — `mcp__sentry__authenticate` and `mcp__plugin_sentry_sentry__authenticate` both appear in the deferred tool list. Examined the plugin structure:

```
~/.claude/plugins/cache/claude-plugins-official/sentry/1.0.0/
├── agents/issue-summarizer.md     # parallel issue analysis agent
├── commands/getIssues.md          # /getIssues slash command
├── commands/seer.md               # /seer AI analysis command
├── skills/sentry-code-review/     # analyze Sentry bot PR comments
├── skills/sentry-setup-tracing/   # instrument perf monitoring
├── skills/sentry-setup-logging/   # add structured logging
├── skills/sentry-setup-metrics/   # add custom metrics
├── skills/sentry-setup-ai-monitoring/  # instrument LLM calls
└── MCP-SETUP.md                   # remote MCP connection guide
```

Reviewed the MCP server's tool catalog from the repo source (packages/mcp-core/src/tools/catalog/) — 35+ tools covering: issue lifecycle (get-issue-details, update-issue, search-issues, add-issue-note), event analysis (search-events, search-issue-events, get-trace-details, get-replay-details), infrastructure (find-alert-rules, find-monitors, find-releases, get-dashboard-details), project management (create-project, create-team, create-dsn), and AI analysis (analyze-issue-with-seer, search-docs).

Verified active maintenance: commits daily (latest 2026-06-18), releases every 2-3 weeks (v0.36.0 on 2026-06-08), 731 stars.

Note: Full tool invocation requires Sentry account authentication (OAuth flow via mcp.sentry.dev or access token for stdio). The evaluation covers architecture, plugin quality, and tool surface area rather than end-to-end authenticated usage.

## What worked

- **Comprehensive tool surface**: 35+ tools covering the full Sentry API — not just issue queries but traces, replays, profiles, alerts, monitors, dashboards, and releases. This is one of the most thorough MCP server implementations available
- **Plugin integration is well-designed**: 5 setup skills that detect your project stack and instrument Sentry automatically (JS, TS, Python, Ruby, React, Next.js, Node.js), plus the code-review skill that processes Sentry bot comments on PRs
- **Dual transport**: remote HTTP (zero-install, mcp.sentry.dev) and local stdio (self-hosted, npx @sentry/mcp-server) with configurable skill disabling
- **AI-powered search**: search-events and search-issues use an embedded LLM agent to translate natural language into Sentry's query syntax
- **Issue-summarizer agent**: parallel multi-issue analysis with pattern recognition and user impact assessment — a good example of a domain-specific subagent
- **Active development**: daily commits, well-structured monorepo with eval suite (packages/mcp-server-evals), smoke tests, and mock infrastructure

## What didn't work or surprised us

- **Authentication friction**: requires OAuth flow or manual access token setup before any tools work. The MCP-SETUP.md guide is minimal
- **AI search requires separate LLM key**: search_events and search_issues need an additional OpenAI or Anthropic API key configured as EMBEDDED_AGENT_PROVIDER — this nested LLM-calling-LLM pattern adds cost and complexity
- **Plugin MCP setup is manual**: the plugin installs skills and commands but the MCP server itself must be added separately via `claude mcp add` — the plugin can't auto-configure remote MCP servers
- **License is BSL, not OSS**: despite being on GitHub, this is Sentry's Business Source License — not truly open source

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Direct access to production error data, stack traces, and event context during development reduces debug guesswork |
| Speed | + | Eliminates context-switching to Sentry dashboard; issue details, traces, and replays accessible inline |
| Maintainability | + | Setup skills automate SDK instrumentation; code-review skill processes Sentry PR comments automatically |
| Safety | neutral | Requires auth tokens with scoped permissions; no code modification by the MCP server itself |
| Cost Efficiency | neutral | Free for the MCP server; Sentry account required (free tier available); AI search features consume additional LLM tokens |

## Verdict

**CONDITIONAL**

Use when your project uses Sentry for error tracking. The 35+ tool surface and plugin integration make this the most complete observability MCP server available — it turns Sentry from a tab you check into context your coding agent can query directly. The setup friction (OAuth + optional LLM key for AI search) and BSL license are the main drawbacks. Skip if you don't use Sentry or prefer a lighter-weight error monitoring integration.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sentry-mcp](https://github.com/getsentry/sentry-mcp) | MCP server | Connects coding agents to Sentry for inline error and performance analysis | Context-switching to Sentry dashboard during debugging slows the fix cycle | sentry (plugin) |
