# Evaluation: OpenSSF Scorecard

**Repo:** [ossf/scorecard](https://github.com/ossf/scorecard)
**Stars:** 5,532 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Outer Loop
**Layer:** Infrastructure

---

## What it does

Automated security health assessment for open source projects. Runs 19 checks (Binary-Artifacts, Branch-Protection, CI-Tests, CII-Best-Practices, Code-Review, Contributors, Dangerous-Workflow, Dependency-Update-Tool, Fuzzing, License, Maintained, Packaging, Pinned-Dependencies, SAST, Security-Policy, Signed-Releases, Token-Permissions, Vulnerabilities, Webhooks) and assigns each a 0–10 score. Aggregate score is risk-weighted: Critical checks (Dangerous-Workflow, Webhooks) count 4× more than Low checks (CI-Tests, License). Available as CLI, GitHub Action, REST API, and BigQuery public dataset covering the 1M most critical OSS projects.

## How we tested it

**Evidence:** REVIEW

Queried the REST API for two projects to assess output quality:

```bash
# Self-assessment (the scorecard repo itself)
curl -sL "https://api.scorecard.dev/projects/github.com/ossf/scorecard"
# → Score: 9/10, all checks pass except minor Pinned-Dependencies issues

# A major dependency (TypeScript)
curl -sL "https://api.scorecard.dev/projects/github.com/microsoft/TypeScript"
# → Score: 7.9/10, 9 unfixed vulnerabilities, no signed releases, no CII badge
```

The TypeScript result surfaced 9 known vulnerabilities with GHSA identifiers, unpinned npm dependencies in CI workflows, and missing release signatures — all actionable and not information readily available from `gh api` alone.

Also attempted CLI install (`brew install scorecard` — formula confirmed to exist) but focused on the API since the REST API and GitHub Action are the primary integration paths for agent workflows.

**Re-verified live (2026-06-20):** the public API needs no key and returned exactly these scores on re-run — `ossf/scorecard` = **9** (Code-Review / Maintained / Security-Policy / Dangerous-Workflow all 10) and `microsoft/TypeScript` = **7.9**. So the figures above are confirmed, not estimated.

## What worked

- **Actionable per-check detail**: each check returns a reason string and detail array — e.g., Token-Permissions lists every workflow file with excessive permissions, with exact line numbers
- **Risk-weighted scoring**: Critical/High/Medium/Low tiers mean the aggregate score reflects actual risk, not just checkbox completion
- **GitHub Action integration**: runs on every push, results appear in the Security tab — zero-config after initial setup
- **Public dataset**: BigQuery table of 1M projects enables dependency risk assessment without running the tool yourself
- **REST API**: pre-calculated scores with CDN caching for instant lookups during planning — no need to install anything

## What didn't work or surprised us

- **Case-sensitive API**: `microsoft/typescript` returns empty, `microsoft/TypeScript` works — unexpected for a URL-based API
- **Coverage gaps**: REST API omits CI-Tests, Contributors, and Dependency-Update-Tool checks for batch-scanned projects due to API cost
- **Not project-local**: scorecard assesses upstream dependencies and other repos, not your own code quality — complementary to linters and code review, not a replacement
- **CLI install overhead**: Go binary with GitHub token requirements for full check coverage (some checks need `repo` scope PAT)

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't check code correctness — assesses project health practices |
| Speed | + | REST API gives instant dependency risk assessment during planning |
| Maintainability | + | Identifies repos lacking code review, dependency updates, and maintenance activity |
| Safety | ++ | Primary value: surfaces vulnerabilities, dangerous workflows, missing security policies, unsigned releases |
| Cost Efficiency | neutral | Free tool and API; BigQuery queries may incur GCP costs at scale |

## Verdict

**CONDITIONAL**

Use when evaluating dependencies or assessing the security posture of upstream projects before adoption. The GitHub Action is valuable for your own repos if you need a security health dashboard. Skip for day-to-day coding workflows — it's an outer-loop assessment tool, not an inner-loop quality gate. Complements SkillSpector (which scans skills for malicious patterns) and hol-guard (which scans before execution); scorecard assesses the project-level health that those tools can't see.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [scorecard](https://github.com/ossf/scorecard) | tool | OpenSSF security health metrics — 19 automated checks for open source projects | Can't quickly assess if a dependency or tool is maintained and secure | SkillSpector (complementary: scorecard = project health, SkillSpector = skill content scanning) |
