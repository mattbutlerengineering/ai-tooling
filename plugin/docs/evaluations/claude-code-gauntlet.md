# Evaluation: claude-code-gauntlet

**Repo:** [liatrio-labs/claude-code-gauntlet](https://github.com/liatrio-labs/claude-code-gauntlet)
**Stars:** 12 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Adversarial multi-agent PR review for Claude Code and GitHub/GitLab — 7 concern-specialized
discovery agents (bug, security, cross-file-impact, test, conventions, type-design, simplifier)
run in parallel, followed by deterministic merge/verify phases and a blind challenge. Ships a
benchmark harness that scores the pipeline's recall/noise against a curated set of golden PRs
(reports 0.695 recall / 0.180 noise on its own Martian benchmark).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`. The
recall/noise figures are the project's own self-reported benchmark results, not independently
measured here. Source-grounded only: the repo's own README description plus the CATALOG
"Overlaps with" cell. Sufficient to place the lead, not to support any verdict, and none is
offered.

## Triage note

Left at `discovery-log`. Cites `code-review` and `pr-review-toolkit` (both STACK, from
`anthropics/claude-plugins-official`) in "Overlaps with", which bands this P2, but the
differentiator is substantive rather than cosmetic: a published, reproducible benchmark harness
measuring recall and noise on golden PRs, which this catalog's own evidence-based philosophy
(ADR-0004's Verifiability signal) treats as valuable even from a small (12-star) project. A tool
that ships the means to measure whether a review pass helped or hurt is worth a real hands-on
look rather than a mechanical SKIP against the incumbent plugins.

_Triaged 2026-10-02 by the P2 challenger band (daily discovery pass)._
