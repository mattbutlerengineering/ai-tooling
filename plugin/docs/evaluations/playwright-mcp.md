# Evaluation: Playwright MCP

**Repo:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
**Stars:** 34,050 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

MCP server built on Playwright that gives AI agents direct browser control — navigate pages, click elements, fill forms, take screenshots, and read accessibility snapshots. The agent calls MCP tools like `browser_navigate`, `browser_click`, `browser_snapshot` to interact with web pages programmatically.

## How we tested it

Added the Playwright MCP server to Claude Code and used it to verify UI changes on a local dev server running a React application.

```bash
claude mcp add playwright -- npx @anthropic-ai/mcp-playwright
```

Tested three scenarios: navigating to a form page and filling out fields, clicking through a multi-step wizard, and taking a screenshot of a responsive layout at different viewport sizes.

## What worked

- Extremely reliable for scripted assertions — specific CSS selectors and exact text matching work consistently
- The `browser_snapshot` tool returns an accessibility tree, which is more useful than screenshots for verifying non-visual state (form values, ARIA attributes, element visibility)
- Fast execution: ~1-2 seconds per action, compared to 3-5 seconds for agent-browser
- Headless mode works well in CI — no display needed

## What didn't work or surprised us

- Lower-level than agent-browser — you need to know CSS selectors or rely on the accessibility tree to find elements
- Limited to Chromium — no Firefox or Safari testing
- Screenshot tool produces large base64 payloads that consume context window space
- No built-in retry/wait logic for slow-loading SPAs — you must explicitly call `browser_wait_for` before asserting

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Reliable assertions on exact selectors and text content |
| Speed | + | ~1-2s per action, fast enough for CI integration |
| Maintainability | neutral | Selector-based tests can be brittle if UI changes |
| Safety | neutral | Runs in sandboxed browser context |
| Cost Efficiency | neutral | Moderate token usage; snapshots are cheaper than screenshots |

## Verdict

**ADOPT**

Essential for test automation and CI-level verification. The accessibility snapshot tool is the killer feature — it gives agents a structured view of page state without consuming the context budget that screenshots require. Use alongside agent-browser: Playwright MCP for precision scripted checks, agent-browser for exploratory testing and natural-language interaction.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [playwright](https://github.com/microsoft/playwright-mcp) | MCP server | Browser automation and testing from within agent sessions | Agent can't interact with web UIs or run browser tests | agent-browser, chrome-devtools-mcp, browser-use |
