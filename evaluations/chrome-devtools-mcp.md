# Evaluation: chrome-devtools-mcp (official)

**Repo:** [ChromeDevTools/chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp)
**Stars:** 48,535  <!-- repo-metadata.json, fetched 2026-08-04 -->
**Last updated:** 2026-08-04 | **License:** Apache-2.0
**Last verified:** 2026-08-05
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

> **This eval replaces a mismatched one** ([#355](https://github.com/mattbutlerengineering/ai-tooling/issues/355)).
> The file that previously held this name reviewed `benjaminr/chrome-devtools-mcp` — a
> different codebase that shares the name — while the `CATALOG.md` row named the official
> server. That review now lives at
> [`chrome-devtools-mcp-benjaminr.md`](chrome-devtools-mcp-benjaminr.md); this file is the
> official server, run hands-on.

## What it does

The Chrome DevTools team's own MCP server. It gives an agent a live Chrome over CDP +
Puppeteer, and — the part that distinguishes it from every other browser MCP — exposes
**DevTools' measurement surface**, not just its automation surface: performance traces
with Core Web Vitals and per-insight drill-down, a full Lighthouse audit, heap
snapshots, and device emulation, alongside the usual navigate/click/fill/snapshot tools.

Distribution is npm; there is nothing to build. It launches Chrome itself (or attaches
to a running instance over `--browserUrl` / `--wsEndpoint` / `--autoConnect`), and
`--isolated` gives each run a throwaway user-data-dir.

## How we tested it

**Evidence:** MEASURED

Run hands-on on **2026-08-05**, macOS 15 (darwin 25.5.0), Node v22.22.3, Chrome stable
from `/Applications/Google Chrome.app`, server pinned to **v1.6.0**.

There is no MCP client in this repo, so the server was driven directly: a ~70-line
JSON-RPC-over-stdio driver (`initialize` → `notifications/initialized` → `tools/list` →
a scripted sequence of `tools/call`), timing every call and printing the raw response
bodies. Every figure below is from that driver's output, not from the README. The same
driver was pointed at `@playwright/mcp` to make the surface comparison a measurement
rather than a recollection.

`CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=1` was set for every run — see **Safety**.

```bash
# server under test (headless, throwaway profile)
npx -y chrome-devtools-mcp@1.6.0 --headless --isolated
npx -y chrome-devtools-mcp@1.6.0 --headless --isolated --slim   # 3-tool mode
# comparison arm
npx -y @playwright/mcp@latest --headless
```

## Test design

- **Task/corpus:** three fixed public pages — `https://example.com` (minimal),
  `https://en.wikipedia.org/wiki/Main_Page` (real, image-heavy, for the trace), and
  `https://en.wikipedia.org/wiki/Model_Context_Protocol` (long article, for snapshot
  size). Plus two deliberate error paths: `click` on a non-existent `uid`, and a
  malformed `wait_for` call.
- **Baseline:** `@playwright/mcp` (v1.63.0-alpha-2026-08-05) — the browser MCP already in
  [STACK.md](../STACK.md) — enumerated with the same driver, so "what does this add" is a
  set difference between two measured tool lists rather than an impression.
- **Metric:** tool count per server; wall-clock per `tools/call`; response body size in
  characters (a direct proxy for context cost); `isError` on the failure paths.
- **Reproduce:** the driver is ~70 lines against the MCP stdio protocol; the commands
  above plus a JSON list of `{name, args}` steps reproduce every number here.

### Measured results

| Call | Wall-clock | Response size |
|---|---|---|
| `initialize` | 1,090 ms (includes npx cold start) | — |
| `tools/list` | 4 ms | **29 tools** |
| `new_page` (example.com) | 1,033 ms | 127 chars |
| `take_snapshot` (example.com) | 9 ms | ~330 chars |
| `evaluate_script` | 205 ms | small |
| `list_console_messages` | 2 ms | `<no console messages found>` |
| `list_network_requests` (example.com) | 1 ms | 1 request |
| `new_page` (Wikipedia main page) | 1,277 ms | — |
| `performance_start_trace` (`reload:true, autoStop:true`) | **6,982 ms** | **8,871 chars** |
| `performance_analyze_insight` (`LCPBreakdown`) | 1 ms | ~900 chars |
| `lighthouse_audit` | **5,665 ms** | ~600 chars + report files |
| `list_network_requests` (Wikipedia) | 2 ms | 36 requests, 7,595 chars |
| **`take_snapshot` (long article)** | 61 ms | **72,445 chars** |
| `take_screenshot` | 40 ms | one image |
| `click` on bogus uid | 1 ms | `isError=true`, `Element uid "9_9999" not found on page 2.` |

**Tool surface, measured both ways:**

| | chrome-devtools-mcp 1.6.0 | @playwright/mcp 1.63.0-alpha |
|---|---|---|
| Tools | **29** (3 with `--slim`) | **24** |
| Only here | `performance_start_trace`, `performance_stop_trace`, `performance_analyze_insight`, `lighthouse_audit`, `take_heapsnapshot`, `emulate`, `list_pages`/`select_page`/`close_page` | `browser_find`, `browser_run_code_unsafe`, `browser_tabs`, `browser_select_option`, `browser_navigate_back` |
| Shared | navigate · click · hover · drag · fill / fill_form · press_key · type · screenshot · a11y snapshot · console · network · dialogs · file upload · resize · wait_for · evaluate | — |

The overlap is the automation surface. **The delta is measurement.**

## What worked

- **Zero-friction start.** One `npx`, no build, no config file, no API key. Headless with
  a throwaway profile worked first try and never touched the user's Chrome profile.
- **The performance trace is the reason to use it.** One call returned lab metrics
  (LCP 283 ms with a TTFB/render-delay breakdown, CLS 0.00) **and CrUX field data for
  real users** (p75 LCP 802 ms, INP 57 ms), then listed named insights the agent can
  drill into. `performance_analyze_insight` returned a prose analysis with percentage
  attribution ("Time to first byte: 36 ms, 24.4% of total LCP time"), an estimated-savings
  figure, and links to the relevant web.dev docs. Nothing else in this catalog's browser
  cluster produces that.
- **Lighthouse is built in.** `lighthouse_audit` returned Accessibility 95, Best
  Practices 77, SEO 92 — and an **Agentic Browsing: 50** category, which is Lighthouse
  scoring how workable the page is *for an agent*. It writes full JSON and HTML reports
  to temp paths.
- **The a11y-tree snapshot is genuinely readable** and stable to act on — every node
  carries a `uid` that the interaction tools take, so click/fill target the tree rather
  than a CSS selector.
- **Errors are clean.** A bogus `uid` returned `isError=true` with an actionable message
  in 1 ms rather than hanging or throwing at the protocol level.
- **`--slim` is a real cost control**, not a marketing bullet: it collapses 29 tools to 3
  (`navigate`, `evaluate`, `screenshot`). For an agent that only needs to look at a page,
  that is 26 tool definitions kept out of context.
- **Deep configurability where it matters for cost:** `--screenshotFormat jpeg|webp`,
  `--screenshotQuality`, `--screenshotMaxWidth/Height`, and per-category toggles
  (`--categoryPerformance=false`, `--categoryNetwork=false`) to trim the surface.

## What didn't work or surprised us

- **A snapshot of a real article is 72,445 characters** — roughly 18k tokens for one
  `take_snapshot` on a long Wikipedia page. On a content-heavy app this single call can
  dominate a context window, and nothing in the tool description warns you. This is the
  most important practical finding here and it applies equally to playwright-mcp's
  snapshot; it is a property of a11y-tree snapshots, not a defect of this server.
- **Telemetry is on by default.** `--usageStatistics` defaults to `true` ("Google collects
  usage data… handled under the Google Privacy Policy"), and separately
  `--performanceCrux` defaults to `true`, which **sends URLs from your performance traces
  to the CrUX API**. On a localhost or staging URL that is a private hostname leaving the
  machine. Both are opt-out (`CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS`, or the flags), and
  the CI env var disables statistics — but the default is collect, and the CrUX default is
  what makes the field-data feature work, so turning it off costs you the best part of the
  trace output.
- **The measurement calls are slow in agent terms** — 7.0 s for a trace, 5.7 s for
  Lighthouse. Fine for a deliberate check, wrong for a tight inner loop.
- **A large experimental surface** — a dozen `--experimental*` flags (vision, screencast,
  devtools targets, WebMCP, structured content, memory). Useful, but a reminder that the
  stable contract is narrower than the flag list suggests.
- **`--autoConnect` and the extensions category need Chrome 144+/149+**, so the
  attach-to-my-running-browser path is version-gated in ways the tool list doesn't show.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | **+** | Verification against a real rendered page — lab *and* field Core Web Vitals, a Lighthouse pass, real console and network output — instead of asserting the UI is fine |
| Speed | **neutral** | Sub-100 ms for inspection calls, but 7.0 s per trace and 5.7 s per Lighthouse run; it accelerates *finding* a perf problem, not the loop |
| Maintainability | **neutral** | Nothing enters the codebase; it is an MCP endpoint, and removing it leaves no trace |
| Safety | **−** | Telemetry on by default, and `--performanceCrux` sends traced URLs (including local/staging hostnames) to a Google API unless disabled |
| Cost Efficiency | **−** | 29 tool definitions resident, and a single `take_snapshot` measured at 72,445 chars (~18k tokens). `--slim` and the category toggles are the mitigations, and they work |
| Verifiability | **+** | Turns "is the page fast/accessible?" into numbers a human can check — LCP breakdown with percentage attribution, Lighthouse category scores, an insight name with a docs link |

## Verdict

**CONDITIONAL** — `adopt-if:` the work is **frontend performance or accessibility**
(Core Web Vitals regressions, LCP/CLS investigation, Lighthouse scores), in which case
nothing else in the catalog comes close.

Do **not** adopt it as a general browser tool alongside [`playwright`](playwright-mcp.md),
which is already the STACK pick for browser verification. The measured surfaces overlap
almost completely on automation — navigate, click, fill, snapshot, console, network — and
running both means **53 tool definitions in context** to gain five measurement tools.
Pick by the question being asked: *does the UI behave* is playwright's job; *is the page
fast, accessible, and agent-workable* is this one's, and it answers it with real
DevTools data rather than a proxy.

Two conditions on adoption, both measured above: disable telemetry
(`CHROME_DEVTOOLS_MCP_NO_USAGE_STATISTICS=1`) and set `--performanceCrux=false` for any
non-public URL; and treat `take_snapshot` as an expensive call on content-heavy pages —
reach for `--slim` or the category toggles when the agent only needs to look.

Held at CONDITIONAL rather than ADOPT because the adopt-if gate is real and narrow: for a
repo that ships no frontend, this server earns nothing, and the honest reading of a second
browser MCP in a stack that already has one is that it must justify its context cost per
project rather than by default.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [chrome-devtools-mcp](https://github.com/ChromeDevTools/chrome-devtools-mcp) | MCP server | Official Chrome DevTools MCP (Apache-2.0, ★48.5K, by the Chrome DevTools team) — gives agents a live Chrome via CDP + Puppeteer to navigate, inspect network/console/DOM, record performance traces with Core Web Vitals + CrUX field data, and run Lighthouse audits; 29 tools, or 3 in `--slim` mode | Agents change frontend code but can't see how the real page performs — no Core Web Vitals, no Lighthouse score, no console or network truth | playwright (complementary: playwright automates, this measures), agent-browser, browser-use, midscene |
