# Evaluation: agentlint

**Repo:** [mauhpr/agentlint](https://github.com/mauhpr/agentlint)
**Stars:** 25 | **Last updated:** 2026-05-26 | **License:** MIT
**Dev loop stage:** Implement / Ship (runtime guardrail, not post-hoc Review)
**Layer:** Infrastructure

---

## What it does

Real-time guardrails for AI coding agents — 77 rules across 8 packs (universal, quality, python, frontend, react, seo, security, autopilot) that hook into PreToolUse/PostToolUse events to block or warn on dangerous actions. Installs via `pip install agentlint` with one-command setup for 10 agent platforms (Claude Code, Cursor, Codex, Gemini, Kimi, Grok, Continue.dev, OpenAI Agents SDK, MCP hosts, generic). ERROR rules block the agent's action before it executes; WARNING rules inject advice into context; INFO rules appear in the session report.

The universal pack (24 rules) catches secrets, force-pushes, destructive commands, test weakening, debug artifacts, and dependency hygiene. The quality pack (7 rules) adds commit format, large diff warnings, file creation sprawl, and dead import detection. Stack-specific packs auto-activate based on project files — `pyproject.toml` triggers Python rules, `package.json` triggers frontend/react/seo rules.

The security pack (7 rules, opt-in) blocks Bash file writes, network exfiltration, credential leakage, and malicious URLs from curated feeds. The autopilot pack (18 rules, experimental) covers cloud infrastructure safety — production guards, dry-run enforcement, cross-account detection, and a subagent safety system that injects briefings on spawn and audits transcripts post-execution.

## How we tested it

Source-grounded review: read the full README (all 8 pack rule tables), the recursive repo tree, the Claude Code setup guide (`docs/setup-claude.md`), and the plugin hook manifest (`plugin/hooks/hooks.json`) to confirm how the guardrails actually fire. **Not installed or run hands-on** — no rule was triggered live, so no trigger output or benchmark below is observed; all rule behavior is read from the documented spec, not measured. The decisive catalog question (does it move Safety, and is it differentiated from SkillSpector/hol-guard?) is answerable from the integration mechanism and rule taxonomy.

```bash
gh api repos/mauhpr/agentlint --jq '{stars,license:.license.spdx_id,description,pushed_at}'
gh api repos/mauhpr/agentlint/contents/README.md --jq '.content' | base64 -d
gh api "repos/mauhpr/agentlint/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/mauhpr/agentlint/contents/docs/setup-claude.md --jq '.content' | base64 -d
gh api repos/mauhpr/agentlint/contents/plugin/hooks/hooks.json --jq '.content' | base64 -d
```

Confirmed mechanism: the Claude Code integration is a set of native hooks (`agentlint setup claude` writes them into `.claude/settings.json`, or the marketplace plugin ships `plugin/hooks/hooks.json`). A `PreToolUse` hook matching `Bash|Edit|Write` runs `agentlint check` and returns `{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":"[no-secrets] …"}}` (exit 0) to **block the action before it executes**; WARNING rules return `additionalContext` advice; `PostToolUse`, `UserPromptSubmit`, `SubagentStart/Stop`, `Notification`, and `Stop` (session report) hooks cover the rest. This is genuine pre-execution prevention, not post-hoc scanning.

Key structural observations:
- **src/agentlint/packs/**: 8 rule packs with dedicated directories (universal, quality, python, frontend, react, seo, security, autopilot)
- **src/agentlint/adapters/**: multi-platform integration layer
- **src/agentlint/agentchute/**: optional cloud analytics (AgentChute) with explicit opt-in
- **tests/**: 43 test files covering engine, packs, adapters, CLI, and integration — unusually thorough for a 25-star repo
- **pyproject.toml + uv.lock**: modern Python packaging with uv

## What worked

- **Rule taxonomy is well-designed**: ERROR/WARNING/INFO severity levels with per-rule exemptions in `agentlint.yml` (`ignore_paths` + a `reason` field) and a session-level `suppress_rule(rule_id)` mechanism (ERRORs always enforced) — eslint/ruff-style ergonomics, though configured via YAML rather than inline source comments
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

Use when running agents on projects with cloud infrastructure access (AWS/GCP/Azure), when the security pack's supply-chain blocking adds value beyond Claude Code's built-in guardrails, or when managing multi-platform agent teams (10 editors). The autopilot pack's infrastructure safety rules are genuinely unique — no other catalog tool addresses production-guard, dry-run enforcement, or subagent transcript auditing. Skip for solo Claude Code users on code-only projects where the built-in permission system already covers the dangerous actions.

**Differentiation from overlaps.** agentlint occupies a distinct point in the agent-safety stack: it gates *the agent's own actions at runtime* (a PreToolUse hook that blocks the Write/Edit/Bash before it executes, plus PostToolUse advice). SkillSpector statically scans *third-party skill files* for malicious patterns before you install them — content provenance, not action control. hol-guard sits one layer lower as "AV": it wraps the harness launcher and snapshot/diffs *extensions and package installs* before execution. So the three are complementary, not substitutes — SkillSpector vets what you import, hol-guard vets what runs at launch, agentlint constrains what the agent does mid-session. The closest substitute is Claude Code's own permission classifier, which the universal pack partially duplicates; agentlint's net-new value is the security + autopilot packs and the cross-platform reach. The 25-star count and solo-developer pattern mean you're early-adopting — hol-guard (CONDITIONAL, 361 stars) is the more battle-tested neighbor if your concern is pre-execution scanning rather than per-action rules.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentlint](https://github.com/mauhpr/agentlint) | tool | Real-time guardrails for AI agents: 77 rules, 8 packs, inline ignores | Need runtime guardrails that prevent agents from doing dangerous things, not just scan after | SkillSpector, hol-guard |
