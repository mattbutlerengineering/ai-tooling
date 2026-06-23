# Evaluation: guard-skills

**Repo:** [amElnagdy/guard-skills](https://github.com/amElnagdy/guard-skills)
**Stars:** 827 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Five focused guard skills — `clean-code-guard`, `test-guard`, `docs-guard`, `wp-guard`, `woo-guard` — designed as second-pass quality gates that catch systematic AI-generated code failure modes before code ships. Each is a standalone SKILL.md with progressive-disclosure reference files. The core differentiator is an AI-specific layer: 14 cataloged failure modes backed by published research (GitClear 2025 on duplication growth, USENIX Security '25 on package hallucination, Karpathy on error swallowing, Fowler on agents declaring success despite failing tests).

The skills work reactively — invoke after the agent produces work, before commit/merge — or proactively in live mode. Three modes: guard-pass (diff review), live (constrain while writing), and review (structured findings report). The general-purpose guards (`clean-code-guard`, `test-guard`, `docs-guard`) are language-agnostic; `wp-guard` and `woo-guard` are WordPress/WooCommerce-specific.

## How we tested it

**Evidence:** REVIEW

Read all five SKILL.md files and their reference directories via the GitHub API. Assessed depth, source quality, actionability, and overlap with existing catalog tools. Could not install via `npx skills add` (permission denied in sandbox), so evaluation is architecture-review-based.

```
gh api repos/amElnagdy/guard-skills/contents/skills/clean-code-guard/SKILL.md --jq '.content' | base64 -d
gh api repos/amElnagdy/guard-skills/contents/skills/test-guard/SKILL.md --jq '.content' | base64 -d
gh api repos/amElnagdy/guard-skills/contents/skills/docs-guard/SKILL.md --jq '.content' | base64 -d
gh api repos/amElnagdy/guard-skills/contents/skills/clean-code-guard/references/ai-failure-modes.md --jq '.content' | base64 -d
```

## What worked

- **AI failure modes reference is the standout feature.** 14 cataloged failure modes with research citations, bad/good examples, and imperative rules. Covers catch-all error swallowing, defensive guards for impossible cases, hallucinated APIs, mock fixtures in production code, copy-from-similar bugs, and premature abstraction. This is the highest-value file — it directly addresses patterns other review tools miss.
- **23 always-applied imperatives with clear thresholds.** Not vague — specific limits like ≤20 lines per function, ≤4 parameters, cyclomatic complexity ≤10, nesting depth ≤5. Each imperative cites its primary source (Clean Code, Fowler, Metz, McCabe, Karpathy, arXiv papers).
- **Self-check before delivery checklist.** 8-item verification the agent runs against its own diff before showing the user. Enforces the rules mechanically rather than relying on judgment.
- **Test-guard's Nine Rules are excellent.** "Every mock must be justified" (only at system boundaries), "every test must justify its existence" (what bug does this catch?), "production regression tests are sacred" — practical, opinionated rules that directly combat AI test bloat.
- **Docs-guard treats documentation as verifiable claims.** Every referenced symbol, code sample, and performance claim gets checked against the source. This prevents the most common AI documentation failure: authoritative-sounding text about APIs that don't exist.
- **Progressive disclosure architecture.** SKILL.md loads the imperatives; reference files load only when a specific principle is invoked or the user pushes back. Efficient use of context window.

## What didn't work or surprised us

- **wp-guard and woo-guard are WordPress-specific.** Only 2 of 5 guards are general-purpose for all codebases. The WordPress guards are thorough but narrow the audience significantly.
- **No hands-on testing possible.** Could not install and invoke against a real codebase to validate guard-pass mode produces useful findings in practice. Architecture review only.
- **Some overlap with existing rules.** Many imperatives (small functions, meaningful names, SOLID) are standard Clean Code advice that CLAUDE.md files and code-review plugins already enforce. The AI-specific layer (imperatives 15-22) is where the unique value lives.
- **No automated integration.** Guards must be manually invoked after work. No hook-based automatic triggering — you have to remember to run `$clean-code-guard` on your diff.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | AI failure modes 15-18 directly prevent error swallowing, hallucinated APIs, and mock fixtures in production code |
| Speed | neutral | Second-pass review adds time, but catching issues before commit is faster than catching them in PR review |
| Maintainability | + | Imperatives 1-14 enforce Clean Code/SOLID/DRY with specific thresholds; test-guard prevents test bloat |
| Safety | + | Docs-guard prevents shipping documentation with hallucinated API references |
| Cost Efficiency | neutral | Context-efficient via progressive disclosure, but adds a review pass to each coding session |

## Verdict

**CONDITIONAL**

Use `clean-code-guard`, `test-guard`, and `docs-guard` on projects where AI-generated code quality is a concern and existing review tooling doesn't catch AI-specific failure modes. The AI failure modes reference (imperatives 15-22) is the unique value — the standard Clean Code rules overlap with what code-review plugin and pr-review-toolkit already do. Skip `wp-guard` and `woo-guard` unless working on WordPress/WooCommerce projects. Best paired with code-review plugin (catches correctness bugs) while guard-skills focuses on the AI-specific quality layer.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [guard-skills](https://github.com/amElnagdy/guard-skills) | skill | Quality gates that catch AI-generated failure modes in code, tests, and docs | AI-generated code has distinct failure patterns not caught by traditional linters | code-review, pr-review-toolkit, trailofbits/skills |
