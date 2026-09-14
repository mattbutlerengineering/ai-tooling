# Evaluation: tldr

**Repo:** [SurefireStudios/tldr](https://github.com/SurefireStudios/tldr)
**Stars:** 5 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-14
**Last triaged:** 2026-09-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Skill making Claude Code, Cursor, Codex, Gemini CLI and 16 more agents lead with a 3-line TL;DR and fold detail instead of burying the answer in prose. Claims every measured run — including failed ones — is published, with a "demote, don't delete" policy for detail rather than dropping it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool, and did not verify the published per-model run claims. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell.

## Verdict

**discovery-log — tentative read** — new (created 2026-09-11), catalogued from today's discovery scan.

## Triage note

P2 challenger: cites `caveman` and `headroom` (both STACK picks) in Overlaps. All three touch response conciseness, but caveman/headroom compress *tool-output tokens before they reach the model*, while tldr restructures the *model's own response* (lead with a TL;DR, fold detail) — a different point in the pipeline. Left at discovery-log rather than SKIPped; a real eval would need to check whether the TL;DR discipline holds up outside the project's own published runs.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [tldr](https://github.com/SurefireStudios/tldr) | skill | Skill (MIT) making Claude Code, Cursor, Codex, Gemini CLI and 16 more agents lead with a 3-line TL;DR and fold detail instead of burying the answer in prose; every measured run, including failures, is published | Agent responses bury the answer in prose the reader has to scan; want a demote-don't-delete conciseness discipline | caveman, headroom, attention-control |  |
