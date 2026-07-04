# Evaluation: Awesome-finance-skills

**Repo:** [RKiding/Awesome-finance-skills](https://github.com/RKiding/Awesome-finance-skills)
**Stars:** 2,569 | **Last commit:** 2026-03-29 | **Created:** 2026-01-31 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Discover (outer loop)
**Layer:** Infrastructure

---

## What it does

Despite the "Awesome-" name, this is **not** an awesome-list of links — it is a packaged collection of nine installable finance agent skills (the "AlphaEar" family) plus a `skill-creator`, all living under `skills/` with per-skill `SKILL.md` files. The pitch is "turn your AI agent into a Wall Street analyst": each skill bolts a finance capability onto an LLM. The bundle is bilingual (English / 中文) and the README documents install paths for Antigravity, OpenCode, OpenClaw, and Claude Code / Codex, plus one-step install via `npx skills add RKiding/Awesome-finance-skills@<skill>`.

The included skills: `alphaear-news` (real-time financial news/trends from 10+ sources including Cailian, WSJ, Weibo, Polymarket), `alphaear-stock` (A-Share/HK/US OHLCV + fundamentals), `alphaear-sentiment` (FinBERT/LLM sentiment scoring), `alphaear-predictor` (Kronos time-series forecasting with news-aware adjustments), `alphaear-signal-tracker`, `alphaear-logic-visualizer` (draw.io transmission-chain diagrams), `alphaear-reporter`, `alphaear-search` (Jina/DDG/Baidu + local RAG), and `alphaear-deepear-lite`. It is the skills front-end to the author's larger [DeepEar/AlphaEar](https://github.com/RKiding/AlphaEar) autonomous-analysis framework.

## How we tested it

**Evidence:** REVIEW

Source-grounded inspection only — we did not install or run any skill (and would not connect it to live market data sources without scrutiny). We pulled metadata, README, last-commit recency, the file tree, the `skills/` listing, and one representative `SKILL.md` via the GitHub API.

```
gh api repos/RKiding/Awesome-finance-skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/RKiding/Awesome-finance-skills/commits --jq '.[0].commit.committer.date'   # 2026-03-29
gh api repos/RKiding/Awesome-finance-skills/contents/skills --jq '.[].name'
gh api repos/RKiding/Awesome-finance-skills/contents/skills/alphaear-news/SKILL.md --jq '.content' | base64 -d | head -30
```

This was requested as a reference/awesome-list evaluation; the honest finding is that it is a **skill bundle**, not a curated link list, which changes the verdict framing below.

## What worked

- **Genuinely installable, coherent skill family.** Nine domain skills under one repo with consistent `SKILL.md` structure (proper `name`/`description` frontmatter, capabilities, dependencies). This is a real skill collection, not a README of pointers — closer to AlphaGBM/skills than to awesome-claude-code.
- **Cross-harness install is well documented.** Explicit install paths for Antigravity, OpenCode, OpenClaw, Claude Code, and Codex, plus `npx skills` one-step install. Portable beyond a single agent.
- **Bilingual and tied to a real framework.** The EN/中文 docs and the link to the upstream DeepEar/AlphaEar project signal this is a maintained productized effort, not a throwaway.
- **Niche is genuinely underserved in our catalog.** The only finance-domain neighbor we carry is AlphaGBM/skills (options analysis). General financial news/sentiment/forecasting agent skills are otherwise absent.

## What didn't work or surprised us

- **The name is misleading.** "Awesome-finance-skills" reads as an awesome-list; it is actually a skill bundle. Anyone cataloging it as a `reference` link list (as the task framed it) would be wrong — Type is `skill`, not `reference`.
- **Out of scope for an AI-coding-tooling catalog.** This repo is a *vertical-domain* (financial analysis) skill pack. Our catalog is organized around the software dev loop and code quality; finance market analysis has near-zero intersection with Plan/Implement/Verify/Review/Ship. Like AlphaGBM/skills, it earns at most a domain-specific footnote, not a core slot.
- **Trust and freshness concerns for live-data skills.** Skills like `alphaear-news`, `alphaear-stock`, and `alphaear-search` fetch from external sources (WSJ, Weibo, Baidu, Polymarket, Jina) via bundled Python scripts. Those endpoints rot, and we did not audit the scripts for credential handling or scraping fragility. Financial decisions on top of unvetted scrapers is a real safety hazard.
- **Last commit 2026-03-29 — ~3 months stale at evaluation.** Not abandoned, but for a niche project depending on volatile data sources, freshness matters and the cadence has slowed since the early-2026 burst.
- **No license/quality flags on the data sources, and forecasting (Kronos) skills imply correctness claims** the repo cannot substantiate from a README.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Domain skills — no effect on *code* correctness; their own market-analysis accuracy is unverified |
| Speed | neutral | Niche relevance to the dev loop; no measurable effect on engineering velocity |
| Maintainability | neutral | No impact on a codebase |
| Safety | − | Bundled scrapers hit volatile external sources; unaudited scripts feeding finance decisions; no source-health flags |
| Cost Efficiency | neutral | Free/open, but irrelevant to dev-loop cost; live-data calls add their own token/API overhead |

## Verdict

**SKIP**

It is a well-organized, cross-harness finance skill bundle and the niche is real — but it is a vertical-domain pack, not an AI-coding-tooling resource, so it sits almost entirely outside this catalog's scope. The closest neighbor, AlphaGBM/skills (finance/options), is carried only as a domain-specific footnote, and Awesome-finance-skills belongs in the same marginal tier at best. If we do record it, the honest Type is `skill` (a bundle), not `reference` — the "Awesome-" name does not make it a curated list. Add it only as a niche pointer for users who explicitly want finance-domain agent skills; do not feature it. Re-evaluate only if the dev-loop relevance changes (it won't) or if it pivots into a genuinely curated cross-author list.

## Catalog entry

If recorded, place under **Reference** as a niche domain pointer (paralleling the AlphaGBM/skills footnote treatment). Note the Type is `skill`, not `reference` — the repo is a bundle, not a curated list.

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Awesome-finance-skills](https://github.com/RKiding/Awesome-finance-skills) | skill | Bundle of 9 bilingual (EN/中文) finance agent skills — news, stock data, sentiment, Kronos forecasting, logic diagrams (2.6K stars) | AI agents lack finance-domain capabilities (real-time news, market data, sentiment, forecasting) | AlphaGBM/skills (finance/options) |
