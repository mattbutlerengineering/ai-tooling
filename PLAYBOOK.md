# The Playbook — how to use AI for development, in one page

The front door to this repo. If you build software with AI agents and want a setup that produces high-quality code and keeps improving, start here. Everything else is depth behind three questions: **what do I install, how do I work, and what do I watch?** This page answers them in order and links the detail — every claim below is a link, not a restatement, so the numbers and tiers live in the derived pages that stay honest on their own.

## 1. What to install

→ **[STACK.md](STACK.md)** — the curated stack worth installing on every project, tiered by evidence (Tier 1 measured, Tier 2 review-based). The five highest-impact picks from its Quick Start:

- **[context7](evaluations/context7.md)** — live docs lookup, so an agent never reasons from stale API info.
- **[caveman](evaluations/caveman.md)** — output-token compression (~60–75% fewer tokens) for cost discipline.
- **[trailofbits/skills](evaluations/trailofbits-skills.md)** — a structured security-audit methodology, not ad-hoc review.
- **[playwright](evaluations/playwright-mcp.md)** — visual, end-to-end verification for UI changes.
- **[claude-code-action](evaluations/claude-code-action.md)** — CI integration for async, on-every-PR review.

Why a pick is (or isn't) in the stack: **[STACK-LEDGER.md](STACK-LEDGER.md)**.

## 2. How to work

The loop is **Plan → Implement → Verify → Review → Ship**, with **Reflect** feeding back — two loops, three layers, five signals. The full stage map is **[WORKFLOW.md](WORKFLOW.md)**.

The runnable end-to-end recipe — a plain-language idea to a merged PR, assembled from skills we already have — is **[methodologies/intent-to-production-recipe.md](methodologies/intent-to-production-recipe.md)**:

```
intent ─▶ /to-prd ─▶ PRD
       ─▶ brainstorming + writing-plans ─▶ plan/spec
       ─▶ /to-issues (+ beads) ─▶ tracer-bullet issues
       ─▶ /implement-issue ─▶ merged PR  ─┐
       ─▶ /triage ◀── feedback/bugs ──────┘   (closes the loop)
       … graphify + claude-mem + CONTEXT.md keep it all linked (cross-cutting)
```

A worked example of assessing your own setup against the loop, with named gaps: **[spikes/my-dev-workflow-assessment.md](spikes/my-dev-workflow-assessment.md)**.

To bootstrap any repo with these conventions, run `/setup-workflow`.

## 3. What to watch

- **[NEXT-EVALS.md](NEXT-EVALS.md)** — the ranked *evaluate-next* queue: which not-yet-evaluated tools to run first, derived from overlap pressure and per-stage gaps.
- **[WATCHLIST.md](WATCHLIST.md)** — the *revisit* page: deferred verdicts and their triggers, stale evals, candidates flagged for a hands-on eval, and unverified claims — all derived.
- **[LEARNING.md](LEARNING.md)** — passive learning: channels, talks, and references worth following.
- **Scan intake** — newly-found tools arrive as [GitHub issues labeled `scan`](https://github.com/mattbutlerengineering/ai-tooling/issues?q=is%3Aissue+label%3Ascan), triaged into the catalog.

## How this stays honest

- **Counts and stacks are derived, never hand-written.** `reconcile-counts.py` propagates the one catalog total; NEXT-EVALS.md, WATCHLIST.md, and STACK's evidence tiers are regenerated from data — nobody edits them by hand.
- **Every verdict declares how hard we looked.** An Evidence taxonomy (MEASURED / RUN / REVIEW / SOURCE-ONLY) separates *what we concluded* from *how we know*, and honesty gates flag a strong verdict resting on a README skim.
- **CI enforces all of it.** `make check` runs the full detector set on every push and pull request — see the Integrity audit section of [CLAUDE.md](CLAUDE.md).
