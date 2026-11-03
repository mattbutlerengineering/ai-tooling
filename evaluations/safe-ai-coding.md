# Evaluation: safe-ai-coding

**Repo:** [sami-hussain-dev/safe-ai-coding](https://github.com/sami-hussain-dev/safe-ai-coding)
**Stars:** 4 | **Last updated:** 2026-10-30 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code skill and plugin that asks before risky actions, flags hallucinated code,
catches prompt injection, SQL injection, and leaked secrets, reviews every change, and
writes PDF reports of what it found.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. At 4 stars and days old, whether the detection
rules actually catch the vulnerability classes it claims (versus a plausible-sounding
README) is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [safe-ai-coding](https://github.com/sami-hussain-dev/safe-ai-coding) | skill | Claude Code skill/plugin (MIT) catching hallucinated code, prompt injection, SQL injection, and leaked secrets | AI coding agents take risky actions and ship vulnerable code with no pre-action check, review, or audit trail | agentshield, patchbot, skill-safety-checker |
