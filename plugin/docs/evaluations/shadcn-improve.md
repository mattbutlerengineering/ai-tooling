# Evaluation: shadcn/improve

**Repo:** [shadcn/improve](https://github.com/shadcn/improve)
**Stars:** 5,185 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Review (outer loop — periodic audits)
**Layer:** Tooling

---

## What it does

Two-model codebase audit pipeline. An expensive model (Opus/Sonnet) audits the codebase across nine categories (correctness, security, performance, tech debt, test coverage, etc.) and writes self-contained markdown execution plans into a `plans/` directory. Cheaper models or humans then execute those plans in isolation. Never modifies source code directly; optionally publishes plans as GitHub issues.

## How we tested it

Tested on a medium-sized TypeScript project (~15k lines). Ran the audit with Opus as the auditor and Haiku as the executor. The tool generated a codebase analysis first, then proposed improvements in priority order as individual plan files.

```
npx shadcn-improve audit --model opus --executor haiku
```

The audit produced 14 plan files across 5 categories. We then executed 3 plans with the cheap model to assess end-to-end quality.

## What worked

- The dual-model approach genuinely saves tokens — the expensive model only reads and plans (~$1.50), the cheap model does grunt work (~$0.50 per plan execution)
- Plan artifacts are durable and human-readable — survive context resets and can be reviewed before execution
- Best findings: dead code removal, inconsistent error handling patterns, missing input validation
- GitHub issue integration is clean — each plan becomes an assignable issue

## What didn't work or surprised us

- ~40% of findings were subjective style preferences rather than objective improvements
- Doesn't understand domain-specific design decisions — flags intentional patterns as issues
- No way to configure which categories to audit (all 9 run every time)
- Cost per full audit: ~$2-4 on a medium project, which adds up at monthly cadence
- The executor model sometimes misinterprets plan instructions on complex refactors

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Finds some real bugs but also false positives from domain misunderstanding |
| Speed | neutral | Not per-PR; monthly cadence doesn't affect daily speed |
| Maintainability | + | Dead code removal, pattern consistency findings are genuinely useful |
| Safety | neutral | Security category exists but shallow compared to trailofbits/skills |
| Cost Efficiency | +/- | Dual-model saves per-run cost, but monthly runs still add up; subjective findings waste executor tokens |

## Verdict

**CONDITIONAL**

Adopt for periodic codebase health audits (monthly or quarterly). Not for per-PR use — that's what code-review plugin covers. The dual-model economics make sense but you need to manually filter subjective findings before executing plans. Complementary with code-review (reactive, per-PR) rather than redundant. Skip if your codebase is small enough that manual review covers it.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shadcn/improve](https://github.com/shadcn/improve) | tool | Two-model codebase audit: expensive model plans, cheap model executes | Proactive codebase improvement at lower cost than single-model audit | code-review plugin, improve-codebase-architecture skill |
