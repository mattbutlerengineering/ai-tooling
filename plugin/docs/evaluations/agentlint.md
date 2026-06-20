# Evaluation: agentlint

**Repo:** [mauhpr/agentlint](https://github.com/mauhpr/agentlint)
**Stars:** 25 | **Last updated:** 2026-05-26 | **License:** MIT
**Dev loop stage:** Implement / Ship (runtime guardrail, not post-hoc Review)
**Layer:** Infrastructure

---

## What it does

Real-time guardrails for AI coding agents — 78 rules across 8 packs (universal, quality, python, frontend, react, seo, security, autopilot) that hook into PreToolUse/PostToolUse events to block or warn on dangerous actions. Installs via `pip install agentlint` with one-command setup for 10 agent platforms (Claude Code, Cursor, Codex, Gemini, Kimi, Grok, Continue.dev, OpenAI Agents SDK, MCP hosts, generic). ERROR rules block the agent's action before it executes; WARNING rules inject advice into context; INFO rules appear in the session report.

The universal pack (24 rules) catches secrets, force-pushes, destructive commands, test weakening, debug artifacts, and dependency hygiene. The quality pack (7 rules) adds commit format, large diff warnings, file creation sprawl, and dead import detection. Stack-specific packs auto-activate based on project files — `pyproject.toml` triggers Python rules, `package.json` triggers frontend/react/seo rules.

The security pack (7 rules, opt-in) blocks Bash file writes, network exfiltration, credential leakage, and malicious URLs from curated feeds. The autopilot pack (18 rules, experimental) covers cloud infrastructure safety — production guards, dry-run enforcement, cross-account detection, and a subagent safety system that injects briefings on spawn and audits transcripts post-execution.

## How we tested it

Installed it for real (`pip install agentlint`, **v2.5.x, 78 rules** via `agentlint list-rules`) and exercised the core mechanism — `agentlint check`, which evaluates a tool call from stdin and emits a Claude Code hook decision. Fed it dangerous and benign Bash calls and watched what it blocked, both at default config and with the opt-in packs enabled.

```bash
# default config (agentlint init -> packs: universal, quality)
echo '{"tool_name":"Bash","tool_input":{"command":"rm -rf /"}}' | agentlint check --event PreToolUse
# -> {"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":
#     "[no-destructive-commands] Catastrophic command detected: rm -rf on root or home directory ..."}}

echo '{"tool_name":"Bash","tool_input":{"command":"ls -la"}}' | agentlint check --event PreToolUse
# -> (no output) ALLOWED

# DROP DATABASE and `terraform apply` were NOT blocked at default config...
echo '{"tool_name":"Bash","tool_input":{"command":"psql -c \"DROP DATABASE prod\""}}' | agentlint check --event PreToolUse
# -> (no output) ALLOWED   <-- destructive-confirmation-gate is in the opt-in autopilot pack

# ...until autopilot + security packs are enabled in agentlint.yml:
echo '{...DROP DATABASE prod...}'        | agentlint check --event PreToolUse
# -> deny: "[destructive-confirmation-gate] Catastrophic operation requires explicit confirmation: DROP DATABASE"
echo '{...terraform apply -auto-approve}'| agentlint check --event PreToolUse
# -> deny: "[dry-run-required] Infrastructure apply without preview: terraform apply -> Run terraform plan first"
echo '{...git status...}'                | agentlint check --event PreToolUse
# -> (no output) ALLOWED
```

**Verified mechanism (matches the docs exactly):** `agentlint check` returns `{"hookSpecificOutput":{"permissionDecision":"deny","permissionDecisionReason":"[rule-id] …"}}` at exit 0 — genuine pre-execution *prevention*, the native Claude Code deny payload, not post-hoc scanning. The Claude Code integration wires this as a `PreToolUse` hook (`agentlint setup claude` writes `.claude/settings.json`, or the marketplace plugin ships `plugin/hooks/hooks.json`); WARNING rules return `additionalContext` advice instead of denying.

**Key measured finding — the powerful guardrails are opt-in.** `agentlint init` enabled only `universal` + `quality`. Out of the box it caught catastrophic `rm -rf /`, but **DROP DATABASE and `terraform apply -auto-approve` passed untouched** because `destructive-confirmation-gate` and `dry-run-required` live in the **autopilot** pack, which is commented out by default (so is `security`). After uncommenting both packs in `agentlint.yml`, all three fired correctly with actionable bypass guidance, and benign commands (`git status`, `ls`) stayed allowed. Anyone installing agentlint *expecting* production/infra protection won't have it until they opt in.

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
| Safety | ++ | Verified: `rm -rf /` denied at default config; DROP DATABASE + `terraform apply` denied once autopilot pack enabled, with benign commands allowed |
| Cost Efficiency | + | token-budget rule tracks session cost; bash-rate-limiter prevents runaway operations |

## Verdict

**CONDITIONAL**

Use when running agents on projects with cloud infrastructure access (AWS/GCP/Azure), when the security pack's supply-chain blocking adds value beyond Claude Code's built-in guardrails, or when managing multi-platform agent teams (10 editors). The autopilot pack's infrastructure safety rules are genuinely unique — no other catalog tool addresses production-guard, dry-run enforcement, or subagent transcript auditing. Skip for solo Claude Code users on code-only projects where the built-in permission system already covers the dangerous actions.

**Differentiation from overlaps.** agentlint occupies a distinct point in the agent-safety stack: it gates *the agent's own actions at runtime* (a PreToolUse hook that blocks the Write/Edit/Bash before it executes, plus PostToolUse advice). SkillSpector statically scans *third-party skill files* for malicious patterns before you install them — content provenance, not action control. hol-guard sits one layer lower as "AV": it wraps the harness launcher and snapshot/diffs *extensions and package installs* before execution. So the three are complementary, not substitutes — SkillSpector vets what you import, hol-guard vets what runs at launch, agentlint constrains what the agent does mid-session. The closest substitute is Claude Code's own permission classifier, which the universal pack partially duplicates; agentlint's net-new value is the security + autopilot packs and the cross-platform reach. The 25-star count and solo-developer pattern mean you're early-adopting — hol-guard (CONDITIONAL, 361 stars) is the more battle-tested neighbor if your concern is pre-execution scanning rather than per-action rules.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentlint](https://github.com/mauhpr/agentlint) | tool | Real-time guardrails for AI agents: 78 rules, 8 packs, inline ignores | Need runtime guardrails that prevent agents from doing dangerous things, not just scan after | SkillSpector, hol-guard |
