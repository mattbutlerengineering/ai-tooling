# Composio

**Evidence:** SOURCE-ONLY

## What it does

Composio is an SDK and tooling platform that connects AI agents to 500+ external apps (Gmail, Slack, GitHub, Notion, Linear, Figma, Jira, etc.) through a unified interface. It handles OAuth authentication, tool discovery, and action execution across services. Their MCP product "Rube" exposes this as an MCP server that works with Claude Code, Cursor, VS Code, and other MCP-compatible clients.

It is NOT a Claude Code plugin or skill in itself. It is a cross-platform SDK (Python + TypeScript) with provider packages for OpenAI, Anthropic, LangChain, LlamaIndex, CrewAI, AutoGen, Vercel AI, Google Gemini, and more. The Claude Code integration happens through Rube (their MCP server).

## Repo Health

**Stars:** 28,791 | **Last updated:** 2026-06-16 | **License:** MIT | **Open issues:** 133 | **Forks:** 4,624

Healthy project. Active development (pushed today), strong community (28K+ stars), reasonable issue count relative to scope. Created Feb 2024, so ~2.3 years old with sustained growth.

## What problem it solves

The core problem: if your agent needs to interact with 10 external services (GitHub, Slack, Linear, Gmail, Sentry, Figma, etc.), you currently need to configure 10 separate MCP servers, each with its own auth flow, token management, and API quirks. Composio bundles this into one integration point with unified auth management.

Secondary value: tool discovery. Instead of knowing which MCP server exists for which service, the agent can search Composio's toolkit registry and find the right action dynamically.

## Does anything in the current workflow already cover this?

**Partially yes.** The recommended stack already includes individual MCP servers for the most common integrations:

| Need | Current recommendation | Composio equivalent |
|------|----------------------|-------------------|
| GitHub | server-github MCP / gh CLI | Composio GitHub toolkit |
| Sentry | sentry MCP | Composio Sentry toolkit |
| Jira | jira MCP (mcp-atlassian) | Composio Jira toolkit |
| Confluence | confluence MCP | Composio Confluence toolkit |
| Browser | playwright MCP | Not covered by Composio |
| Database | prisma MCP / supabase MCP | Composio has some DB toolkits |
| Docs lookup | context7 MCP | Not covered by Composio |

**What Composio adds that individual MCP servers don't:**
- Unified OAuth management (authenticate once, use everywhere)
- 500+ app integrations vs. the ~15 MCP servers in the catalog
- Dynamic tool discovery (agent finds the right toolkit at runtime)
- Cross-app workflows in a single action chain (e.g., "when Sentry fires, create Linear issue, notify Slack")

**What individual MCP servers do better:**
- Deeper integration with specific tools (Playwright's browser automation is far richer than any Composio equivalent)
- No external dependency or API key required (most MCP servers run locally)
- No vendor lock-in (Composio is a SaaS with an API key)

## Dev loop fit

**Outer loop (Automate) — for cross-service orchestration.**

For the inner loop, individual MCP servers for GitHub and Sentry are sufficient. When feedback loops close themselves and agents take autonomous actions across services (triage issue in Linear, notify Slack, create PR in GitHub), the unified auth and cross-app workflow capability becomes valuable.

For simpler workflows, Composio is overhead — you don't need 500 integrations when you're using 5.

## Verdict

**CONDITIONAL** — adopt if you need cross-app automation across 5+ external services in the outer loop, AND individual MCP servers aren't covering your needs.

**Reasons to skip for now:**
1. Individual MCP servers (GitHub, Sentry, Jira, Playwright, Prisma) already cover the most critical integrations in the recommended stack
2. Composio adds a SaaS dependency with an API key — counter to the "local-first, fewer dependencies" philosophy
3. The 500+ integrations sound impressive but most developers use 5-10 tools daily — the long tail is noise
4. Rube (their MCP product) competes with the individual MCP servers already installed, creating overlap rather than filling a gap

**Reasons to adopt later (L4+):**
1. If you're building autonomous workflows that chain actions across services
2. If managing OAuth tokens across 10+ MCP servers becomes painful
3. If you need integrations the MCP ecosystem doesn't cover yet (500 vs. ~50 MCP servers available)

## If adopting, where in WORKFLOW.md

L4 stack, as a **replacement for individual MCP servers** (not alongside them — that's the worst of both worlds). The adoption trigger would be: "I'm spending more time configuring and authenticating individual MCP servers than using them."
