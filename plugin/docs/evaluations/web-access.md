# Evaluation: Web Access (web-access)

**Repo:** [eze-is/web-access](https://github.com/eze-is/web-access)
**Stars:** 7,739 | **Last updated:** 2026-05-16 (pushed) | **License:** ⚠️ none declared | **Language:** JavaScript (SKILL.md skill; primarily 中文 docs)
**Dev loop stage:** Skills & Plugins / Verify — gives agents full web access
**Layer:** Tooling (agent skill, SKILL.md-compatible)

---

## What it does

web-access is **an Agent Skill that gives SKILL.md-compatible agents (Claude Code, Cursor, Gemini CLI, Codex CLI) full web capability** beyond the built-in WebSearch/WebFetch, which "lack scheduling strategy and browser automation." It adds **networking strategy + CDP browser control + per-site experience accumulation**. v2.5 capabilities: automatic tool selection (WebSearch / WebFetch / curl / Jina / CDP, combinable per scenario); **CDP Proxy browser control** against the user's *real* daily browser (Chrome/Edge/Chromium) — inheriting logged-in state, handling dynamic pages, interactions, and **video frame-grab**; three click modes (`/click` JS, `/clickAt` real CDP mouse, `/setFiles` upload); **local bookmark/history search** (`find-url.mjs`) across Chrome/Edge to reach internal systems the public web can't; **parallel sub-agent dispatch** sharing one proxy with tab-level isolation; **per-domain experience accumulation** (URL patterns, platform quirks, known traps) reused across sessions; and media extraction from the DOM.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill installed, no browser driven; README is primarily Chinese (read via translation).

```bash
gh api repos/eze-is/web-access --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 7739, license=null, pushed 2026-05-16
gh api repos/eze-is/web-access/readme --jq '.content' | base64 -d | sed -n '343,400p'        # CDP proxy, tool selection, find-url, parallel sub-agents
```

## What worked

- **Logged-in, real-browser access is the key idea.** Driving the user's *actual* Chrome/Edge via CDP inherits session/cookies, so the agent can reach authenticated and internal pages that headless tools and WebFetch can't — a genuinely higher ceiling than built-in web tools.
- **Strategy layer, not just a tool.** Auto-selecting among WebSearch/WebFetch/curl/Jina/CDP per scenario (and combining them) is smarter than a single fixed fetch path, and directly targets WebFetch's context-bloat/JS-page weaknesses.
- **Per-domain experience accumulation.** Storing site know-how (URL patterns, traps) and reusing it across sessions is a compounding capability most browser tools lack.
- **Parallelism + local history search.** Sub-agent fan-out over one shared proxy and bookmark/history lookup (`find-url.mjs`) are thoughtful, practical features.
- **Agent-agnostic + popular.** SKILL.md format works across Claude Code/Cursor/Gemini/Codex; 7.7K stars.

## What didn't work or surprised us

- **No license declared.** A skill with **no LICENSE** is a real adoption blocker for many — usage/redistribution rights are unclear; treat as "all rights reserved" until clarified.
- **Driving your real browser is a powerful, sensitive capability.** CDP control of your logged-in Chrome/Edge with file upload and real mouse events is high-trust: the agent can act as you on authenticated sites. That's the feature and the risk — needs careful permissioning.
- **Primarily Chinese docs.** README/design essays are mostly 中文; non-Chinese users lean on translation, raising the bar to configure CDP correctly.
- **Setup friction.** Requires enabling remote debugging on the browser and managing `config.env`/proxy pinning — more involved than an MCP one-liner.
- **Overlaps the browser-tool field.** Conceptually near agent-browser/browser-use/playwright; the wedge is real-logged-in-browser + strategy + site memory as a portable *skill*.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Logged-in real-browser access + strategy reach pages WebFetch can't, so agents work from real data. |
| Speed | + / neutral | Parallel sub-agents + cached site experience speed multi-target work; CDP setup adds upfront effort. |
| Maintainability | neutral | Per-domain experience is reusable; managing browser debug + proxy config is ongoing overhead. |
| Safety | − / neutral | Driving your authenticated browser (uploads, real clicks) is high-trust; no license adds legal uncertainty. |
| Cost Efficiency | + | Smart tool selection avoids WebFetch's 20k-token dumps; reuse of site experience cuts re-discovery. |

## Verdict

**CONDITIONAL** (with caveats) — web-access is a capable, popular **web-access skill** whose standout idea is driving the user's **real, logged-in Chrome/Edge via CDP** with a tool-selection strategy and **per-domain experience accumulation** — reaching authenticated/internal pages and dynamic content that built-in WebSearch/WebFetch and headless tools miss. Adopt it when an agent genuinely needs logged-in, interactive web access (internal dashboards, authenticated flows, video frame analysis) and you can navigate the setup. Two real caveats keep it CONDITIONAL: **no declared license** (resolve rights before any non-personal use) and the **high-trust nature of letting an agent act as you in your real browser** (permission carefully). Chinese-first docs add friction for others. For simpler, lower-trust automation, agent-browser/playwright are more conventional.

Compared to neighbors: **agent-browser** is a CLI browser-automation tool for agents; **browser-use** is an autonomous web agent; **playwright** automates a controlled browser; **exa-mcp-server** is web search. web-access's distinguishing pitch is **a portable skill that drives your real logged-in browser via CDP, with a networking strategy and reusable per-site experience.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [web-access](https://github.com/eze-is/web-access) | skill | Full web-access skill for SKILL.md agents (⚠️ no license declared; primarily 中文 docs) — adds networking strategy + CDP browser control over your real logged-in Chrome/Edge (dynamic pages, clicks, uploads, video frame-grab), local bookmark/history search, parallel sub-agents, and per-domain experience accumulation | Built-in WebSearch/WebFetch lack scheduling and real-browser automation; want logged-in, interactive web access with reusable site know-how | agent-browser, browser-use, playwright, exa-mcp-server |
