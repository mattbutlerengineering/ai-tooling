# Evaluation: turbo

**Repo:** [tobihagemann/turbo](https://github.com/tobihagemann/turbo)
**Stars:** 411 | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-14
**Last triaged:** 2026-10-14  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Markdown skills (separate Claude Code and Codex editions) for a Plan → Implement →
Finalize pipeline: `/turboplan` assesses scope and settles the approach,
implementation uses the project's own tests/tooling, and `/finalize` checks,
reviews, and polishes before shipping. `/finalize` uses the *other* tool (Codex for
the Claude Code edition and vice versa) for peer review. Standalone skills include
`/investigate`, `/review-pr`, and `/self-improve`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata, the README's documented workflow, and the CATALOG "Overlaps with"
cell.

## Verdict

**discovery-log — tentative read**

## Triage note

Triage bands this P2 challenger against `GSD (Get Shit Done)` and `feature-dev`,
both STACK picks for the same plan→implement→verify shape — a real overlap, not a
dangling citation. Not SKIPped as redundant because turbo's distinguishing claim is
structural rather than cosmetic: `/finalize` hands review to a *second coding
agent* (Codex reviewing Claude Code's work, or vice versa), which is a different
mechanism from GSD's subagent-gated loop or feature-dev's single-tool
planning/implementation/verification stages. Whether that cross-tool review
delivers a real correctness/safety edge over a same-tool review gate is exactly
the kind of question a bulk pass cannot answer — significant (★411) and
differentiated enough to deserve a real hands-on eval rather than a mechanical
SKIP.

_Triaged 2026-10-14 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [turbo](https://github.com/tobihagemann/turbo) | skill | Markdown skills (MIT) for a plan → implement → finalize pipeline across Claude Code and Codex, each tool reviewing the other's work | A single agent's plan, implementation, and review share the same blind spots; want cross-tool peer review built into the pipeline | GSD (Get Shit Done), feature-dev, sol-skill |
