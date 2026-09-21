# Evaluation: deep-code-review (Perun)

**Repo:** [remigiusz-antczak/deep-code-review](https://github.com/remigiusz-antczak/deep-code-review)
**Stars:** 1 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-21
**Last triaged:** 2026-09-21  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

"Perun" ships a universal code-review skill, `deep-code-review`, meant to be dropped into any
repository and invoked on any major coding agent (Cursor, Claude Code, Codex, Copilot, Gemini,
Aider). Default mode is review-only; opt-in overlays extend it toward delivery gates, idea
criticism, and product/business specialist roles. It runs systematic audits across ~21 domains
(correctness, security, AI/LLM safety, data integrity, performance, reliability, testing,
infrastructure, docs, accessibility, …) and produces a severity-ranked report.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow clone
of the repo (README, LICENSE, install script, docs) confirming it is real, MIT-licensed, and
matches its stated description. That is sufficient to catalog it and place it relative to existing
review-quality peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P2 challenger: cites `code-review` and `pr-review-toolkit` (both STACK `KEEP`) in Overlaps, but
pressure is 0 (brand new, nothing cites it back yet). Not SKIPped as redundant — its stated design
(an explicit "never fabricates" evidence-grounded bar, multi-domain severity-ranked audits, opt-in
overlays) is differentiated enough from the two general-purpose incumbents to be worth a real
hands-on comparison rather than a mechanical dismissal, per the "don't SKIP a major or
differentiated tool as merely redundant" guardrail. At 1 star and same-day activity it is too early
to prioritize that eval; left at `discovery-log` for a future P0 pass.

_Triaged 2026-09-21 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [deep-code-review (Perun)](https://github.com/remigiusz-antczak/deep-code-review) | skill | Evidence-grounded code-review skill (MIT) — severity-ranked audits across correctness, security, AI/LLM safety, data quality, performance, and reliability | Agent-run review is inconsistent and can fabricate findings; want a reproducible, evidence-grounded audit bar across any language or agent | vet, brooks-lint, code-review, pr-review-toolkit |  |
