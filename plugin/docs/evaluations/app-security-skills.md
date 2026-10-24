# Evaluation: app-security-skills

**Repo:** [defi0x1/app-security-skills](https://github.com/defi0x1/app-security-skills)
**Stars:** 10 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-24
**Last triaged:** 2026-10-24  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Claude Code skill (`appsec`) combining security and code-quality review in one
pass: every finding must pass an explicit verification gate, facts the repo cannot
prove are labelled "needs validation" instead of guessed, and hunting is driven by
invariants and trust boundaries rather than keyword lists.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Triage banded this as a P2 challenger against `code-review` (the STACK incumbent,
pressure 0 — the citation is one-directional so far). `code-review`'s multi-agent
confidence-scored review and `brooks-lint`'s book-grounded decay-risk review are both
general code-review tools; this one's specific claim — findings must pass a
verification gate or get labelled unproven, rather than reported as plausible-sounding
guesses — is a methodology difference, not obviously dominated by either incumbent.
Left at `discovery-log` for a real hands-on eval rather than a mechanical SKIP.

_Triaged 2026-10-24 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [app-security-skills](https://github.com/defi0x1/app-security-skills) | skill | Code review skill (MIT) combining security and quality in one pass, labeling unproven findings "needs validation" | Automated review either buries findings in plausible-sounding noise or misses the bug living in the gap between two components | code-review, brooks-lint, cdmx-in/security-review |
