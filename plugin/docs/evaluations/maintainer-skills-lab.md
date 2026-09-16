# Evaluation: maintainer-skills-lab

**Repo:** [00200200/maintainer-skills-lab](https://github.com/00200200/maintainer-skills-lab)
**Stars:** 14 | **Last updated:** 2026-09-16 (pushed) | **License:** MIT
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

16 reusable skills and 6 agents (Humanizer, ML debugging, PR review, Skill Watch, and more)
for Codex, Claude Code, Cursor, OpenCode, and Grok Bot.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `agent-skills` and `documentation-and-adrs`
(P2's catalogued incumbents) are narrower single-purpose skills; this is a broader
16-skill/6-agent bundle spanning maintenance tasks (humanizer, ML debugging, PR review,
skill watch) neither one covers on its own. Not clearly redundant with either single
component — left for a real look at the whole bundle.

_Triaged 2026-09-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [maintainer-skills-lab](https://github.com/00200200/maintainer-skills-lab) | plugin | 16 reusable skills + 6 agents (MIT) for Codex, Claude Code, Cursor, OpenCode, and Grok Bot — humanizer, ML debugging, PR review, skill watch | Maintainers rebuild the same review/debugging/documentation skills per project; want a portable, cross-harness bundle | godmode, headcount, agent-skills |
