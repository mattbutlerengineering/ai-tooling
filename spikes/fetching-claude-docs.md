# Spike: Best way to fetch up-to-date Claude documentation & best practices

**Issue:** [#122](https://github.com/mattbutlerengineering/ai-tooling/issues/122) ·
**Date:** 2026-06-24 · **Status:** complete (recommendation below) ·
**Evidence:** MEASURED (light) — each candidate was **run once, hands-on, against
the same probe question** ("How does Anthropic prompt caching work — `cache_control`,
per-model minimum tokens, 5-minute vs 1-hour TTL pricing, max breakpoints?"). This is
a smoke test of *mechanics and output quality*, not a multi-question benchmark.

> Spikes live outside `evaluations/` on purpose — they compare several tools and carry
> no single `## Verdict`, so they aren't parsed by the eval/verdict gates and aren't
> synced to `plugin/docs/`. Promoting a pick here to a catalog ADOPT verdict needs a
> measured eval against `TEMPLATE.md`.

---

## The question

Issue #122 asks for the **best skill / tool / MCP for fetching up-to-date Claude
(Anthropic) documentation *and best practices***. The named candidates: context7 (MCP),
the `claude-api` skill, the `claude-code-guide` agent, and direct WebFetch of the docs
site. I ran all four against one concrete, freshness-sensitive API question and compared.

## TL;DR — strict recommendation

There is **no single winner — the pick is job-dependent** (same shape as #116/#119). But
the question has two halves, and they split cleanly:

| | Tool | Best job | Notes |
|---|---|---|---|
| **1 (primary — "best practices")** | **`claude-api` skill** | Building/maintaining Claude apps with **correct current patterns** — it front-loads the *drift* (adaptive thinking, removed `budget_tokens`/sampling params, current model IDs) that raw docs bury, bundles per-language SDK refs, and routes to live docs | First-party-aligned, version-stamped; **heavy context load** — invoke for LLM-app work, not a one-off lookup |
| **1 (primary — "documentation")** | **WebFetch `platform.claude.com/…​.md`** | Pulling **one authoritative current fact** on demand | Leanest, stateless, most complete single answer. Catch: `docs.anthropic.com` **301-redirects** to `platform.claude.com`; append `.md` to the doc path for clean markdown |
| **2 (SDK code snippets)** | **context7 (MCP)** | "How do I call X in SDK Y" — indexed code examples, ranked by source reputation | Already **KEEP / RUN / in STACK**; two-call flow (`resolve-library-id` → `query-docs`); snippet-oriented, lighter on prose/pricing |
| **3 (NL Q&A convenience)** | **`claude-code-guide` agent** | Natural-language questions about Claude Code / SDK / API when you want a *synthesized answer*, not raw docs | Returns a sourced answer and keeps research out of the main context — at the cost of a subagent (latency + tokens). It WebFetches the same docs under the hood |

**The honest bottom line:** for the *documentation* half, **WebFetch of
`platform.claude.com/<path>.md` is the primitive everything else sits on** (context7
indexes it; claude-code-guide fetches it; the `claude-api` skill links to it). For the
*best-practices* half — the part the issue title actually distinguishes — **the
`claude-api` skill is the only candidate that curates judgment** (do this, not that;
this param was removed), so it's the pick whenever you're writing Claude code. Use the
others as accelerators around those two.

---

## What each candidate did (verified 2026-06-24)

### `claude-api` skill — *curated best-practices + current API*, heavy
- **What it is:** a bundled skill that loads a large in-context reference — current model
  catalog (version-stamped `cached: 2026-06-04`), an **API-drift table** (stale prior →
  current API), prompt-caching/thinking/effort quick-references, per-language SDK docs,
  a migration guide, and `shared/live-sources.md` (a directory of WebFetch URLs for the
  live docs).
- **On the probe:** answered correctly *and* gave the surrounding best-practice framing
  (prefix-match invariant, silent-invalidator checklist, where to place breakpoints) plus
  the current model context (Opus 4.8 minimums) — the only candidate that volunteered the
  *why*, not just the *what*.
- **Strength:** uniquely covers "**best practices**." Surfaces the gotchas raw docs
  bury (adaptive thinking vs removed `budget_tokens`; `temperature`/`top_p`/`top_k`
  removed on Opus 4.7/4.8/Fable 5; model-ID strings) and routes to live docs for freshness.
- **Cost:** large context footprint on load. Right for *doing Claude-app development*,
  wrong for a single fact lookup.

### WebFetch of the docs site — *leanest, most current single fact*
- **On the probe:** the most complete single answer — per-model cacheable minimums, 5m
  (1.25×) vs 1h (2×) write multipliers, 0.1× reads, 4 breakpoints, the 20-block lookback,
  the tools→system→messages invalidation hierarchy, and a worked Opus 4.8 price table.
- **Friction (real, worth recording):** `https://docs.anthropic.com/…` now **301-redirects
  to `https://platform.claude.com/…`** — WebFetch returns the redirect for you to re-issue.
  Appending **`.md`** to a doc path yields clean markdown. So the durable recipe is
  *WebFetch `https://platform.claude.com/docs/en/<path>.md`*.
- **Strength:** zero setup beyond the tool, stateless, always current (it's the source).
- **Weakness:** one URL at a time; you must know/guess the path; no best-practice curation.

### context7 (MCP) — *SDK code-snippet retriever*, KEEP/in-STACK
- **On the probe:** `resolve-library-id "Anthropic Claude API"` →
  `/websites/platform_claude_en_api` (High reputation, 59K snippets), then `query-docs`
  returned accurate **SDK-snippet** results (cache_control examples, `5m`/`1h` TTL enums,
  the `cache_creation`/`cache_read` usage fields) — strong for code, lighter on the
  pricing/prose narrative the WebFetch pull captured in full.
- **Strength:** indexed across libraries and versions, ranked by source reputation; the
  best fit for "show me the code for X in SDK Y." Already catalogued KEEP, RUN, in STACK.
- **Weakness:** two-call flow; snippet-shaped (you assemble the picture); needs the MCP
  server connected.

### `claude-code-guide` agent — *synthesized NL answer*, costs a subagent
- **On the probe:** dispatched as an agent; it WebFetched `platform.claude.com/…/prompt-caching.md`
  and returned a clean, correct, **concise** answer with explicit source attribution and a
  freshness-confidence line.
- **Strength:** best when you want an *answer* to a natural-language question (about Claude
  Code, the SDK, or the API), not raw docs — and it keeps the doc-trawling out of your main
  context.
- **Weakness:** spins a subagent (latency + tokens); it's a convenience layer over WebFetch,
  not a distinct source.

### Also considered (not named in the issue)
- **`ref-tools-mcp`** (catalogued) — a generic docs-search MCP; overlaps context7 but isn't
  Claude-specialized. Use context7 for Claude/library docs.
- **WebSearch** — fine for *finding* the right doc URL when you don't know the path, then
  hand off to WebFetch; not a primary fetch path on its own.

---

## Recommended next steps

- **Adopt the two-primary recipe in practice:** load the `claude-api` skill when writing
  or reviewing Claude/Anthropic SDK code (it already auto-triggers on Claude/Anthropic
  mentions); use `WebFetch https://platform.claude.com/docs/en/<path>.md` for a single
  current fact; reach for context7 for SDK code snippets; use `claude-code-guide` for
  NL Q&A you want answered rather than researched.
- **Record the domain move:** any catalog/eval/doc that still points at `docs.anthropic.com`
  for a *fetchable* path should expect a 301 to `platform.claude.com` — note it where it
  matters (this is a freshness gotcha, not a gate failure; link-rot detector is opt-in).
- **If a measured catalog verdict is wanted** for the `claude-api` skill or
  `claude-code-guide` agent, graduate this smoke test to a `TEMPLATE.md` eval with a
  multi-question battery (freshness, coverage, latency, token cost) — out of scope for a spike.
