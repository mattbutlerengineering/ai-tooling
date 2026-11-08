# Evaluation: vibe-shield

**Repo:** [avivgerz-hue/vibe-shield](https://github.com/avivgerz-hue/vibe-shield)
**Stars:** 13 | **Last updated:** 2026-11-08 (pushed) | **License:** MIT
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A 60-rule static security scanner, MCP server, and skill-poisoning auditor for AI-generated
codebases, targeting Claude Code, Codex, and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient for the verdict below, because the
verdict turns on *redundancy with an already-adopted incumbent*, not on the tool's behaviour —
a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `SkillSpector`. `SkillSpector` is already a STACK pick covering the same
job (security scanning of AI agent skills for vulnerabilities and malicious patterns), and the
Security & Safety category already carries eight-plus overlapping scanners of this exact shape
(`skill-scanner`, `skilldoctor`, `skill-safety-checker`, `skill-quality-suite`, `ai-skill-scanner`,
`agent-plugin-lint`, `agent-scan`, `agentshield`). At 13 stars with no measured differentiation
from the incumbent, a second scanner here earns nothing a hands-on eval would change.

_Triaged 2026-11-08 by the P2 challenger band — challenges SkillSpector._
