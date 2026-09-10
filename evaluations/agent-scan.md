# Evaluation: Agent Scan

**Repo:** [snyk/agent-scan](https://github.com/snyk/agent-scan)
**Stars:** 3.0K | **Last updated:** 2026-09-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-10
**Last triaged:** 2026-09-10  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Snyk's security scanner for AI agents, MCP servers, and agent skills. Auto-discovers
installed agent configurations (Claude Code/Desktop, Cursor, Gemini CLI, Windsurf) on the
machine it runs on and scans them for 15+ distinct risk classes, including prompt
injection, tool poisoning, and tool shadowing, across MCP servers and agent skills.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `SkillSpector` (STACK pick,
CONDITIONAL/MEASURED). SkillSpector scans *agent skill packages* specifically; agent-scan's
own description covers a broader surface — installed agent configs, MCP servers, *and*
skills, with auto-discovery across four named clients (Claude Code/Desktop, Cursor, Gemini
CLI, Windsurf) rather than a single skill package at a time. Backed by an established
security vendor (Snyk) rather than a first-time author, which is itself a reason to look
closer rather than dismiss as a duplicate — a false SKIP here would be the expensive
direction. Worth a real hands-on comparison against SkillSpector before concluding either
way.

_Triaged 2026-09-10 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-scan](https://github.com/snyk/agent-scan) | tool | Snyk's security scanner for AI agents, MCP servers, and agent skills (Apache-2.0, ★3K) — auto-discovers installed configs (Claude Code/Desktop, Cursor, Gemini CLI, Windsurf) and flags 15+ risks including prompt injection, tool poisoning, and tool shadowing | Downloaded skills/MCP servers/agent configs can carry prompt injection or exfiltration with no vendor-backed scanner checking installed state | SkillSpector, skill-scanner, trustmcp, agentshield |
