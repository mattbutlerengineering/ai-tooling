# Evaluation: passmark

**Repo:** [bug0inc/passmark](https://github.com/bug0inc/passmark)
**Stars:** 1,023 | **Last updated:** 2026-06-16 | **License:** FSL-1.1-Apache-2.0 (Functional Source License; GitHub reports NOASSERTION)
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

AI browser regression testing library that wraps Playwright. You write test steps in natural language (`"Click Acme Circles T-Shirt"`, `"Add to cart"`) instead of CSS/ARIA selectors; an AI model (Gemini for step execution by default) resolves each step against an ARIA accessibility snapshot of the page and drives Playwright to perform the action. Assertions go through a multi-model consensus engine — Claude and Gemini evaluate the same claim in parallel, and a third arbiter model (Gemini 3.1 Pro) breaks ties when they disagree.

The two headline reliability mechanisms are:

- **Intelligent caching** — successful single-step actions are cached in Redis keyed by `userFlow` + `step.description`. Subsequent runs replay the cached Playwright action directly with no AI call, cutting latency and token cost.
- **Auto-healing** — when a cached action fails (e.g., the UI changed and the cached selector no longer resolves), Passmark falls back to a fresh AI execution against the current snapshot and re-caches the result. The natural-language step is the durable contract; the underlying selector is regenerated on demand, so tests "stay stable without needing to update AI prompts."

Additional surface: video assertions (records the run, evaluates via Gemini Files API — for transient toasts), `runUserFlow()` for exploratory single-agent flows, opt-in OpenAI CUA (computer-use) screenshot mode, dynamic placeholders (`{{run.*}}`, `{{email.*}}`), pluggable email extraction, an AST-validated "secure script runner" with an allowlisted Playwright API, and Axiom/OpenTelemetry telemetry.

## How we tested it

Did not install or run. This evaluation is based on inspection of the GitHub repository metadata (`gh api repos/bug0inc/passmark`), the full README, the repository file tree, and the license. No hands-on execution was performed — running it requires Anthropic + Google API keys (and Redis for the caching/healing path), and the verdict does not depend on metrics that would require a live run.

```
gh api repos/bug0inc/passmark --jq '{stars,license,description,pushed_at,created_at}'
# stars 1023 | license NOASSERTION | created 2026-03-29 | pushed 2026-06-16
gh api repos/bug0inc/passmark/readme --jq '.content' | base64 -d   # full README
gh api repos/bug0inc/passmark/contents --jq '.[].name'             # file tree
```

Key facts established from inspection: created 2026-03-29 (~3 months old at eval time), actively pushed, TypeScript, published to npm as `passmark`, backed by a commercial company (bug0.com). The README's own "Known Limitations" states: *"Tests are not comprehensive at the moment."* License is FSL-1.1-Apache-2.0 — a source-available, non-compete Functional Source License that converts to Apache-2.0 two years after each release; GitHub cannot classify it, hence the NOASSERTION marker.

## What worked

(From documentation/design inspection — not hands-on confirmation.)

- The natural-language-step-as-durable-contract design directly targets the stated pain: tests survive selector churn because selectors are regenerated, not hand-maintained. This is a genuinely different value proposition from raw Playwright.
- Multi-model consensus assertions with an explicit `fail-on-disagreement` policy is a thoughtful flakiness control — disagreement between Claude and Gemini surfaces ambiguity in the UI rather than letting one model swing the verdict.
- Redis caching with auto-heal-on-miss is a sensible cost/latency strategy: steady-state runs are cheap (cached replay), and only changed UI incurs AI cost.
- Strong Claude Code fit on paper: it is itself a harness for AI-driven verification, multi-provider (Anthropic/Google/OpenAI, plus Vercel/OpenRouter/Cloudflare gateways), and produces a Playwright HTML report with an AI summary that an agent can consume.
- Cache is auto-bypassed on Playwright retries, which avoids replaying a stale cached action during a retry loop.

## What didn't work or surprised us

(Concerns identified from inspection; not failures observed in a run.)

- **Auto-healing is a double-edged sword.** The same mechanism that keeps tests green through legitimate UI refactors can also mask real regressions: if a button moves or a label changes *because of a bug*, the AI may "heal" the step to the new wrong target and the test still passes. Consensus assertions mitigate this for the final claim but not for intermediate steps.
- **Non-determinism in the Verify stage.** Steps are resolved by an LLM against a live snapshot. Compared to deterministic Playwright selectors, results can vary run-to-run, and assertion verdicts depend on model output. This is the inverse of what a regression gate usually wants.
- **License is restrictive (FSL-1.1).** Source-available with a non-compete clause — you cannot use it to build a competing product, and it is not OSI-approved until the 2-year Apache-2.0 conversion. This matters for commercial adoption and is a meaningfully different posture than the Apache-2.0 of agent-browser and stryker-js.
- **Maturity is low.** ~3 months old, the maintainers themselves flag non-comprehensive tests, and the consensus/arbiter design multiplies per-step API spend (each assertion is at least 2 model calls, 3 on disagreement). Real cost depends on cache hit rate.
- **Heavy setup.** Requires at minimum two provider keys (Anthropic + Google) for consensus, and Redis for caching/healing/global state — without Redis the headline caching and auto-heal features are degraded.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / risk | Resilient regression coverage on shifting UIs and multi-model assertions raise correctness, but auto-heal can mask the very regressions it should catch |
| Speed | + | Redis cache replays steps with no AI call after first run; AI only on cache miss / UI change |
| Maintainability | + | Natural-language steps survive selector churn — no brittle selector maintenance |
| Safety | - | FSL-1.1 non-compete license (NOASSERTION); AST-allowlisted script runner is a plus but license constrains use |
| Cost Efficiency | - / mixed | Multi-model consensus = 2-3 model calls per assertion; mitigated by caching but cost scales with miss rate |

## Verdict

**CONDITIONAL**

Adopt only for projects with rapidly-changing UIs where selector maintenance is a real, recurring cost and where the FSL-1.1 non-compete license is acceptable (i.e., you are not building a competing test/QA product). The auto-healing + consensus design is genuinely novel for the Verify stage, but it trades determinism for resilience — the same healing that absorbs legitimate refactors can absorb bugs, so it complements rather than replaces deterministic Playwright assertions on critical paths. Given its ~3-month age, self-acknowledged thin test coverage, restrictive license, and Redis + dual-provider-key setup cost, it is not a default-install tool.

Comparison: vs **playwright** (deterministic, free, Apache-2.0) — Passmark adds resilience to UI churn at the cost of determinism and AI spend; use Playwright for stable critical-path gates and Passmark for high-churn flows. vs **agent-browser** (ADOPT, Apache-2.0) — agent-browser is for live exploratory verification during development with zero per-test maintenance; Passmark is for persistent, cached, repeatable regression *suites*. They occupy different slots: agent-browser for ad-hoc dogfooding, Passmark for a standing AI regression suite. vs **stryker-js** (CONDITIONAL) — both are CONDITIONAL Verify tools whose value is gated by cost/runtime; stryker audits test *quality*, Passmark provides resilient browser tests — non-overlapping in practice despite the catalog overlap marker.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [passmark](https://github.com/bug0inc/passmark) | tool | AI browser regression testing on Playwright — intelligent caching + auto-healing selectors (1K stars) | Brittle browser tests break on UI changes; need self-healing AI-driven regression checks | stryker-js, playwright, agent-browser |
