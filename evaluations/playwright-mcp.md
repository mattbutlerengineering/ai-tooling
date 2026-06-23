# Evaluation: Playwright MCP

**Repo:** [microsoft/playwright-mcp](https://github.com/microsoft/playwright-mcp)
**Stars:** 34,050 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

MCP server built on Playwright that gives AI agents direct browser control — navigate pages, click elements, fill forms, take screenshots, and read accessibility snapshots. The agent calls MCP tools like `browser_navigate`, `browser_click`, `browser_snapshot` to interact with web pages programmatically.

## How we tested it

**Evidence:** RUN

Ran the Playwright MCP server live from inside an agent session (installed as a Claude Code plugin; the standalone install is `claude mcp add playwright -- npx @playwright/mcp@latest`). Navigated to a real page and captured the accessibility snapshot — the tool the eval claims is the differentiator — to see exactly what the agent gets back.

```
browser_navigate { url: "https://example.com" }
# -> Page URL: https://example.com/  |  Page Title: "Example Domain"

browser_snapshot
```

The snapshot came back as compact YAML, not an image:

```yaml
- generic [ref=e2]:
  - heading "Example Domain" [level=1] [ref=e3]
  - paragraph [ref=e4]: This domain is for use in documentation examples...
  - paragraph [ref=e5]:
    - link "Learn more" [ref=e6] [cursor=pointer]:
      - /url: https://iana.org/domains/example
```

## What worked

- **The accessibility snapshot is the real value, confirmed.** It returns a structured tree of roles + text (`heading [level=1]`, `paragraph`, `link` with its `/url`) — the agent reads page *state* without an image payload. Verifying "the H1 says Example Domain" or "the link points to iana.org" is a direct YAML read, no vision needed.
- **Every node carries a stable `[ref=eN]` handle.** Those refs are how follow-up actions target elements (`browser_click { ref: "e6" }`), so the agent doesn't have to author CSS/aria selectors itself — it points at what the snapshot already labeled.
- **`browser_navigate` returns the resolved URL and title inline**, so the agent gets immediate confirmation the navigation landed (e.g. trailing-slash normalization to `https://example.com/`).

## What didn't work or surprised us

- **The catalog's install command was wrong.** Both this eval and STACK.md referenced `@anthropic-ai/mcp-playwright`, which returns a 404 on npm — it does not exist. The real package is **`@playwright/mcp`** (Microsoft). Corrected here and in STACK.md as part of this evaluation.
- **It's lower-level than agent-browser by design** — you operate on snapshot refs / selectors rather than describing intent in natural language. Great for precise scripted checks, more verbose for one-off exploration.
- **Snapshot depth matters on real apps.** `example.com` is tiny; the tool exposes `depth` and `filename` params precisely because a full SPA tree can be large — capture to a file or limit depth rather than dumping the whole tree into context.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Accessibility snapshot gives exact roles/text/URLs to assert against (verified on a live page). |
| Speed | + | Headless, programmatic actions; no human in the loop for UI verification. |
| Maintainability | neutral | Ref/selector-based interaction can be brittle if the UI restructures. |
| Safety | neutral | Runs in a sandboxed browser context. |
| Cost Efficiency | + | YAML snapshot avoids the image-token cost of screenshotting just to read page state. |

## Verdict

**ADOPT**

Verified hands-on: a live navigate + snapshot returned a compact YAML accessibility tree with stable element refs — exactly the structured, screenshot-free page state that makes it cheap for an agent to verify UI without vision tokens. Install via `npx @playwright/mcp@latest` (not the non-existent `@anthropic-ai/mcp-playwright`). Use alongside agent-browser: Playwright MCP for precision scripted checks, agent-browser for exploratory natural-language interaction.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [playwright](https://github.com/microsoft/playwright-mcp) | MCP server | Browser automation and testing from within agent sessions | Agent can't interact with web UIs or run browser tests | agent-browser, chrome-devtools-mcp, browser-use |
