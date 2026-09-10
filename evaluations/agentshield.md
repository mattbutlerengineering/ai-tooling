# Evaluation: AgentShield

**Repo:** [affaan-m/agentshield](https://github.com/affaan-m/agentshield)
**Stars:** 1.2K | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-10
**Last triaged:** 2026-09-10  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An AI agent security scanner (CLI, GitHub Action, ECC plugin, and GitHub App) that detects
vulnerabilities in agent configurations, MCP servers, and tool permissions. Scans Claude
Code setups for hardcoded secrets, permission misconfigurations, hook-injection risk, MCP
server vulnerabilities, and agent prompt-injection vectors across 268 rules organized into
five security categories.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `SkillSpector` (STACK pick,
CONDITIONAL/MEASURED). SkillSpector scans skill packages for malicious patterns;
agentshield instead audits a live Claude Code *setup* — configs, hooks, MCP servers, and
tool-permission grants — for hardcoded secrets and misconfiguration across 268 named rules,
a different surface than skill-package scanning. Same author as the already-catalogued
`ECC` harness, with a plugin integration between the two, so this is a maintained project
rather than a one-off. Worth a real hands-on look rather than a redundancy call made from
the outside.

_Triaged 2026-09-10 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agentshield](https://github.com/affaan-m/agentshield) | tool | AI agent security scanner (MIT, ★1.2K) — detects vulnerabilities in agent configurations, MCP servers, and tool permissions across 268 rules; CLI, GitHub Action, ECC plugin, and GitHub App | Claude Code setups ship with no check for hardcoded secrets, permission misconfigurations, hook-injection risk, or MCP vulnerabilities | SkillSpector, skill-scanner, trustmcp, agent-scan |
