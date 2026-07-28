# Evaluation: openhub

**Repo:** [24KaratAu/openhub](https://github.com/24KaratAu/openhub)
**Stars:** 20 | **Last updated:** 2026-07-23 | **License:** MIT
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement (sits beside the inner loop — discovers/installs tooling, not how the agent uses it)
**Layer:** Tooling

---

## What it does

A terminal discovery hub and package manager (Python/Textual TUI) for AI coding tools, MCP servers, and agent skills — browse and install across the fragmented ecosystem from one place.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 20 stars, MIT, pushed 2026-07-23) plus the CATALOG "Overlaps with" cell against skills-manage/vercel-labs/skills/capa/claude-code-templates. Sufficient to catalog and note the gap (broader discovery across tools+MCP servers+skills, not just skills), not to judge registry completeness or install reliability hands-on.

## Triage note

Broader in scope than skills-manage/vercel-labs/skills (skill-only) by also indexing MCP servers and coding-agent CLIs themselves, but at only 20 stars and 5 days old it's too early to tell if the registry has real coverage. No STACK incumbent to SKIP against. Left at discovery-log for a future hands-on eval once the registry matures.
