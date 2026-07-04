# Evaluation: ACMM (AI Codebase Maturity Model)

**Repo:** [arXiv:2604.09388](https://arxiv.org/abs/2604.09388) (paper, not a repo)
**Stars:** N/A (academic paper) | **Last updated:** v2 — Apr 27, 2026 | **License:** arXiv (author: Andy Anderson)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Reflect / Retrospect (used to assess and direct workflow maturity)
**Layer:** Process (a conceptual model, not tooling or infrastructure)

---

## What it does

6-level AI Codebase Maturity Model defined by feedback loop tightness.

ACMM is a conceptual framework, not software. Per the arXiv abstract, it observes that "AI coding tools are widely adopted, but most teams plateau at prompt-and-review without a framework for systematic progression," and presents "a 6-level framework describing how codebases evolve from basic AI-assisted coding to fully autonomous systems." Each level is defined by its *feedback loop topology* — the specific feedback mechanism (instructions, tests, metrics) a codebase must have in place before it can advance to the next level. The paper's central claim is that the intelligence of an AI-driven development system depends on the surrounding infrastructure rather than the AI model itself, and that each level unlocks the next by adding one more feedback mechanism — with testing called out as the single most critical investment across the whole progression.

## How we tested it

**Evidence:** REVIEW

This is a reference/conceptual framework (an arXiv paper), not an installable tool, so there is no command to run. "Testing" here means reading the source and comparing its thesis against this repo's own maturity framing in WORKFLOW.md.

- Fetched the arXiv abstract page (`https://arxiv.org/abs/2604.09388`) and confirmed: author Andy Anderson, v1 Apr 10 2026 / v2 Apr 27 2026, 6 levels, defining dimension = feedback-loop topology, testing identified as the most critical investment.
- Read this repo's WORKFLOW.md and compared ACMM's thesis to the four Design Principles and the inner/outer loop model.

```
WebFetch https://arxiv.org/abs/2604.09388
Read /Users/mbutler/github/ai-tooling/WORKFLOW.md
```

## What worked

- The paper's thesis is the same one WORKFLOW.md is built on. Design Principle #1 ("Fewer tools, more feedback loops") and #4 ("Process + Tooling + Infrastructure ... connected by feedback arcs, is how quality compounds") restate ACMM's "feedback loop topology defines maturity" claim almost directly.
- ACMM's "testing is the single most critical investment" maps cleanly onto WORKFLOW.md's Implement/Verify stages (TDD enforcement, coverage gating, mutation testing) — useful external corroboration for the repo's emphasis.
- As a *named, citable axis* it gives the repo's maturity discussion an external reference point. WORKFLOW.md currently uses its own inner/outer loop vocabulary; ACMM supplies a complementary "what level is this codebase at?" lens that the per-stage feedback arcs could be scored against.

## What didn't work or surprised us

- No software, no install, nothing to adopt. It changes how you *think*, not what you run — its value is purely as a reference.
- The abstract does not enumerate the six level names or their per-level criteria; those are in the paper body, not verifiable from the abstract alone. Any specific level mapping in this repo would need the full text to avoid fabrication.
- Single-author arXiv preprint with no repo, no stars, no community signal — quality/uptake is unverified beyond the paper itself.
- Partial overlap with this repo's own framing means ACMM is more a *validation/alternative vocabulary* than a new capability. CLAUDE.md explicitly tells this repo to use inner/outer loop vocabulary "not ACMM levels," so ACMM should stay a reference, not become the repo's primary model.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | A maturity model doesn't touch code; testing emphasis is already covered by Verify-stage tooling. |
| Speed | neutral | Conceptual reference, no effect on prompt-to-merge time. |
| Maintainability | + | Gives teams a named axis to assess whether their feedback infrastructure is actually maturing over time. |
| Safety | neutral | Higher levels imply more autonomy gating, but the paper provides no enforcement mechanism. |
| Cost Efficiency | neutral | No token or cost implications. |

## Verdict

**CONDITIONAL** (as a reference, not a tool — KEEP in catalog)

ACMM is a conceptual framework that independently arrives at this repo's own core thesis: maturity in AI-assisted development is defined by feedback-loop topology, and testing is the highest-leverage investment. Keep it in the Maturity Frameworks category as a citable external reference for the maturity discussion in WORKFLOW.md. Do not treat it as an installable tool (there is nothing to install) and do not adopt its level vocabulary as the repo's primary model — CLAUDE.md already standardizes on inner/outer loop terms. Useful as corroboration and as an optional scoring axis; not a workflow change.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ACMM](https://arxiv.org/abs/2604.09388) | reference | 6-level AI Codebase Maturity Model defined by feedback loop tightness | Teams plateau at prompt-and-review with no framework for systematic progression toward autonomy | WORKFLOW.md (this repo's inner/outer loop + feedback-arc maturity framing) |
