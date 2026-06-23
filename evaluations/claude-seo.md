# Evaluation: claude-seo

**Repo:** [AgriciDaniel/claude-seo](https://github.com/AgriciDaniel/claude-seo)
**Stars:** 9,262 | **Last updated:** 2026-06-13 (pushed; created 2026-02-07) | **License:** MIT
**Dev loop stage:** Verify / Review — a domain audit layer that scores a shipped site against primary-source SEO/GEO guidance and produces a prioritized action plan; runs outside the code-change loop on a deployed surface
**Layer:** Process / Tooling (a Claude Code plugin: 25 sub-skills + 18 sub-agents orchestrated in parallel; optional MCP/API extensions add infrastructure)

---

## What it does

The catalog one-liner: "25 SEO sub-skills + 18 sub-agents covering technical SEO, E-E-A-T, schema, GEO/AEO, and reporting." It is a Claude Code plugin (v2.2.0 per `plugin.json`) that turns an agent into a parallel SEO audit team: a top-level orchestrator (`seo-flow`) fans work out to specialist sub-agents — `seo-technical`, `seo-content`, `seo-schema`, `seo-sitemap`, `seo-geo` (AI-search / answer-engine optimization), `seo-local`, `seo-maps`, `seo-ecommerce`, `seo-backlinks`, `seo-cluster`, `seo-drift`, `seo-performance`, `seo-google`, `seo-sxo`, plus image/visual agents — and produces a single prioritized report.

The mechanism is prompt-and-reference driven, not a closed-source SaaS. Each skill is a `SKILL.md` plus `references/` (e.g. `seo-cluster/references/hub-spoke-architecture.md`) that encode SEO methodology grounded in Google's published guidance (the README cites Google's AI Optimization Guide, web.dev, IPTC metadata standards). The README's headline claim is "falsifiable, not promotional": every recommendation is supposed to carry the first-principle observation it rests on, a dependency relationship, an explicit "how would we know this failed?" check, and a leading indicator — i.e. SEO advice framed as testable hypotheses rather than checklist dogma. Optional extensions (DataForSEO, Firecrawl, Ahrefs, SE Ranking, Bing Webmaster, Unlighthouse, Banana image-gen) wire in third-party data via MCP/API and require their own keys; the core works offline against the page/site you point it at. The repo ships hardened fetchers (the `plugin.json` notes "SSRF/DNS-rebinding safe fetchers"), CI, 20 releases, and dual-distribution: a public MIT repo and a private "AI Marketing Hub Pro" Skool-community mirror with early access.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** The plugin was not installed, no site was audited, and no report was generated, so every claim below is from the repository (GitHub metadata, README, `plugin.json`, full file tree, agent/skill inventory), not from observed audit output. The "326 tests passing" badge, the three-month Google Search Console growth screenshot, and the "site-level audits in minutes" claim are the author's self-reported figures from the README — not measured here. **Identity note:** the task brief flagged that the CATALOG link "may be wrong" (pointing at `addyosmani/web-quality-skills`). That is not what the catalog shows — line 180 already links `AgriciDaniel/claude-seo`, and `gh search repos claude-seo` confirms this is the canonical, by-far-largest "claude-seo" repo (9.3K stars vs. single-digit-K alternatives). The addyosmani link belongs to a *different* entry (`web-quality-skills`, line 162). The catalog is correct; I evaluated `AgriciDaniel/claude-seo`.

```bash
gh search repos claude-seo --limit 5                                          # AgriciDaniel/claude-seo is canonical (9.3K stars)
gh api repos/AgriciDaniel/claude-seo --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,license:.license.spdx_id}'
gh api repos/AgriciDaniel/claude-seo/readme --jq '.content' | base64 -d
gh api "repos/AgriciDaniel/claude-seo/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/AgriciDaniel/claude-seo/commits --jq 'length'      # 30 (capped page)
gh api repos/AgriciDaniel/claude-seo/releases --jq 'length'     # 20
gh api repos/AgriciDaniel/claude-seo/contributors --jq '[.[].login]'  # 12, incl. "claude"
```

## What worked

- **Genuinely deep domain coverage.** 18 specialist agents + 25 sub-skills span the modern SEO surface: classic technical SEO and schema, but also GEO/AEO (optimizing for AI answer engines), local/maps intelligence, semantic clustering, international hreflang, and e-commerce. This is far past a "check your meta tags" checklist.
- **Falsifiability discipline is the right instinct.** Framing every recommendation with an explicit failure check and a leading indicator is exactly how to keep an LLM from emitting confident, unverifiable SEO folklore. It maps cleanly onto the catalog's Correctness signal.
- **Primary-source grounding.** The skills cite Google's own AI Optimization Guide and web.dev rather than recycled blog wisdom, and ship a `data/google-updates.json` — reducing the "trained on 2021 SEO advice" failure mode.
- **Parallel fan-out fits the audit shape.** SEO audit is embarrassingly parallel (technical, content, schema, links are independent passes), so the orchestrator → sub-agent design is a natural fit and plausibly fast.
- **Strong maturity signals for a skill pack.** 9.3K stars / 1.3K forks, MIT, 20 releases, CI workflows, `SECURITY.md` / `PRIVACY.md` / `CITATION.cff`, 12 contributors, and SSRF-hardened fetchers. This is maintained software, not a weekend gist.
- **Core works without paid data.** The base audit runs against the site you point it at; third-party data providers (DataForSEO, Ahrefs, etc.) are opt-in extensions, so there's no mandatory subscription to get value.

## What didn't work or surprised us

- **Out of the catalog's core lane.** This is a *marketing/growth* tool, not a code-quality tool. It moves search ranking, not the correctness or maintainability of an engineering codebase. It belongs in the catalog as a domain-specific skill, but it competes for an SEO budget, not a dev-tooling budget.
- **Results claims are unverifiable.** The "three-month GSC growth" chart is one anonymous site run by the author; "326 tests passing" tests the skill's plumbing, not SEO efficacy. SEO outcomes depend on the site, competition, and Google's ranking changes — none of which the skill controls. Treat the growth screenshot as anecdote.
- **Commercial-funnel framing.** The README is heavily oriented toward an "AI Marketing Hub Pro" paid Skool community with a private early-access mirror. The public MIT version is real and complete, but the marketing gravity is unusually strong for an open-source dev tool, and "private mirror requires membership" means the bleeding edge is paywalled.
- **Extensions reintroduce cost and key-management.** The most powerful data (backlinks, keyword volume, rank tracking) lives behind DataForSEO/Ahrefs/SE Ranking extensions — paid APIs with their own keys and SSRF surface. The headline "25 skills" oversells what runs for free.
- **Heavy surface area.** 18 agents + 25 skills + 8 extensions is a large install for a single domain. For a team that occasionally needs SEO, the lighter `web-quality-skills` SEO pass may be enough.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Primary-source grounding (Google AI Optimization Guide, web.dev) plus a per-recommendation falsifiability check ("how would we know this failed?") directly targets hallucinated SEO advice — *for the SEO domain*, not for code. |
| Speed | + | Parallel orchestrator → 18 sub-agents turns a multi-day manual audit into a single run; the README claims "minutes not hours" (self-reported, plausible given the parallel design). |
| Maintainability | neutral | It audits a deployed site, not your codebase; it doesn't change how maintainable your engineering code is. The plugin itself is well-maintained (20 releases, CI). |
| Safety | neutral / + | Ships SSRF/DNS-rebinding-hardened fetchers and a `SECURITY.md`. Offset: optional extensions add third-party API keys and outbound calls; the `curl \| bash` install path is mitigated by a documented `git clone` + review-first alternative. |
| Cost Efficiency | neutral / − | Core audit costs only agent tokens, but a full 18-agent parallel fan-out is token-heavy, and the high-value data extensions are paid subscriptions. |

## Verdict

**CONDITIONAL** — adopt when SEO/GEO is an actual deliverable for you or your clients (agencies running multiple sites, in-house SEO leads, freelance consultants doing audits). For a general engineering team that ships a product and occasionally wants a sanity check on meta tags and schema, this is overkill — reach for the lighter SEO pass in `web-quality-skills` instead. It is a domain tool that earns its place in the catalog's skills section, but it is not a dev-loop default.

Compared to neighbors: the catalog marks claude-seo's overlap as "— (domain-specific: SEO)" and that's accurate — nothing else in the catalog covers SEO at this depth. The closest neighbor is **web-quality-skills (addyosmani)**, whose SEO is one slice of a broader accessibility/performance/Core-Web-Vitals audit suite; web-quality-skills is the better pick when SEO is a *secondary* concern bundled with general web quality, while claude-seo wins decisively when SEO/GEO is the primary job and you need backlinks, clustering, local, and AI-search depth. **security-best-practices** overlaps only on the narrow "security headers" sliver. claude-seo's real competition is commercial SEO platforms (Ahrefs, Semrush, Screaming Frog), against which its differentiator is the agentic, falsifiability-checked, in-your-terminal workflow — and, candidly, its weakness is that the strongest data still flows through those same paid APIs as extensions.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-seo](https://github.com/AgriciDaniel/claude-seo) | skill | 25 SEO sub-skills + 18 sub-agents (technical SEO, E-E-A-T, schema, GEO/AEO, local, backlinks, reporting); parallel orchestrator, falsifiability-checked recommendations, optional paid-data extensions | Need a deep, AI-search-aware SEO/GEO audit of a deployed site with a prioritized, verifiable action plan instead of generic checklist advice | web-quality-skills (SEO slice overlap), security-best-practices (security-headers sliver) |
