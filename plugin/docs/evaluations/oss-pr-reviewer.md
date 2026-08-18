# Evaluation: oss-pr-reviewer

**Repo:** [vuphongle/oss-pr-reviewer](https://github.com/vuphongle/oss-pr-reviewer)
**Stars:** 111 | **Last updated:** 2026-08-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-18
**Last triaged:** 2026-08-18  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An AI-powered CLI for reviewing GitHub pull requests — detects potential bugs, security
risks, regressions, and missing tests, and produces structured Markdown reports aimed at
open-source maintainers.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns
on *redundancy with a catalogued incumbent*, not on the tool's behaviour — a question the
overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `code-review` (already in STACK, MEASURED). `code-review`
(anthropics/claude-plugins-official) already does 4-agent parallel PR review with
confidence scoring, and `pr-review-toolkit` adds dimension-specific review agents on top
of it. oss-pr-reviewer's bug/security/regression/missing-test detection with Markdown
reports covers the same job with no differentiating capability; a second general-purpose
PR reviewer earns nothing here.

_Triaged 2026-08-18 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [oss-pr-reviewer](https://github.com/vuphongle/oss-pr-reviewer) | tool | AI-powered CLI (MIT) reviewing GitHub PRs for bugs, security risks, regressions, and missing tests, with Markdown reports | Open-source maintainers want automated PR review without a hosted per-seat service | juror, PR-Agent, open-code-review, code-review |
