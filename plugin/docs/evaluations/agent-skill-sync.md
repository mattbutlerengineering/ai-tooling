# Evaluation: agent-skill-sync

**Repo:** [kina-cmd/agent-skill-sync](https://github.com/kina-cmd/agent-skill-sync)
**Stars:** 18 | **Last updated:** 2026-09-12 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Plan (skill management)
**Layer:** Tooling

---

## What it does

A zero-dependency Python CLI that scans a machine's installed SKILL.md files, classifies each (A/B/C/D), and syncs them across toolchains (Codex, Claude Code, WorkBuddy) so a skill written for one harness doesn't have to be hand-copied to the others.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It overlaps `skills-hub` and `skill_manager` on cross-tool skill management, but neither is a STACK pick, and `skills-hub` is a desktop GUI app while this is a zero-dependency scriptable CLI with a scan/classify step neither peer has — a differentiated angle worth a real look rather than a mechanical SKIP. 18★ and 3 days old.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-skill-sync](https://github.com/kina-cmd/agent-skill-sync) | tool | Zero-dependency CLI (MIT) that scans, classifies (A/B/C/D), and syncs AI-agent SKILL.md files across toolchains | SKILL.md files diverge across Codex/Claude Code/WorkBuddy with nothing tracking or syncing them | skills-hub, skill_manager, skill-creator |
