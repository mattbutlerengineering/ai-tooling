# Evaluation: shadcn/improve

**Repo:** [shadcn/improve](https://github.com/shadcn/improve)
**Stars:** 5,185 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Review (outer loop — periodic audits)
**Layer:** Tooling

---

## What it does

Two-model codebase audit pipeline. An expensive model (Opus/Sonnet) audits the codebase across nine categories (correctness, security, performance, tech debt, test coverage, etc.) and writes self-contained markdown execution plans into a `plans/` directory. Cheaper models or humans then execute those plans in isolation. Never modifies source code directly; optionally publishes plans as GitHub issues.

## How we tested it

**Evidence:** REVIEW

**Repo/README review — not run hands-on.** Correcting the install first: shadcn/improve is a **Claude Code skill**, installed via the skills.sh installer, not a standalone `npx shadcn-improve` CLI (no such npm package exists):

```
npx skills add shadcn/improve
```

Once installed, you invoke it as a skill inside Claude Code (you pick which model audits and which executes); it writes a codebase analysis, then per-improvement plan files. The mechanism below is from the repo's README ("Use your most capable model to audit your codebase and write plans for cheaper models to execute"), not from an observed run — so no token costs, plan counts, or timings are claimed as measured.

## What it offers (from the README/design review)

- **Two-model economics by design**: the most capable model only reads and plans; cheaper models execute the plans. The intended saving is that you don't pay top-tier rates for mechanical edits. (Plausible, but actual per-run cost was not measured here.)
- **Durable plan artifacts**: improvements are written as individual, human-readable plan files that survive context resets and can be reviewed before execution — a real advantage over a one-shot "fix everything" pass.
- **Issue-tracker integration**: plans can become assignable GitHub issues, fitting a backlog-driven workflow.

## Open questions (would need a hands-on run)

- Signal-to-noise: how many findings are objective improvements vs subjective style preferences — and whether it flags intentional, domain-specific patterns as problems.
- Actual cost of a full audit at the dual-model split, and how it scales with codebase size.
- Whether the executor model reliably follows plan instructions on complex refactors.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | An audit aid, not a correctness gate; finding quality unverified here. |
| Speed | neutral | Periodic (not per-PR), so no effect on daily loop speed. |
| Maintainability | + (by design) | Plan-file artifacts + dead-code/consistency focus target maintainability. |
| Safety | neutral | A security category exists but is shallow next to dedicated tools like trailofbits/skills. |
| Cost Efficiency | + (claimed) | Dual-model split is designed to cut audit cost — not measured in this review. |

## Verdict

**CONDITIONAL** (review-based)

On its design, shadcn/improve fits periodic codebase-health audits (monthly/quarterly) rather than per-PR use — that's the code-review plugin's job — and the plan-file + dual-model approach is a sensible way to make a proactive audit cheaper and reviewable. Held at CONDITIONAL because this is a README review, not a run: the signal-to-noise ratio and real cost are the open questions, and the install is `npx skills add shadcn/improve` (a skill), not a `npx shadcn-improve` CLI. Complementary with code-review (reactive, per-PR), not redundant.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shadcn/improve](https://github.com/shadcn/improve) | tool | Two-model codebase audit: expensive model plans, cheap model executes | Proactive codebase improvement at lower cost than single-model audit | code-review plugin, improve-codebase-architecture skill |
