# Evaluation: arnold

**Repo:** [PhonePe/arnold](https://github.com/PhonePe/arnold)
**Stars:** 34 | **Last updated:** 2026-11-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

A self-hosted code review platform over GitHub/GitLab MRs/PRs, from PhonePe: a prioritised merge queue, a full review workspace, and AI review workflows that post inline findings back to the forge, using any OpenAI-compatible model.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — a heavier, self-hosted platform (merge queue + review workspace), a different deployment shape than the plugin incumbents it's compared against.

## Triage note

Left at `discovery-log`, not SKIPped. It cites `code-review` and `pr-review-toolkit` in Overlaps, but those are lightweight Claude Code plugins, while arnold is a self-hosted platform with its own merge queue and review workspace — a different operational commitment, not a drop-in substitute. Not clearly dominated either way; deserves a real eval rather than a mechanical redundancy call.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [arnold](https://github.com/PhonePe/arnold) | platform | Self-hosted code review platform (Apache-2.0) over GitHub/GitLab MRs/PRs — prioritised merge queue, review workspace, AI review against any OpenAI-compatible model | Teams running AI-assisted review on GitHub/GitLab MRs want a self-hosted merge queue and review workspace instead of a SaaS bot | openreview, code-review, pr-review-toolkit |
