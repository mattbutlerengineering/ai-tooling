# Evaluation: agentlint

**Repo:** [mauhpr/agentlint](https://github.com/mauhpr/agentlint)
**Stars:** 25 | **Last updated:** 2026-05-26 | **License:** MIT
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Real-time guardrails for AI coding agents — 77 rules across 8 packs (universal, quality, python, frontend, react, seo, security, autopilot) that hook into PreToolUse/PostToolUse events to block or warn on dangerous actions. Installs via `pip install agentlint` with one-command setup for 10 agent platforms (Claude Code, Cursor, Codex, Gemini, Kimi, Grok, Continue.dev, OpenAI Agents SDK, MCP hosts, generic). ERROR rules block the agent's action before it executes; WARNING rules inject advice into context; INFO rules appear in the session report.

The universal pack (24 rules) catches secrets, force-pushes, destructive commands, test weakening, debug artifacts, and dependency hygiene. The quality pack (7 rules) adds commit format, large diff warnings, file creation sprawl, and dead import detection. Stack-specific packs auto-activate based on project files — `pyproject.toml` triggers Python rules, `package.json` triggers frontend/react/seo rules.

The security pack (7 rules, opt-in) blocks Bash file writes, network exfiltration, credential leakage, and malicious URLs from curated feeds. The autopilot pack (18 rules, experimental) covers cloud infrastructure safety — production guards, dry-run enforcement, cross-account detection, and a subagent safety system that injects briefings on spawn and audits transcripts post-execution.

## How we tested it

Architecture review based on repo structure, README documentation, source layout, and test coverage. Not hands-on installed — evaluated from source inspection.

```bash
gh api repos/mauhpr/agentlint --jq '.description, .stargazers_count'
gh api repos/mauhpr/agentlint/contents/src/agentlint --jq '.[].name'
gh api repos/mauhpr/agentlint/contents/tests --jq '.[].name' | wc -l  # 43 test files
```

Key structural observations:
- **src/agentlint/packs/**: 8 rule packs with dedicated directories (universal, quality, python, frontend, react, seo, security, autopilot)
- **src/agentlint/adapters/**: multi-platform integration layer
- **src/agentlint/agentchute/**: optional cloud analytics (AgentChute) with explicit opt-in
- **tests/**: 43 test files covering engine, packs, adapters, CLI, and integration — unusually thorough for a 25-star repo
- **pyproject.toml + uv.lock**: modern Python packaging with uv

## What worked

- **Rule taxonomy is well-designed**: ERROR/WARNING/INFO severity levels with inline ignore directives (`# agentlint:ignore no-secrets`) and path exemptions — same ergonomics as eslint/ruff
- **Autopilot pack is unique**: no other catalog tool addresses cloud infrastructure safety for agents — production-guard, dry-run-required, bash-rate-limiter, cross-account-guard fill a real gap
- **Subagent safety**: addresses Claude Code's architectural limitation where parent hooks don't fire for subagent tool calls — safety briefing injection (SubagentStart) + post-hoc transcript auditing (SubagentStop) is a genuine innovation
- **Stack auto-detection**: automatically activates Python/frontend/React/SEO packs from project files — zero config for most projects
- **10-platform adapter architecture**: widest platform support of any guardrails tool in the catalog
- **Supply chain integration**: `no-compromised-dependency` (AgentChute feed), `no-vulnerable-version-install` (GHSA), `no-nvd-critical-cve-install` (NVD CVE) — layered vulnerability blocking
- **43 test files** for a 25-star repo indicates engineering discipline over growth metrics

## What didn't work or surprised us

- **25 stars despite v2.5.3 with 56 merged PRs** — suggests solo developer project with limited adoption signal; hard to gauge real-world reliability
- **Last commit May 26** — 3 weeks stale as of evaluation date, though the release cadence (v2.5.1–2.5.3 in consecutive days) shows burst activity
- **AgentChute cloud dependency** for advanced features (team budgets, compromised-package feeds, secret rulesets) — local-only mode loses supply chain intelligence
- **Python-only installation**: `pip install agentlint` means Python must be on the system even for TypeScript-only projects; no native npm/Go alternative
- **Security and autopilot packs are opt-in** — the most valuable rules require explicit configuration, which means many users never enable them
- **Overlap with Claude Code's built-in permission system**: Claude Code already blocks many dangerous operations (force-push, `rm -rf`, etc.) via its auto-mode classifier — agentlint's universal pack partially duplicates this

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | drift-detector and test-with-changes rules enforce test discipline |
| Speed | neutral | Hook execution adds ~milliseconds per tool call; no measurable impact |
| Maintainability | + | commit-message-format, max-file-size, no-dead-imports enforce code hygiene |
| Safety | ++ | Security pack blocks exfiltration, secret leaks, malicious URLs; autopilot pack prevents cloud disasters |
| Cost Efficiency | + | token-budget rule tracks session cost; bash-rate-limiter prevents runaway operations |

## Verdict

**CONDITIONAL**

Use when running agents on projects with cloud infrastructure access (AWS/GCP/Azure), when the security pack's supply chain blocking adds value beyond Claude Code's built-in guardrails, or when managing multi-platform agent teams (10 editors). The autopilot pack's infrastructure safety rules are genuinely unique — no other catalog tool addresses production-guard, dry-run enforcement, or subagent transcript auditing. Skip for solo Claude Code users on code-only projects where the built-in permission system already covers the dangerous actions. The 25-star count and solo-developer pattern mean you're early-adopting — evaluate hol-guard (CONDITIONAL, 361 stars) as a more battle-tested alternative for pre-execution scanning.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentlint](https://github.com/mauhpr/agentlint) | tool | Real-time guardrails for AI agents: 77 rules, 8 packs, inline ignores | Need runtime guardrails that prevent agents from doing dangerous things, not just scan after | SkillSpector, hol-guard |
