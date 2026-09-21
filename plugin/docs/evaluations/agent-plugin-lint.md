# Evaluation: agent-plugin-lint

**Repo:** [AkaraChen/agent-plugin-lint](https://github.com/AkaraChen/agent-plugin-lint)
**Stars:** 0 | **Last updated:** 2026-09-21 (pushed) | **License:** MIT
**Last verified:** 2026-09-21
**Last triaged:** 2026-09-21  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A command-line linter (Rust, MIT) for [Agent Plugins](https://agent-plugins.org). Static analysis
only, no code execution: checks `plugin.json` (required fields, field types, plugin name, spec
version), `skills/` (skill discovery plus `SKILL.md` frontmatter names/descriptions), and `mcp.json`
configs and package paths for spec compliance, reporting issues with file locations and rule IDs.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow clone of
the repo (README, LICENSE, Cargo manifest) confirming it is real, MIT-licensed, and does what its
description claims. That is sufficient to catalog it and place it relative to existing peers, not to
support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog (pressure 0 — brand new, nothing cites it yet). No STACK incumbent it clearly duplicates:
`skilldoctor`/`skill-quality-suite` combine linting with security/prompt-injection scanning and
cross-harness compatibility checks, while this tool is narrower — pure spec-compliance static
analysis against the Agent Plugins format, with no security-audit claim. Left at `discovery-log`
rather than SKIPped as redundant; 0 stars and same-day activity mean it needs time before a
hands-on eval is worth the effort.

_Triaged 2026-09-21 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [agent-plugin-lint](https://github.com/AkaraChen/agent-plugin-lint) | tool | CLI linter (MIT) validating plugin.json, SKILL.md frontmatter, and mcp.json against the Agent Plugins spec, offline | Plugin authors have no static check that their manifest and skill/MCP configs meet spec before shipping | skilldoctor, skill-quality-suite, agnix |  |
