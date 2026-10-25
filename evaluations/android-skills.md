# Evaluation: android/skills

**Repo:** [android/skills](https://github.com/android/skills)
**Stars:** 9,700 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** Apache-2.0
**Last verified:** 2026-10-25
**Last triaged:** 2026-10-25  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A modular `SKILL.md` pack, maintained by the Android team, guiding coding agents
through Android development workflows that LLMs tend to perform poorly on — following
guidance from developer.android.com rather than restating well-known basics.
Installable via the Android CLI or as a Claude Code/Codex plugin.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own README (fetched over the web, since this session's GitHub API access is
scoped to this repository and does not extend to arbitrary repos) plus the CATALOG
"Overlaps with" cell. That is sufficient to place the lead against its closest catalog
peers, not to support any verdict, and none is offered here.

## Triage note

Cites `agent-skills` and `documentation-and-adrs` in its "Overlaps with" cell, which
bands this P2 challenger — but `agent-skills` (addyosmani, a STACK pick) is a general,
language-agnostic production-engineering skill pack, while `android/skills` is
Android-platform-specific. That is the same domain-specificity that kept
`vercel-labs/agent-skills` (React/Next-specific) at `discovery-log` rather than SKIPped
as redundant with the same general pack — a platform-specific skill set is additive to
a general one, not a competing claim on the same job. Left at `discovery-log`.

_Triaged 2026-10-25 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [android/skills](https://github.com/android/skills) | skill | Modular SKILL.md pack (Apache-2.0, ★9.7K) for AI-agent-assisted Android development, focused on workflows LLMs handle poorly per developer.android.com guidance | Agents lack curated, maintained Android-specific guidance beyond well-known basics; installable via Android CLI or as a Claude Code/Codex plugin | vercel-labs/agent-skills, agent-skills, awesome-copilot |
