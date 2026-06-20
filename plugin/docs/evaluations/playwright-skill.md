# Evaluation: playwright-skill

**Repo:** [lackeyjb/playwright-skill](https://github.com/lackeyjb/playwright-skill)
**Stars:** 2,791 | **Last updated:** 2025-12-19 (pushed; created 2025-10-19 — ⚠️ ~6 months stale at evaluation) | **License:** MIT
**Dev loop stage:** Verify (browser automation for testing/validation)
**Layer:** Process/Tooling (a Claude Code skill)

---

## What it does

playwright-skill is a **Claude Code skill for browser automation with Playwright**. It's model-invoked: rather than exposing a fixed tool surface, Claude autonomously writes and executes custom Playwright automation for testing and validation when the skill triggers. In effect it's the *skill packaging* of "drive a browser with Playwright" — the agent generates the automation code on demand.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill installed, no automation executed. Claims come from the repository (GitHub metadata, description) and comparison against the catalog's existing browser-automation coverage.

```bash
gh api repos/lackeyjb/playwright-skill --jq '{stars,created_at,pushed_at,license:.license.spdx_id}'
grep -nE "playwright|agent-browser|chrome-devtools-mcp|browser-use" CATALOG.md   # existing coverage
```

## What worked

- **Skill form is ergonomically distinct.** A model-invoked skill that *writes* Playwright automation on demand is a different packaging from the MCP/CLI options — no fixed tool schema, the agent composes exactly the automation it needs.
- **Simple, MIT, no infra.** It's just a skill; trivial to drop in for a Claude Code user who wants Playwright-style validation.

## What didn't work or surprised us

- **Redundant with stronger, maintained options.** The catalog already covers this capability well: **playwright** (Microsoft's official Playwright MCP — **ADOPT**), **agent-browser** (Vercel's browser-automation CLI — **ADOPT**), plus browser-use and chrome-devtools-mcp. The MCP/CLI forms give a stable, maintained tool surface; a skill that hand-writes Playwright each time is more variable and harder to reason about.
- **⚠️ Stale.** Last pushed 2025-12-19 — roughly six months before evaluation, with no activity since. Browser automation + Claude Code both move fast; an unmaintained skill is a liability versus the actively-maintained alternatives.
- **No verification advantage.** It doesn't add caching, self-healing selectors, or inspection that the neighbors lack (cf. passmark's auto-healing selectors, chrome-devtools-mcp's inspection).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Model-generated automation each run is more variable than a stable tool surface. |
| Speed | neutral | Comparable to alternatives; no distinctive speed feature. |
| Maintainability | − | Unmaintained (~6 months); model-written automation is less repeatable than configured tools. |
| Safety | neutral | Standard browser-automation trust model. |
| Cost Efficiency | neutral | Free/MIT. |

## Verdict

**SKIP** — evaluated and not recommended for the stack. It's a fine idea (a model-invoked skill that writes Playwright automation), but the capability is already covered by **maintained, higher-quality options** in the catalog: the official **playwright** MCP and **agent-browser** CLI (both ADOPT), with browser-use and chrome-devtools-mcp filling autonomous-agent and inspection niches. Combined with ~6 months of staleness, there's no reason to choose this over those. Use the playwright MCP or agent-browser instead; reach for passmark when you specifically need self-healing regression tests.

Compared to neighbors: **playwright** (MCP) and **agent-browser** (CLI) are the maintained, stable-surface equivalents; **browser-use** is the autonomous browser agent; **chrome-devtools-mcp** adds inspection/profiling; **passmark** adds AI regression testing with auto-healing selectors. playwright-skill is the stale, skill-form duplicate of the first two — superseded.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [playwright-skill](https://github.com/lackeyjb/playwright-skill) | skill | Claude Code skill where the model writes & runs custom Playwright browser automation on demand for testing/validation (⚠️ ~6 months stale) | Want browser automation as a model-invoked skill rather than a fixed MCP/CLI tool surface | playwright, agent-browser, browser-use, chrome-devtools-mcp |
