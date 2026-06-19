# Evaluation: himself65/finance-skills

**Repo:** [himself65/finance-skills](https://github.com/himself65/finance-skills)
**Stars:** 2,851 | **Last updated:** 2026-06-14 (pushed; created 2026-03-13) | **License:** MIT
**Dev loop stage:** None of the software dev loop. This is a *domain* collection for financial analysis/trading — it sits outside Plan/Implement/Verify/Review/Ship/Reflect. The loop-adjacent exception is the bundled **`finance-skill-creator`** plugin (a skill-authoring/quality-scoring skill) and the `opencli-plugins/` JS adapters, which are reusable patterns rather than dev tooling.
**Layer:** Process (25 `SKILL.md` packs grouped into 6 installable Claude Code plugins via a `marketplace.json`; backed by yfinance, opencli adapters, and external MCP/REST APIs — no orchestration runtime)

---

## What it does

The catalog one-liner would be: "A collection of skills for AI financial analysis." himself65/finance-skills is a **multi-provider financial-analysis skill marketplace** following the [Agent Skills](https://agentskills.io) open standard, installable as a whole or as six discrete plugins. As inspected it ships **25 `SKILL.md` files** across `plugins/`, organized as:

- **finance-market-analysis (11 skills)** — `company-valuation` (DCF + relative + SOTP), `earnings-preview`/`earnings-recap`, `estimate-analysis`, `etf-premium`, `options-payoff`, `saas-valuation-compression`, `sepa-strategy` (Minervini VCP), `stock-correlation`, `stock-liquidity`, `yfinance-data`. These run on the open-source **yfinance** library, not a paid API.
- **finance-social-readers (6 skills)** — read-only research feeds (`twitter-reader`, `discord-reader`, `linkedin-reader`, `telegram-reader`, `yc-reader`, and `opencli-reader`, a generic fallback for 90+ sources) via [opencli](https://github.com/jackwener/opencli) + `tdl`.
- **finance-data-providers (5 skills)** — `finance-sentiment` (Adanos), `funda-data` (sponsor Funda AI MCP + REST), `hormuz-strait` (geopolitical/oil monitoring), `tradingview-reader` and `hyperliquid-reader` (read-only via opencli + CDP/public API).
- **finance-startup-tools (1)** — `startup-analysis` (VC / applicant / founder perspectives).
- **finance-ui-tools (1)** — `generative-ui` (renders interactive HTML/SVG widgets via `show_widget`).
- **finance-skill-creator (1)** — a skill-authoring helper with quality scoring.

Distribution is mature: a `.claude-plugin/marketplace.json`, install via `npx plugins add himself65/finance-skills` (all) or `--plugin <name>` (individual), plus `npx skills add … -a <agent>` for other agents. The repo also vendors its own **opencli JS adapters** (`opencli-plugins/hyperliquid`, `opencli-plugins/tradingview`) with unit tests. It is **sponsored by Funda AI**, which the README openly upsells as the paid "hundreds of skills" tier — but unlike AlphaGBM, the core skills here are vendor-neutral and run on free/open data.

## How we tested it

**Source-grounded inspection — not installed, not run, no agent invoked.** No plugin was `npx plugins add`-ed, no skill was activated, yfinance/opencli were not called, and no Funda/Adanos/Hyperliquid endpoint was hit. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, skill/plugin/commit/release counts), not from observed output. Data accuracy, freshness, and any trading utility are unverified; the WARNING banner ("not financial advice") is the authors'.

```bash
gh api repos/himself65/finance-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/himself65/finance-skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/himself65/finance-skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "repos/himself65/finance-skills/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'  # 25
gh api repos/himself65/finance-skills/commits      --jq 'length'   # 30 (page-1 cap)
gh api repos/himself65/finance-skills/releases     --jq 'length'   # 19
gh api repos/himself65/finance-skills/contributors --jq '[.[].login]'  # himself65, Fallenhh
```

## What worked

- **Multi-provider and largely vendor-neutral.** Core market analysis runs on open-source **yfinance**; research feeds run on open **opencli** adapters. Real value isn't paywalled the way AlphaGBM's is — the Funda AI sponsor tier is an optional upsell, not a gate.
- **Genuinely mature distribution.** A proper `marketplace.json` with six installable plugins, `npx plugins add … --plugin <name>` granularity, multi-agent install (`-a <agent>`), **19 tagged releases**, and CI (`skill-lint.yml`, `release-skills.yml`, `opencli-plugin-test.yml`) — more release/packaging discipline than most domain packs in this catalog.
- **Breadth with depth.** `company-valuation` does DCF + relative + SOTP triangulation with WACC×g sensitivity and Bull/Base/Bear scenarios; `sepa-strategy` encodes Minervini's trend template; `opencli-reader` fans out to 90+ sources. This is analyst-grade scope, not toy skills.
- **`finance-skill-creator` and the vendored opencli adapters are reusable beyond finance.** The skill-authoring/quality-scoring skill and the tested JS adapter pattern (`lib/` + `tests/`) are transferable references for building your own data-backed skills.

## What didn't work or surprised us

- **Zero relevance to building software.** As with any finance domain pack, nothing here touches code, tests, review, or shipping. It helps only if financial analysis *is* your work.
- **Thin contributor base for the star count.** 2.8K stars but effectively **two contributors** (himself65, Fallenhh). The traction is one maintainer + a sponsor, not a broad community — bus-factor risk for a 25-skill surface.
- **External-dependency surface is large and fragile.** Skills lean on yfinance (unofficial scraping, breaks often), opencli + `tdl` + CDP browser automation, plus third-party APIs (Funda, Adanos, Hyperliquid). Many moving parts that can rot independently, and several "readers" automate logged-in sessions (Twitter, Discord, TradingView) with the brittleness and ToS exposure that implies.
- **Sponsor entanglement.** The README leads with a Funda AI banner and upsell; `funda-data` is a first-class skill. Vendor-neutral at the core, but the commercial pull is overt.
- **Read-only social automation invites account/ToS risk.** `twitter-reader`, `discord-reader`, `linkedin-reader`, `telegram-reader` drive real authenticated sessions — useful, but a safety/compliance footgun for the unwary.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (finance only) / n/a (software) | yfinance/API-backed numbers and structured valuation frameworks beat LLM guessing *for finance*; irrelevant to code correctness. |
| Speed | neutral | Saves an analyst time on data pulls and valuations; no effect on a software dev loop. |
| Maintainability | neutral | Markdown skills + JS adapters; no effect on your codebase. Heavy external-dependency surface is a maintenance risk for *the skills*. |
| Safety | − | Browser/CDP automation of logged-in social and trading accounts; third-party API keys; outputs could drive real-money decisions (authors disclaim advice). |
| Cost Efficiency | + / neutral | Core skills run on free yfinance/opencli — better free utility than single-vendor paid packs; optional Funda tier costs money. |

## Verdict

**CONDITIONAL (finance-only) — strong addition to the catalog as a domain pack; irrelevant to software development.** himself65/finance-skills is the most polished finance skill collection inspected: multi-provider, vendor-neutral at the core, with real release/packaging discipline and analyst-grade depth. But it has **no bearing on the AI-for-software-development loop** — adopt only if financial analysis is part of your actual work; otherwise SKIP. The thin (2-person) maintainer base and large external-dependency surface are the main caveats. Add to the catalog flagged domain-specific (finance).

Compared to neighbors: like **pm-skills** (100+) and **marketingskills**, this is a broad, free, vendor-neutral *domain* collection that belongs in the catalog as an "if you do this work" reference — and it sits naturally beside them as the finance entry. Versus the other finance pack [AlphaGBM/skills](./AlphaGBM-skills.md), himself65 is clearly **broader and less locked-in**: AlphaGBM gates its real value behind a single paid options API, while himself65 runs core skills on open yfinance/opencli and offers six independently installable plugins. For anyone doing finance work, himself65 is the better default; AlphaGBM is the narrower options-specialist alternative.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [himself65/finance-skills](https://github.com/himself65/finance-skills) | skill | Multi-provider financial-analysis skill pack — 25 skills in 6 plugins (valuation, earnings, options, social/data readers) on yfinance + opencli | AI agents lack domain knowledge and live-data access for financial analysis and trading research | AlphaGBM/skills (narrower, single-vendor options pack); pm-skills, marketingskills (other domain packs); — (domain-specific: finance) |
