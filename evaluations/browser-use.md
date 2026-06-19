# Evaluation: browser-use

**Repo:** [browser-use/browser-use](https://github.com/browser-use/browser-use)
**Stars:** 99,580 | **Last updated:** 2026-06-15 | **License:** MIT
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Catalog one-liner: "AI browser agent for autonomous web interaction" — solves "Need agents to navigate and interact with web pages autonomously."

The catalog files browser-use as an "MCP server," but that undersells what it actually is. browser-use is primarily a **Python agent framework** for building autonomous, LLM-driven browser agents. You hand it a natural-language task ("Find the number of stars of the browser-use repo") and an LLM; the agent then plans and executes a multi-step loop — read page state, decide the next action, click/type/navigate, observe, repeat — until it judges the task complete. As of 0.13 the action loop runs on a Rust core ("Python API -> Rust core -> Browser harness -> Web task done") with recovery loops inspired by coding agents. It ships three usage surfaces relevant to a Claude Code dev loop:

1. **Library** (`from browser_use.beta import Agent`) — build your own autonomous web agents. This is the product's center of gravity.
2. **Stateful CLI** (`browser-use open/state/click/type/screenshot/close`) — keeps a browser alive between commands for fast iteration; agent drives discrete actions by element index.
3. **Claude Code skill** (curl the `SKILL.md` into `~/.claude/skills/browser-use/`) — the most direct way to use it inside a Claude Code Verify loop.

MCP is offered as one more integration ("custom tools, MCP, and more on our Docs"), so the catalog's "MCP server" type is technically available but is not how most people use it. The defining characteristic for evaluation purposes is **autonomy**: browser-use is goal-driven (you give intent, the LLM figures out the steps), whereas Playwright MCP is action-driven (you specify each step) and agent-browser is intent-per-action.

There is a heavily-promoted hosted **Cloud** offering (stealth browsers, proxy rotation, CAPTCHA solving, 1000+ integrations) layered on top of the OSS core; the OSS library is MIT and free, but production scaling is steered toward the paid cloud.

## How we tested it

Method, stated honestly: **inspected the GitHub repo metadata, the full README, and the documented CLI/skill/library surfaces. Did not install or run the agent against a live site.** No hands-on metrics below are invented — where I lack first-hand numbers I say so and reason from the architecture and from our two calibration evals (agent-browser ADOPT, Playwright MCP ADOPT), which were tested hands-on on local dev servers.

```bash
# Metadata
gh api repos/browser-use/browser-use --jq '{stars,license,description,pushed_at}'
# -> 99,580 stars, MIT, actively pushed (2026-06-15)

# Surfaces reviewed (not executed):
uvx browser-use init --template default      # scaffold a starter agent
browser-use open https://example.com         # stateful CLI navigate
browser-use state                            # list clickable elements
browser-use click 5                          # act by element index
# Claude Code skill install:
curl -o ~/.claude/skills/browser-use/SKILL.md \
  https://raw.githubusercontent.com/browser-use/browser-use/main/skills/browser-use/SKILL.md
```

For the dev-loop comparison I leaned on the existing hands-on evals of the two overlapping tools rather than re-deriving their behavior.

## What worked

- **Massive, current ecosystem.** ~99.6K stars, 11K forks, MIT, pushed within days — this is the dominant OSS browser-agent project, not an experiment. Low abandonment risk.
- **True autonomy is real value for the long tail.** For multi-step, exploratory, or under-specified web tasks ("apply to this job with my resume," "find PC parts and compare") where you cannot enumerate the steps up front, a goal-driven agent is the right shape. Playwright MCP and agent-browser both require you (the orchestrating agent) to drive each action.
- **Stateful CLI is a clean fit for an agent loop.** Persisting the browser across `open/state/click` commands and acting by element index avoids re-navigation cost and gives Claude Code a low-friction way to step through a page.
- **Pluggable LLMs.** Works with Claude (`ChatAnthropic`/`ChatBrowserUse(model='anthropic/...')`), GPT, Gemini, or local Ollama — no lock-in at the model layer for the OSS path.
- **Published benchmark.** A 100-task open benchmark (browser-use/benchmark) exists, which is more rigor than most tools in this category offer.

## What didn't work or surprised us

- **Autonomy is overkill — and a liability — for deterministic UI verification.** Our Verify loop wants a repeatable, cheap, fast check that "the form submits and shows Welcome." A planning LLM choosing its own steps each run is non-deterministic, slower (an LLM call per decision step), and harder to assert against than Playwright MCP's `browser_click` + `browser_snapshot`. For the catalog's stated problem (verify UIs in the dev loop), this is the wrong abstraction.
- **Cost profile is materially worse for verification.** Each autonomous step burns an LLM call. agent-browser and Playwright MCP let the *already-running* Claude Code session drive actions directly; browser-use adds a second nested agent loop. That is real token/latency cost for verification work.
- **Type mismatch in the catalog.** Listed as "MCP server," but the product is a library/framework first; MCP is a side integration. The "How it's used in a Claude Code Verify loop" answer is really "via the Claude Code skill or the stateful CLI," not an MCP server.
- **Strong commercial pull toward Cloud.** The README repeatedly routes production, stealth, CAPTCHA, and scaling to the paid hosted product. Fine for the use case browser-use targets (scraping/automation against third-party sites), but irrelevant-to-mildly-distracting for verifying your own local dev server.
- **Beta churn.** The 0.13 Rust core + `browser_use.beta` Agent is new; the autonomous agent surface is explicitly beta, so expect API movement.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (for autonomous tasks) / neutral (for UI verification) | Goal-driven loop completes under-specified multi-step web tasks; but non-determinism makes it weaker than Playwright MCP for repeatable assertions |
| Speed | - | An LLM call per decision step; slower than agent-browser's ~3-5s/action and far slower than Playwright MCP's ~1-2s/action for verification |
| Maintainability | neutral | No selector test code to maintain, but beta API churn and a nested-agent layer add moving parts |
| Safety | neutral/- | Autonomous agent acting on web pages widens blast radius; mitigated by `allowed_domains` allowlist in `BrowserProfile` |
| Cost Efficiency | - | Nested autonomous loop roughly doubles LLM spend vs driving the browser from the existing Claude Code session |

## Verdict

**CONDITIONAL**

Use browser-use when the task is **genuinely autonomous web automation** — under-specified, multi-step, or exploratory tasks against external sites where the steps can't be enumerated up front (form-filling from a resume, cross-site research, scraping workflows). For that job it is the strongest OSS option in existence (99.6K stars, MIT, active, benchmarked) and earns a place in the catalog.

For the catalog's *stated* problem — verifying your own UI in the Claude Code Verify loop — it is **redundant with and inferior to** the two ADOPT tools we already have. Playwright MCP gives deterministic, fast, cheap, assertable checks; agent-browser gives zero-setup intent-based exploratory verification driven by the session you already have running. browser-use's autonomous planning loop adds latency, token cost, and non-determinism that verification does not want. It is additive to the catalog (it covers autonomous automation, which neither ADOPT tool targets), but it does not displace either for visual/UI verification. Adopt only when the autonomy is the point; otherwise reach for Playwright MCP or agent-browser. Recommend correcting the catalog Type from "MCP server" to "framework" (or "tool") to reflect what it actually is.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [browser-use](https://github.com/browser-use/browser-use) | framework | Autonomous LLM-driven browser agent for goal-based web tasks | Agent must complete under-specified, multi-step web tasks without scripted steps | playwright, agent-browser, chrome-devtools-mcp |
