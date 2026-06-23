# Evaluation: AlphaGBM/skills

**Repo:** [AlphaGBM/skills](https://github.com/AlphaGBM/skills)
**Stars:** 951 | **Last updated:** 2026-05-27 (pushed; created 2026-04-06) | **License:** MIT
**Dev loop stage:** None of the software dev loop. This is a *domain* skill pack for options/equities trading and market research — it sits outside Plan/Implement/Verify/Review/Ship/Reflect entirely. The only loop-adjacent piece is `cli/` (a thin Python client you could read as a reference for skill→API wiring).
**Layer:** Process (29 single-file `SKILL.md` instruction packs that teach an agent to call the hosted AlphaGBM options-data API, plus mock JSON and a pip-installable CLI; no orchestration runtime)

---

## What it does

The catalog one-liner: "Real-data options intelligence for AI agents — 29 skills for financial options analysis." AlphaGBM is a **commercial, real-data options-intelligence layer** packaged as agent skills. The pitch is that every number (IV, HV, VRP, Greeks, skew, surface, flow) comes from the vendor's market-data API rather than from LLM guessing — the README explicitly contrasts itself with "LLM roleplay tools" that emit `"85% confidence"` hallucinations. The proprietary framing is `G = B + M` (Gain = Basics + Momentum) with quantitative 0–100 option / 1–10 stock scores.

As inspected the repo ships **29 `SKILL.md` files** under `skills/`, each named `alphagbm-*`: analysis (`stock-analysis`, `options-score`, `options-strategy`, `greeks`, `iv-rank`, `vol-surface`, `vol-smile`, `pnl-simulator`), research/persona signals (`buffett-analysis`, `marks-cycle`, `tepper-signal`, `duan-analysis`), sentiment/macro (`fear-score`, `vix-status`, `market-sentiment`, `macro-view`, `polymarket`), and workflow (`alert`, `watchlist`, `compare`, `take-profit`, `hedge-advisor`, `earnings-crush`, `unusual-activity`, `health-check`, `company-profile`, `investment-thesis`, `theme-research`, `bps-backtest`). Each skill mostly instructs the agent to hit `https://alphagbm.zeabur.app` endpoints; `mock-data/` holds demo JSON for AAPL/NVDA/SPY/TSLA/META so the skills "work" without a key, and `cli/` is a small Python package (`client.py`, `config.py`, `display.py`, `main.py`) that wraps the same API.

The business model is visible in the repo: free tier is **2 stock + 1 options analysis per day**, with Plus/Pro paid tiers, and live data requires `ALPHAGBM_API_KEY`. The skills are a free funnel to a paid hosted service.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run, no API key obtained.** No skill was cloned into `.claude/skills/`, the CLI was not `pip install`-ed, and no AlphaGBM endpoint was called. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, skill/commit counts), not from observed analysis output. The README's "10K users, 3mo live trading, real-time / battle-tested" copy is vendor marketing — I did not verify data freshness, accuracy, or any trading outcome, and the catalog should treat those numbers as unverified.

```bash
gh api repos/AlphaGBM/skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/AlphaGBM/skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/AlphaGBM/skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api "repos/AlphaGBM/skills/git/trees/HEAD?recursive=1" --jq '[.tree[]|select(.path|endswith("SKILL.md"))]|length'  # 29
gh api repos/AlphaGBM/skills/commits  --jq 'length'   # 17
gh api repos/AlphaGBM/skills/releases --jq 'length'   # 0
```

## What worked

- **Real-data-over-hallucination framing is the right instinct for finance.** Routing numeric questions (Greeks, IV rank, VRP, vol surface) to a deterministic API instead of letting the model invent figures is exactly how an agent *should* handle quantitative finance — this is the one genuinely transferable design lesson.
- **Clean, consistent skill packaging.** 29 uniformly named `alphagbm-*` skills, one `SKILL.md` each, installable by a single `git clone` into `.claude/skills/` or `.cursor/skills/`. Easy to read and to cherry-pick.
- **Bundled `mock-data/` lets you trial skills with zero signup** — AAPL/NVDA/SPY/TSLA/META demo JSON means the skills demonstrate behavior before you hit the paywall.
- **The `cli/` package is a usable reference** for the skill→hosted-API pattern (key config, client, display formatting) if you're building your own data-backed skill pack.

## What didn't work or surprised us

- **Hard dependency on a paid, single-vendor hosted API.** Beyond the five demo tickers, every skill needs `ALPHAGBM_API_KEY` and calls one vendor's `zeabur.app` endpoint. This is a thin instruction layer over a commercial SaaS, not a self-contained tool — if the service degrades, reprices, or disappears, the skills are inert. The free tier (2+1 analyses/day) is a funnel, not a usable allowance.
- **Unverifiable marketing as documentation.** "10K+ users," "3mo live trading," "battle-tested," "every number has a source" are README badges, not evidence in the repo. The competitor comparison table is vendor-authored. None of it is substantiated by anything inspectable.
- **Persona-signal skills are dressed-up subjectivity.** `buffett-analysis`, `tepper-signal`, `marks-cycle`, `duan-analysis` brand themselves as named-investor signals — the very "roleplay" the README claims to reject — layered on top of real data.
- **Zero relevance to building software.** Nothing here touches code, tests, review, or shipping. It is useful only if your *work itself* is options trading/market research.
- **No releases and low commit volume (17 commits, 0 tags).** You install whatever `main` is; there's no pinned, versioned bundle — and the README still carries `TODO: replace screenshot` placeholders.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (finance only) / n/a (software) | API-backed numbers beat LLM-invented figures *for trading questions*; irrelevant to code correctness. |
| Speed | neutral | Saves an analyst time pulling options data; no effect on a software dev loop. |
| Maintainability | neutral | Markdown skills + thin CLI; no effect on your codebase. Vendor-API coupling is a maintenance risk for *the skills*. |
| Safety | − | Skills send tickers to and pull data from a third-party hosted API; requires an API key (secret) and trusts an external service. Not financial advice, and outputs could drive real-money decisions. |
| Cost Efficiency | − | Real value sits behind paid Plus/Pro tiers; free tier is a 2+1/day funnel. |

## Verdict

**CONDITIONAL (finance-only) — keep in catalog as a domain pack; irrelevant to software development.** AlphaGBM/skills is a tidy, real-data options-intelligence layer for traders, with the genuinely sound instinct of routing quantitative questions to an API instead of the model. But it is a free funnel to a paid single-vendor SaaS, its "battle-tested / 10K users" claims are unverifiable vendor copy, and it has **no bearing on the AI-for-software-development loop**. Adopt only if options/market analysis is part of your actual work; otherwise SKIP. Keep the catalog row flagged domain-specific.

Compared to neighbors: like **pm-skills** and **marketingskills**, this is a non-software *domain* collection that belongs in the catalog only as an "if you do this work" reference. It is **narrower and more commercial** than either — pm-skills (100+) and marketingskills are broad, vendor-neutral, free skill packs, whereas AlphaGBM gates its real value behind a paid API for one narrow vertical (options). Versus the *other* finance pack [himself65/finance-skills](./himself65-finance-skills.md), AlphaGBM is single-vendor and options-centric; himself65 is multi-provider (yfinance, opencli, MCP) and broader, making AlphaGBM the more locked-in of the two.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [AlphaGBM/skills](https://github.com/AlphaGBM/skills) | skill | Real-data options intelligence for AI agents — 29 skills for financial options analysis | AI agents lack domain knowledge for options trading and financial analysis | himself65/finance-skills (broader, multi-provider finance pack); — (domain-specific: finance/options) |
