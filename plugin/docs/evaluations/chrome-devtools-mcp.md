# Evaluation: chrome-devtools-mcp

**Repo:** [benjaminr/chrome-devtools-mcp](https://github.com/benjaminr/chrome-devtools-mcp)
**Stars:** 300 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

An MCP server that bridges Claude to Chrome's DevTools Protocol (CDP), giving agents direct access to network monitoring, console logs, JavaScript execution, DOM inspection, CSS analysis, storage/cookie access, and performance metrics. Unlike playwright (which automates browser interactions — clicking, typing, navigating), this server focuses on *inspection*: reading network responses, diagnosing console errors, profiling performance, and examining runtime state. The agent connects to a Chrome instance with remote debugging enabled and queries it through ~40 MCP tools organized into six categories (Chrome management, network, console, page analysis, DOM, CSS).

Available as a Claude Desktop Extension (.dxt) for one-click install, or via `claude mcp add` for Claude Code with a Python server + uv venv.

## How we tested it

Architecture review of the repo structure, README, and tool catalog. Not hands-on tested (no Chrome DevTools debugging session available in this environment).

```bash
gh api repos/benjaminr/chrome-devtools-mcp --jq '.description, .stargazers_count, .updated_at'
gh api repos/benjaminr/chrome-devtools-mcp/readme --jq '.content' | base64 -d
```

Assessed the tool surface area (40+ tools), installation paths (4 options including Claude Code), and compared against playwright MCP (ADOPT) and agent-browser (ADOPT) for overlap and complementarity.

## What worked

- **Genuinely different from playwright**: playwright automates (click, fill, navigate); this *inspects* (network requests, console errors, performance metrics, computed styles). They complement each other — playwright drives the browser, chrome-devtools-mcp reads what happened
- **Deep tool surface**: 40+ tools covering network monitoring with filtering (`filter_status=500`), console error summaries, live console monitoring, DOM querying with CSS selectors, computed/inline/matched style analysis, CSS coverage tracking, storage/cookie inspection, and performance metrics
- **Claude Code integration documented**: explicit instructions with absolute-path requirements and common pitfalls called out (relative paths, ModuleNotFoundError, venv Python)
- **Pre-commit quality gates**: ruff formatting/linting, mypy type checking, pytest validation, MCP server registration check
- **Extension packaging**: ships as .dxt for Claude Desktop one-click install

## What didn't work or surprised us

- **300 stars is modest** — the devtools-debugger-mcp fork by ScriptedAlchemy (345 stars) adds breakpoint debugging, step/run, call stacks, and source maps, which this server lacks. The debugging space is fragmenting
- **Python server with uv dependency**: heavier setup than a Node-based MCP server; requires cloning, `uv sync`, absolute path configuration. Compare with playwright MCP which is a single npx command
- **No breakpoint support**: the most powerful DevTools capability (setting breakpoints, stepping through code, inspecting call stacks) is missing — devtools-debugger-mcp covers this gap
- **Catalog URL is wrong**: CATALOG.md links to `ChromeDevTools/chrome-devtools-mcp` which 404s; real repo is `benjaminr/chrome-devtools-mcp`
- **Not tested hands-on**: evaluation is architecture-review-based; actual tool reliability in agent debugging sessions is unverified

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Network request inspection and console error summaries surface bugs that test suites miss |
| Speed | + | Agents can diagnose auth/network/performance issues without manual DevTools investigation |
| Maintainability | neutral | Inspection tool, doesn't change code |
| Safety | neutral | Localhost-only by design; no production use case |
| Cost Efficiency | neutral | Standard MCP tool call overhead |

## Verdict

**CONDITIONAL**

Use when you need agents to *diagnose* web application issues (failed API calls, console errors, performance bottlenecks, cookie/storage problems) rather than just *automate* browser interactions. Complements playwright MCP (ADOPT) and agent-browser (ADOPT) — those drive the browser, this reads what happened. The Python/uv setup is heavier than ideal, and the missing breakpoint support is a real gap (devtools-debugger-mcp fills it). Choose this when debugging network, console, or performance issues; choose playwright for automation and testing.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [chrome-devtools-mcp](https://github.com/benjaminr/chrome-devtools-mcp) | MCP server | Chrome DevTools Protocol integration — network, console, DOM, CSS, performance inspection | Need agents to inspect, debug, and profile web apps in Chrome, not just automate them | playwright (complementary: playwright = automation, chrome-devtools = inspection) |
