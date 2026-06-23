# Evaluation: ghostsecurity/skills

**Repo:** [ghostsecurity/skills](https://github.com/ghostsecurity/skills)
**Stars:** 393 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A Claude Code plugin providing 7 skills for application security scanning, covering the full AppSec pipeline: repository context mapping (`ghost-repo-context`), static code analysis (`ghost-scan-code`), dependency vulnerability scanning (`ghost-scan-deps`), secrets detection (`ghost-scan-secrets`), finding validation (`ghost-validate`), HTTP proxy for live testing (`ghost-proxy`), and combined reporting (`ghost-report`). Each skill is a multi-step orchestrator that spawns subagents for planning, scanning, verifying, and summarizing — not just a prompt that tells the agent to "look for vulnerabilities."

The scan-code skill alone covers 103 vulnerability vectors across 4 project types (backend, frontend, mobile, library), organized by OWASP category (injection, authz, authn, crypto, data exposure, etc.). Each vector has per-severity thresholds, CWE mappings, file-candidate heuristics, and multi-criteria validation rules. The verifier agent independently re-checks every finding against the source code before it reaches the report.

## How we tested it

**Evidence:** REVIEW

Architecture review of all 7 SKILL.md files and supporting prompts/criteria. Read the full scan-code pipeline (planner → nominator → analyzer → verifier), the backend.yaml criteria for injection/authz vectors, the validate SKILL.md for live DAST flow, and the scan-deps orchestrator for SCA pipeline.

```
gh api repos/ghostsecurity/skills/git/trees/main?recursive=1 --jq '.tree[].path'
# 79 files: 7 SKILL.md files, 4 criteria YAML files, 5 prompt files, 1 loop script
# Read: scan-code/SKILL.md, repo-context/SKILL.md, validate/SKILL.md, scan-deps/SKILL.md
# Read: criteria/index.yaml, criteria/backend.yaml, prompts/verifier.md
```

Not hands-on tested (requires a project with security-relevant code to scan meaningfully). Evaluation is architecture-and-content review.

## What worked

- **103 vulnerability vectors with per-criteria validation** — each vector in `criteria/backend.yaml` has specific candidate file heuristics, CWE mapping, severity tiers, and 3-4 boolean criteria that must be independently confirmed. This is practitioner-level specificity, not a generic OWASP checklist.
- **Independent verifier agent** — the scan-code pipeline has a dedicated verifier step that re-reads the source, checks line number accuracy, validates each criterion independently, and checks for missed mitigations. This is the kind of adversarial verification that prevents false positives from reaching reports.
- **Full AppSec pipeline in one plugin** — repo context → SAST → SCA → secrets → DAST validation → combined report. Each skill can be invoked independently, and they share cached repo context via `~/.ghost/repos/`.
- **Live validation via proxy** — the `ghost-validate` skill can confirm findings against a running application using `ghost-proxy` (HTTP interception), turning static findings into confirmed exploits. This is a DAST capability rare in agent tooling.
- **Proper orchestration pattern** — scan-deps and scan-secrets use the Task tool to spawn subagents, keeping context clean. scan-code uses a bash loop script for resumable execution with timeout handling.

## What didn't work or surprised us

- **Low star count (393) relative to quality** — this is significantly underrated compared to the star-inflated alternatives. The criteria YAML files alone contain more security depth than most 10K+ star security skill collections.
- **Requires custom binaries** — scan-deps installs "wraith" and scan-secrets installs "poltergeist" (Ghost Security's own binaries). These aren't open-source tools you can audit — you're trusting Ghost Security's closed-source scanners. The skills orchestrate around them rather than using only open tools.
- **Tool restrictions are inconsistent** — scan-code allows `Read, Write, Edit, Glob, Grep, Bash` while scan-deps allows `Read, Glob, Grep, Bash, Task, TodoRead, TodoWrite`. No explanation for why some have Task access and others don't.
- **No auto-triggering** — skills must be manually invoked (`/ghost-scan-code`). No hooks for pre-commit or pre-push scanning. Compare with agentlint which has runtime guardrails.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Independent verifier agent reduces false positives; 103-vector coverage catches real issues |
| Speed | neutral | Multi-agent pipeline is thorough but slow — full scan is token-expensive |
| Maintainability | neutral | Doesn't affect code quality directly; findings feed review process |
| Safety | ++ | Full AppSec pipeline (SAST + SCA + secrets + DAST) in one plugin; 103 vectors with per-criteria thresholds |
| Cost Efficiency | - | Multi-agent orchestration with subagent spawning uses significant tokens, especially at `full` depth |

## Verdict

**CONDITIONAL**

Use when your project needs structured security scanning beyond what trailofbits/skills provides. trailofbits/skills (ADOPT) gives you audit methodology — how to systematically review code for security issues. ghostsecurity/skills gives you automated scanning pipelines — SAST, SCA, secrets, and DAST validation with 103 vulnerability vectors and independent verification. They're complementary: trailofbits for manual security review discipline, ghostsecurity for automated scanning coverage. The closed-source scanner binaries (wraith, poltergeist) are a trust tradeoff — you get deeper SCA/secrets scanning but can't audit the scanner itself.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ghostsecurity/skills](https://github.com/ghostsecurity/skills) | skill | AppSec skills for AI coding agents — SAST, SCA, secrets, DAST with 103 vulnerability vectors | Need automated security scanning with per-criteria validation and independent verification | trailofbits/skills (complementary: methodology vs scanning), SkillSpector, Anthropic-Cybersecurity-Skills |
