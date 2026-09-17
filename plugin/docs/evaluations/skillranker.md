# Evaluation: skillranker

**Repo:** [Dicklesworthstone/skillranker](https://github.com/Dicklesworthstone/skillranker)
**Stars:** 3 | **Last updated:** 2026-09-17 (pushed) | **License:** "MIT + Open AI/Anthropic rider" (per README badge; not a plain MIT grant)
**Last verified:** 2026-09-17
**Last triaged:** 2026-09-17  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Standalone Rust CLI that puts TypeSafe.ai's Jev at the center of skill selection — evaluates an
agent's current context (conversation history, available procedures, workspace signals) and
recommends which installed skill to use next, with Claude Code hooks and the ability for the
agent to decline the recommendation. Requires a TypeSafe API key.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (jump-skills, Only-Skill-You-Need, skill-creator). That is
sufficient to place the lead, not to judge the tool's behaviour hands-on.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `skill-creator` — `skill-creator` authors
and packages skills, this tool selects among already-installed ones at runtime, which is the same
job as `jump-skills`/`Only-Skill-You-Need` (routing) rather than `skill-creator`'s (authoring).
Very early signal (★3, created today) and a paid third-party dependency (a TypeSafe API key) are
both worth noting for whoever picks this up next; neither is grounds for a mechanical SKIP on its
own.

_Triaged 2026-09-17 by the P2 challenger band._
