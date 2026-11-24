# Evaluation: BriefCheck

**Repo:** [yulongwu-x/BriefCheck](https://github.com/yulongwu-x/BriefCheck)
**Stars:** 15 | **Last updated:** 2026-11-22 (pushed) | **License:** MIT
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A zero-dependency Python CLI, Agent Skill, and GitHub Action that catches hallucinated diff citations in any AI PR review — it checks whether the lines/symbols a review cites actually exist in the diff, rather than reviewing code quality itself.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to assess redundancy against a catalogued incumbent, not the tool's actual behavior.

## Verdict

**discovery-log — tentative read** — a narrow citation-fidelity checker, not a competitor to general-purpose review tools.

## Triage note

Left at `discovery-log`, not SKIPped. It cites `code-review` and `pr-review-toolkit` in Overlaps, both STACK picks, but BriefCheck's job (verifying a diff citation isn't hallucinated) is a narrower, complementary check that neither of those performs — they review code quality/structure, not whether the review's own citations are real. No incumbent does what this does, so a redundancy SKIP isn't available; left for a real eval if it gains traction.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [BriefCheck](https://github.com/yulongwu-x/BriefCheck) | tool | Zero-dependency CLI, Agent Skill, and GitHub Action (MIT) that catches hallucinated diff citations in any AI PR review | An AI PR review can cite diff lines or symbols that don't exist, and nothing checks the citations themselves | code-review, pr-review-toolkit, AgentSeed |
