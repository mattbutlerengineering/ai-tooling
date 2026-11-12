# Evaluation: owner-decisions-skill

**Repo:** [nyxandro/owner-decisions-skill](https://github.com/nyxandro/owner-decisions-skill)
**Stars:** 2 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Process

---

## What it does

A private decision log for Claude Code, Codex, OpenCode, and Cursor spanning all of a
user's projects: the agent settles a question the way a similar one was already answered
in a past project, asks only what's genuinely new, and records the answer, per the repo's
own description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell. That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `claude-reflect` (STACK, KEEP,
MEASURED) despite the overlap. `claude-reflect` captures corrections/preferences and
syncs them into one repo's `CLAUDE.md`; this skill's stated scope is explicitly
cross-project (a decision made in one repo answers a similar question in another), which
`claude-reflect` does not claim. Whether that cross-project claim holds up needs a
hands-on eval, not a mechanical SKIP — very low star count (★2) also argues for watching
rather than evaluating yet.
