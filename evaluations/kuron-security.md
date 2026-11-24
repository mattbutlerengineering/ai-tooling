# Evaluation: kuron-security

**Repo:** [shirokun20/kuron-security](https://github.com/shirokun20/kuron-security)
**Stars:** 8 | **Last updated:** 2026-11-23 (pushed) | **License:** NOASSERTION (⚠️ no declared license found by GitHub)
**Last verified:** 2026-11-24
**Last triaged:** 2026-11-24  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An evidence-first security scanner for any AI coding agent's output — taint-chain findings, 3-lens verification, honest provenance labels, SARIF 2.1.0 output, and live progress reporting. Standalone; no Workflow tool required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a P3 stamp, not for a verdict.

## Verdict

**discovery-log — tentative read** — a very new (★8), early-stage entrant in an already crowded security-scanner niche; no STACK pick is clearly dominant over it yet.

## Triage note

Left at `discovery-log`, stamped. No STACK pick is cited in its Overlaps cell, so it doesn't qualify for a P2 redundancy SKIP, and `Type: tool` (not vendored) means P4's license-based mechanical skip doesn't apply even though the license is NOASSERTION. Too early/thin a signal (★8, 1-day-old) for a confident call either way.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kuron-security](https://github.com/shirokun20/kuron-security) | tool | Evidence-first security scanner (⚠️ no declared license) for any AI coding agent — taint-chain findings, 3-lens verification, honest provenance labels, SARIF 2.1.0 | AI-agent-written code ships with no fast scanner tracing taint chains end-to-end or disclosing how confident each finding is | safe-anything, agent-scan, ai-skill-scanner |
