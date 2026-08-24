# Evaluation: agent-browser

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
**Stars:** 41,204 | **Last updated:** 2026-08-24 (last push) | **License:** Apache-2.0
**Last verified:** 2026-08-23
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A browser automation CLI for AI agents — a terse, one-shot command surface over a persistent Chrome daemon. Roughly 40 commands (`open`, `click`, `fill`, `select`, `check`, `press`, `snapshot`, `read`, `get`, `is`, `find`, `eval`, `pdf`, `screenshot`, `connect`) driven by **CSS selectors, accessibility refs, and semantic locators** (`find role|text|label|placeholder|testid`). Ships as a Claude Code skill, a standalone CLI, and via Vercel Sandbox microVMs, with Electron support for desktop apps.

There is also **one** natural-language command — `chat "<instruction>"` — which requires `AI_GATEWAY_API_KEY`. It is one entry in the command list, not the interface.

## How we tested it

**Evidence:** RUN

**Method: installed `agent-browser@0.34.0` and drove it end-to-end against a locally-served fixture page, with per-action timings at N≥3.**

The previous review declined to run it on this reasoning: *"Exercising it meaningfully needs a running dev server (or an Electron target) and an interactive browser session rather than a scriptable one-shot."* **Both halves are wrong.** A dev server is `python3 -m http.server` and one HTML file; and the tool is a one-shot CLI against a persistent daemon — being scriptable is the whole design. That blocker is what kept the surface review from noticing that its central claim about the tool was also wrong.

```bash
# fixture: a form (email, select, checkbox, button), a testid result node,
# and a second fully inert page with no listeners and no timers.
python3 -m http.server 8931           # served from the fixture dir
npm i agent-browser@0.34.0
./node_modules/.bin/agent-browser open http://127.0.0.1:8931/
./node_modules/.bin/agent-browser snapshot
./node_modules/.bin/agent-browser fill '#email' 'loop-test@example.com'
./node_modules/.bin/agent-browser select '#plan' pro
./node_modules/.bin/agent-browser check '#tos'
./node_modules/.bin/agent-browser click '#submit'
./node_modules/.bin/agent-browser get text '#result'
./node_modules/.bin/agent-browser find label 'Email address' fill 'second@example.com'
./node_modules/.bin/agent-browser --json get text '#result'
```

**It works, and it is fast.** The full form flow ran clean: `fill` → `select` → `check` → `click` → `get text` produced `signed up: loop-test@example.com / pro`, and the negative path (submit without accepting terms) produced `error: you must accept the terms`. Semantic locators worked without a single CSS selector (`find label "Email address" fill …`, `find role button click`). `is checked` / `is visible` returned `true`; `wait`-free polling of a `setTimeout`-revealed element was correct. Failure messages are good and exit codes are right — a missing selector gives rc=1 and *"Element not found: #nope. Verify the selector, role, or name is correct and the element exists in the DOM."*

**Latency, N=3 per action, medians, warm daemon:**

| action | median | |
|---|---|---|
| `hover` | **5,073 ms** | pointer |
| `click` | **5,075 ms** | pointer |
| `focus` | 50 ms | |
| `press` | 51 ms | |
| `snapshot` | 53 ms | |
| `fill` | 53 ms | |
| `select` | 53 ms | |
| `get text` | 52 ms | |
| `read` | 53 ms | |
| `pdf` | 124 ms | |
| cold `open` (browser launch) | 4,167 ms | once per session |

**Pointer actions cost ~98× everything else, and the penalty is unconditional.** It reproduces across 8+ clicks (5,059 / 5,060 / 5,066 / 5,067 / 5,074 / 5,075 / 5,079 / 5,086 ms — a constant, not variance) and it reproduces on a **fully inert page with no event listeners, no timers and no navigation**, where a static `<button>` still costs 5,074 ms. So it is a fixed post-pointer settle rather than a wait on real page activity, and `--help` documents no flag to shorten it (`AGENT_BROWSER_DEFAULT_TIMEOUT` is 25,000 ms, a different number).

**`screenshot` failed every attempt on this machine — 5 of 5.** Two error modes, both after long stalls:

```
152,103 ms  rc=1  ✗ Failed to read: Resource temporarily unavailable (os error 35)
                     (after 5 retries - daemon may be busy or unresponsive)
152,112 ms  rc=1  (same)
 30,066 ms  rc=1  ✗ CDP command timed out: Page.captureScreenshot
 30,055 ms  rc=1  (same, PNG)
```

This is not a sick browser: `pdf` renders the identical page to a 26 KB file in **124 ms**, and `snapshot`/`read`/`get` all answer in ~50 ms. The failure is specific to `Page.captureScreenshot` over CDP. **Scoped honestly: one machine** (macOS, Darwin 25.5.0, headless Chrome, `agent-browser@0.34.0`) — reproducible here, not shown to be universal.

**`--json` is a clean scripting envelope:** `{"success":true,"data":{…,"text":"…"},"error":null}`, with session lifecycle metadata alongside the value.

**Not exercised:** Electron/desktop targets, Vercel Sandbox microVMs, `connect`/CDP against an existing browser, the `chat` command (needs `AI_GATEWAY_API_KEY`, which this machine does not have — verified it refuses cleanly with rc=1), the dashboard, action policies, and the Claude Code skill packaging. No comparison against Playwright MCP was re-run; the corrections below come from agent-browser's own surface, not from a head-to-head.

## Test design

- **Task/corpus:** one form page (text input, select, checkbox, button, `data-testid` result node, a `setTimeout`-revealed element) plus one fully inert control page with no scripts.
- **Baseline/control:** the inert page is the control for the latency finding — it removes every plausible cause of a real wait (listeners, timers, navigation), so a persisting 5 s is a fixed cost rather than page activity. `pdf` is the control for the screenshot finding: same page, same daemon, same render path, 124 ms and a valid file.
- **Metric:** per-action wall-clock median at N≥3, exit code, and output correctness against a known-correct DOM result string.
- **Reproduce:** the block above. Deterministic, fully local, no API keys, pinned to `agent-browser@0.34.0`.
- **Timing method:** `date +%s%N` around each invocation, so figures include npm-binary startup — the number a script actually pays, not an internal timer.

## What worked

- **The core loop is genuinely fast and genuinely scriptable.** ~50 ms per non-pointer command against a warm daemon, correct exit codes, and a clean `--json` envelope. This is a good CI/agent primitive.
- **Semantic locators are the real ergonomic win**, and they are not what the previous review described. `find label "Email address" fill …` and `find role button click` addressed the page with no CSS at all — stable against markup churn, and requiring no natural-language layer to do it.
- **`snapshot` and `read` are both cheap and both text.** A YAML-ish accessibility tree with refs (`textbox "Email address" [ref=e2]`) in 53 ms, and markdown page text in 53 ms.
- **Failure messages are actionable and exit codes are honest.** rc=1 with a message naming the selector and what to check. `chat` without a key refuses cleanly rather than half-running.
- **`pdf` works and is fast** — 124 ms for a full render, which is a usable visual-artifact path while `screenshot` is broken here.
- **Real adoption, by the one number the previous review didn't have: 5,001,582 npm downloads/month.** Pushed the day this was written; 41,204 stars.

## What didn't work or surprised us

- **It is not an intent-based tool, and the previous review's headline claim describes an optional credential-gated subcommand.** *"Intent-based commands ('click the submit button', 'fill the email field') so the agent describes goals instead of authoring CSS/aria selectors — the headline ergonomic difference from raw Playwright MCP"* is refuted by the CLI's own first help screen: every core command takes a selector or a ref. Natural language is exactly one command, `chat`, which requires `AI_GATEWAY_API_KEY`. The consequence reaches the comparison table — *"Learning curve: Zero — describe what you want"* is wrong for the 40 commands you would actually script.
- **The claimed state-readout difference does not exist.** The table gave agent-browser *"Screenshots (image payload)"* against Playwright MCP's *"YAML accessibility snapshot (no image) — verified"*. `agent-browser snapshot` **is** an accessibility tree with refs, in 53 ms, and `read` returns plain markdown. The two tools have the same primitive; the row asserted a distinction on the side that was never checked.
- **~5 s per pointer action, unconditional.** `click`, `dblclick` and `hover` all pay it; `fill`, `select`, `focus`, `press`, `snapshot`, `get` and `is` do not. A ten-click flow spends ~50 s waiting and ~0.5 s working. The previous review listed *"per-action overhead versus raw Playwright MCP calls — the intent-resolution step plausibly adds latency"* as an open question; there is no intent-resolution step, and the overhead is real and elsewhere.
- **`screenshot` failed 5 of 5 on this machine**, taking 30 s to 152 s to do it, with a *"daemon may be busy or unresponsive"* message that misattributes the cause — the same daemon answered `pdf` in 124 ms immediately afterwards. Screenshots are the capability the previous review named as this tool's distinguishing readout.
- **666 open issues** against a repo that publishes roughly weekly. Velocity is real; so is the backlog.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Every scripted assertion returned the right value — form flow, negative path, `is checked`/`is visible`, semantic locators. Exit codes distinguish failure from success |
| Speed | +/- | ~50 ms per non-pointer command is excellent; ~5,070 ms per pointer action is not, and a UI flow is mostly pointer actions |
| Maintainability | + | Semantic locators (`find label/role/testid`) survive markup churn without selector rewrites; no test code to keep |
| Safety | + | Local headless browser, `--allowed-domains`, action policies and confirmation categories exist (not exercised) |
| Cost Efficiency | + | `snapshot`/`read` return text, not images, so reading page state costs no image tokens — the opposite of what the previous review assumed |
| Verifiability | + | Every figure here is wall-clock around a pinned binary against a fixture in the eval, re-runnable in under a minute with no credentials |

## Comparison with Playwright MCP

Rewritten — the previous version of this table asserted four distinctions that the tool's own surface refutes.

| Dimension | agent-browser | Playwright MCP |
|-----------|---------------|----------------|
| Interface | CSS selectors, a11y refs, semantic locators (`find role\|label\|testid`) | Snapshot-ref / selector-based |
| Natural language | `chat` only, requires `AI_GATEWAY_API_KEY` | — |
| State readout | a11y tree with refs (53 ms) **or** markdown text — both cheap | YAML accessibility snapshot (no image) — verified |
| Transport | one-shot CLI against a persistent daemon; `--json` envelope | MCP tool calls in-session |
| Pointer latency | **~5,070 ms measured**, unconditional | not measured here |
| Screenshots | **failed 5/5 on this machine**; `pdf` works in 124 ms | — |

They are closer siblings than the previous table suggested. The honest difference is **shape, not paradigm**: agent-browser is a CLI you script from a shell or a Makefile, Playwright MCP is a tool surface inside a model session.

## Verdict

**CONDITIONAL** — adopt-if: you want a fast, scriptable selector/ref browser CLI to drive from a shell — **and you can absorb ~5 s per pointer action and do not depend on `screenshot`**.

The tool is good and the previous verdict undersold it in one direction while describing a different tool in another. Non-pointer commands answer in ~50 ms with correct exit codes and a clean `--json` envelope, semantic locators address a page with no CSS at all, and 5.0M npm downloads a month say plenty of people are getting value from it. As a shell-drivable verification primitive it is a strong CONDITIONAL.

What holds it back is measured, not suspected. **Every pointer action costs ~5,070 ms** — reproducibly, on a page with no listeners, no timers and no navigation, so it is a fixed cost rather than a wait on anything real. A ten-click smoke test spends fifty seconds doing nothing. And **`screenshot` failed 5 of 5 here**, twice taking over two minutes to fail, while `pdf` rendered the same page in 124 ms — scoped to this machine, but reproducible on it, and it is the capability the earlier review named as this tool's differentiator.

The corrections matter beyond the score. The prior review called intent-based commands *"the headline ergonomic difference from raw Playwright MCP"* and rated the learning curve *"Zero — describe what you want"*. The CLI's own first help screen refutes both: natural language is a single `chat` command behind `AI_GATEWAY_API_KEY`, and everything else takes a selector or a ref. It also gave agent-browser screenshots and Playwright MCP the cheap text snapshot, when agent-browser has `snapshot` **and** `read`, both text, both ~53 ms. Those errors all point the same way — a surface review inferring behaviour from positioning — and the stated blocker (*"needs an interactive browser session rather than a scriptable one-shot"*) is what prevented the fifteen-minute run that would have caught them.

**Sensible path:** use it for scripted verification where pointer actions are few — navigate, `fill`, `snapshot`, `get`, assert. Prefer `find label/role/testid` over CSS. Read state with `snapshot`/`read`, not `screenshot`; use `pdf` if you need a visual artifact. Re-evaluate toward ADOPT if the pointer-action cost drops or gains a documented opt-out, and if `screenshot` works on a second machine — the first is a design question for upstream, the second may be local.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-browser](https://github.com/vercel-labs/agent-browser) | tool | Fast one-shot browser automation CLI for agents — selectors, a11y refs, semantic locators (5.0M npm downloads/mo) | Agents can't interact with web UIs for testing, verification, or data extraction | playwright, browser-use |
