# Evaluation: cdmx-in/security-review

**Repo:** [cdmx-in/security-review](https://github.com/cdmx-in/security-review)
**Stars:** 3 | **Last updated:** 2026-08-07 (pushed) | **License:** MIT
**Last verified:** 2026-08-11
**Last triaged:** 2026-08-11  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code skill (MIT) that chains real security scanners — Semgrep, gitleaks, TruffleHog, Trivy, osv-scanner, ZAP — then verifies every finding against source before reporting. Covers SAST, secrets across full git history, SCA, IaC, and Supabase/Firebase RLS checks, with one report tagged to OWASP Top 10 2025.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and README/topic description. Whether the source-verification step meaningfully cuts false positives from the underlying scanners is untested here.

## Verdict

**discovery-log — tentative read**

## Triage note

Newly discovered and catalogued today. Left at `discovery-log`, not SKIPped as redundant with `SkillSpector` — SkillSpector scans *agent skill packages* for malicious/injected code, while this tool orchestrates conventional AppSec scanners (Semgrep/gitleaks/TruffleHog/Trivy/osv-scanner/ZAP) against a *project's own codebase*. Different targets, not a clean overlap despite both sitting in Security & Safety. Very early-stage (3 stars, single contributor) — worth another look once it has more adoption signal.

_Triaged 2026-08-11 by the daily discovery-and-triage pass._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cdmx-in/security-review](https://github.com/cdmx-in/security-review) | skill | Claude Code skill (MIT) chaining real scanners (Semgrep, gitleaks, TruffleHog, Trivy, osv-scanner, ZAP) and verifying every finding against source, tagged to OWASP Top 10 2025 | Agent-run security scans produce untriaged noise; want real-tool findings verified against source before reporting | ghostsecurity/skills, SkillSpector, garak |
