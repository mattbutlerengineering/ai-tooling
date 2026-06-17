# New Tools Evaluation (Loop 8)

Final batch — high-star research and discovery tools from the catalog.

## last30days-skill
**Repo:** [mvanhorn/last30days-skill](https://github.com/mvanhorn/last30days-skill)
**Stars:** 42,980 | **Last updated:** 2026-06-10 | **Forks:** 3,507
**What it does:** Claude Code skill that fans out searches across Reddit, X/Twitter, YouTube, TikTok, Hacker News, Polymarket, GitHub, and the broader web simultaneously, scoring results by engagement and freshness. Deduplicates across platforms and synthesizes a cited brief. The `--competitors` flag and comparison syntax (`A vs B vs C`) make it useful for tool-selection research.
**Current workflow alternative:** WebSearch and context7 cover web and documentation lookup. No existing tool covers social-signal-first community sentiment research.
**Key difference:** Explicitly social-signal-first — weights Reddit upvotes, X engagement, Polymarket prediction odds, and GitHub PR velocity as ranking signals. Optimized for "what is the community saying right now" rather than "what is objectively true."

**Verdict:** CONDITIONAL at L3+ for tool evaluation and adoption decisions
**Justification:** Fills a distinct niche: rapid community sentiment on libraries, frameworks, and tools before adoption decisions. At 43K stars it's well-validated. However, it's a research tool, not a feedback loop — it doesn't improve code quality, testing, or observability. Best used during deliberate tool evaluation sessions (like this one), not daily coding work.

---

## Agent-Reach
**Repo:** [Panniantong/Agent-Reach](https://github.com/Panniantong/Agent-Reach)
**Stars:** 30,604 | **Last updated:** 2026-06-16 | **Forks:** 2,478
**What it does:** CLI toolkit giving AI agents read/search access to Twitter, Reddit, YouTube, GitHub, LinkedIn, Bilibili, XiaoHongShu, and general web — zero API fees, using open-source backends with automatic failover.
**Current workflow alternative:** exa-mcp-server covers web search but is limited to indexed pages and requires an API subscription.
**Key difference:** Targets social media and video platforms exa-mcp-server can't reach. Zero-cost using open-source scrapers with cookie-based auth and multi-backend failover.

**Verdict:** CONDITIONAL at L3+ (useful but ToS risk)
**Justification:** At 30K stars with active maintenance, Agent-Reach fills a gap for social media and video content access. However, cookie-based auth for scraping social platforms carries ToS risk and maintenance overhead. The zero-API-fee model is attractive but relies on scraper stability. Best for teams that need social media intelligence and accept the operational trade-offs.

---

## llm-council
**Repo:** [karpathy/llm-council](https://github.com/karpathy/llm-council)
**Stars:** 20,851 | **Last updated:** 2025-11-22 | **Forks:** 3,895
**What it does:** Local web app that polls multiple LLMs simultaneously, has each model anonymously rank the others' responses, then uses a "Chairman" model to synthesize a consensus answer. Uses OpenRouter for multi-provider access.
**Current workflow alternative:** design-council (CONDITIONAL L4) provides multi-agent debate with role specialization within Claude.
**Key difference:** Cross-provider consensus (GPT-4, Claude, Gemini, etc.) vs. design-council's role-specialized debate within a single provider. The mechanism is inverted: design-council agents argue; llm-council agents evaluate and rank each other.

**Verdict:** SKIP
**Justification:** Last updated November 2025 — 7 months stale with no activity, confirmed abandoned. The cross-provider consensus concept is genuinely distinct from design-council, but the tool is unmaintained and the use case (distrusting a single provider's output) is niche in a Claude-centric workflow. The pattern can be replicated with a simple OpenRouter script without taking on a dead repo.
