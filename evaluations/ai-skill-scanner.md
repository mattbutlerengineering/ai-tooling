# Evaluation: ai-skill-scanner

**Repo:** [suchithnarayan/ai-skill-scanner](https://github.com/suchithnarayan/ai-skill-scanner)
**Stars:** 15 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An LLM-powered security scanner for Claude Code plugins and skills — scans manifests, skills,
hooks, and MCP/LSP configs across 17 risk categories, combining LLM analysis (six provider
options) with 235 static YAML rules; outputs JSON/SARIF and an interactive graph.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Sufficient to support this SKIP (a redundancy call turning on overlap, not on behavior), not
enough for any ADOPT-direction verdict.

## Verdict

**SKIP** — redundant with `SkillSpector` (STACK, CONDITIONAL/MEASURED). The catalog already
carries a dozen skill/plugin security scanners (SkillSpector, skill-scanner, skilldoctor,
skill-safety-checker, skill-quality-suite, agent-plugin-lint, agent-scan, agentshield, trustmcp,
mcp-audit-tool) covering the same threat model (prompt injection, exfiltration, supply-chain risk
in SKILL.md/plugin manifests) before install. ai-skill-scanner's differentiator — LLM-based
evidence triage layered on static rules, with CI/PR diff scanning — is an incremental detection-
method change on an already heavily-covered job, at 15 stars against SkillSpector's established
STACK position. Not a fundamentally different capability the way, say, a reverse-engineering MCP
server would be; a 13th scanner in this niche does not earn a first-time hands-on eval over the
incumbent.

_Triaged 2026-10-02 by the P2 challenger band (daily discovery pass)._
