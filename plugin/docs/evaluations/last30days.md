# Evaluation: last30days-skill

**Repo:** [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)
**Stars:** 44,374 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Reflect (research informs next iteration) / Plan (pre-meeting, pre-build reconnaissance)
**Layer:** Tooling

---

## What it does

A research skill that searches Reddit, X/Twitter, YouTube, TikTok, Instagram, Hacker News, Polymarket, GitHub, Bluesky, Threads, Pinterest, Digg, Perplexity, and the web in parallel, then synthesizes what real people are actually saying about any topic in the last 30 days. The Python engine (`scripts/last30days.py`, 1,036 lines + 57 library modules) fans out searches across all configured platforms, scores results by engagement (upvotes, likes, views, money wagered), clusters them, and emits a compact synthesis the hosting AI model transforms into a narrative with inline citations.

The SKILL.md is 1,718 lines and acts as a strict behavioral contract with 8 "LAWs" governing output format, citation style, and failure mode prevention. The skill drives a full pre-flight resolution pipeline (X handles, GitHub users/repos, subreddit discovery, TikTok hashtags, Instagram creators, first-party positioning) before running the engine. A setup wizard handles first-run configuration for platform API keys. Supports five query types: GENERAL, NEWS, COMPARISON, RECOMMENDATIONS, and PROMPTING.

## How we tested it

**Evidence:** REVIEW

Inspected the installed skill at `~/.claude/skills/last30days/SKILL.md` (v3.3.2), examined all 57 Python library modules under `scripts/lib/`, reviewed the README, and assessed the architecture against Agent-Reach (34K stars), the closest catalog competitor.

```bash
# Skill installation (already present)
ls ~/.claude/skills/last30days/SKILL.md
# Engine inspection
wc -l ~/.claude/skills/last30days/scripts/last30days.py  # 1,036 lines
ls ~/.claude/skills/last30days/scripts/lib/ | wc -l       # 57 modules
```

Reviewed the engine's platform coverage by examining library modules: `reddit.py` + 5 Reddit variants (keyless, RSS, listing, shreddit, enrich), `bird_x.py` + `xurl_x.py` + `xai_x.py` (three X/Twitter backends), `youtube_yt.py`, `tiktok.py`, `instagram.py`, `hackernews.py`, `polymarket.py`, `github.py`, `bluesky.py`, `threads.py`, `pinterest.py`, `truthsocial.py`, `xiaohongshu_api.py`, `digg.py`, `perplexity.py`, `grounding.py` (web search).

## What worked

- **Extraordinary platform breadth.** 15+ data sources with dedicated scrapers, not just WebSearch wrappers. Reddit alone has 6 backend modules for different access methods (public JSON, RSS, keyless API, Shreddit, listing, enrichment). This is real engineering, not prompt wrapping.
- **Engagement-weighted scoring.** Results ranked by upvotes, views, likes, and wagered money (Polymarket). A 1,500-upvote Reddit thread outranks a zero-traffic blog post. This produces genuinely different results from Google or ChatGPT.
- **Rigorous output contract.** The 8 LAWs prevent the most common AI synthesis failure modes: invented titles, trailing Sources blocks, em-dashes, section headers in narrative body, raw evidence dumps. Each LAW cites the specific failure date and run that motivated it. This is battle-tested iterative improvement.
- **Pre-flight intelligence pipeline.** Step 0.5/0.55/0.75 resolve handles, repos, and communities before running the engine, producing targeted platform-specific queries rather than keyword-only search.
- **Comparison mode.** `X vs Y vs Z` queries fan out N full pipeline passes in parallel with per-entity targeting, producing side-by-side tables with live data (star counts from GitHub API, not stale blog posts).
- **Shareable HTML briefs.** `--emit=html` produces self-contained, dark-mode, print-friendly files for Slack/email/Notion. No JavaScript, no external dependencies.
- **Zero-config baseline.** Reddit, HN, Polymarket, and GitHub work immediately. Setup wizard progressively unlocks X, YouTube, TikTok, etc.

## What didn't work or surprised us

- **1,718-line SKILL.md is a context budget risk.** At ~38K tokens, it consumes a significant chunk of context window on every invocation. The skill acknowledges this - the LAWs were hoisted to the top specifically because models couldn't reach line 1224. Effective but expensive.
- **Heavy dependency footprint.** Requires Python 3.12+, node, and optionally 10+ API keys/tokens for full coverage. The setup wizard helps but the full platform matrix (ScrapeCreators for TikTok/Instagram, browser cookies for X, yt-dlp for YouTube) is a significant configuration surface.
- **Defensive specification overhead.** The SKILL.md documents 8+ named failure modes from specific dates (Peter Steinberger disaster #2, Hermes Agent Use Cases disaster, etc.) with multi-paragraph explanations. This is valuable for reliability but increases the token cost per invocation substantially.
- **Not a quick lookup.** A full research run takes 2-5 minutes of engine execution time plus pre-flight WebSearches. This is research infrastructure, not a quick-answer tool.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Engagement-weighted scoring surfaces what real communities actually discuss, not SEO-optimized content |
| Speed | + | Replaces hours of manual multi-platform research with a 2-5 minute automated sweep |
| Maintainability | neutral | Does not affect codebase maintainability directly |
| Safety | neutral | Reads public data only; no code generation or modification |
| Cost Efficiency | - | ~38K tokens for SKILL.md context + multiple WebSearch calls + engine execution; high per-invocation cost |

## Verdict

**ADOPT**

The most comprehensive social intelligence skill available - 15+ platforms with dedicated scrapers, engagement-weighted scoring, and a battle-hardened output contract that prevents common AI synthesis failures. The token cost is high (~38K for the SKILL.md alone) but justified by the quality of output: no other tool produces engagement-ranked, multi-platform research synthesis with inline citations and shareable HTML briefs. Use it for pre-meeting research, competitive analysis, trend monitoring, and any "what are people actually saying" question. Agent-Reach (34K stars) covers similar platforms at the data collection layer but lacks the synthesis contract, engagement scoring, query planning pipeline, and comparison mode that make last30days a complete research product rather than just a data pipe.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [last30days-skill](https://github.com/mvanhorn/last30days-skill) | skill | Research any topic across Reddit, X, YouTube, HN, Polymarket, and the web | Need current sentiment and discussion, not just static docs | Agent-Reach |
