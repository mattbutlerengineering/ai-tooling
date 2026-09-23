# Evaluation: code-quality (smixs)

**Repo:** [smixs/code-quality](https://github.com/smixs/code-quality)
**Stars:** 6 | **Last updated:** 2026-09-23 (pushed) | **License:** MIT
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A deterministic code-quality gate (TypeScript, MIT) for AI coding agents — git hooks that block test
tampering, hold a CRAP-metric bar on changed functions, and check diff coverage, secrets (gitleaks),
and dependencies (osv-scanner), across 12 languages behind one config file. Ships an optional Jev
classifier for judging test hunks, off by default.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the hook-based gates. That is sufficient to catalog it and place it
relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Overlaps `gap-trap` (rules-and-gates framework) and `tdd-guard`/`agent-delivery-gates`
(test-tampering-adjacent gates), but is the only one of the three combining a CRAP-metric bar,
diff-coverage check, secret scanning, and dependency scanning in one deterministic, multi-language
gate. Not a clean redundancy with any single incumbent; left at `discovery-log` for a hands-on
comparison against `gap-trap` specifically once both have real usage data.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [code-quality](https://github.com/smixs/code-quality) | tool | Deterministic code-quality gate (MIT) for AI coding agents — git hooks blocking test tampering, a CRAP-metric bar on changed functions, diff coverage, secrets, and dependency checks across 12 languages | AI agents can tamper with tests or ship low-quality diffs with nothing mechanically blocking it before commit | gap-trap, tdd-guard, agent-delivery-gates |  |
