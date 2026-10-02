# Evaluation: claude-cybersecurity

**Repo:** [AgriciDaniel/claude-cybersecurity](https://github.com/AgriciDaniel/claude-cybersecurity)
**Stars:** 225 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** MIT
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

An AI-powered cybersecurity code-review skill for Claude Code — deploys 8 specialist agents
covering vulnerability detection, authorization flaws, exposed secrets, supply-chain risk,
IaC security, threat patterns, AI-generated-code concerns, and business-logic defects, mapped to
OWASP 2025 and CWE Top 25 across 14 languages with zero configuration.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Sufficient to place the lead, not to support any verdict, and none is offered.

## Triage note

Left at `discovery-log`. No STACK pick is cited in its "Overlaps with" cell, so this bands P3 —
nothing structural forces a disposition. The catalog already holds several security-skill bundles
(ghostsecurity/skills, Anthropic-Cybersecurity-Skills, Claude-BugHunter, cdmx-in/security-review),
but this one's differentiator — 8 parallel specialist agents each targeting a distinct defect
class, with real adoption (225 stars) — is specific enough to be worth a real look rather than a
mechanical SKIP, and nothing bands it for mechanical disposal today.

_Triaged 2026-10-02 by the P3 backlog band (daily discovery pass)._
