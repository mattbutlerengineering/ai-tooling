# Evaluation: crommacode

**Repo:** [CrommaAI/crommacode](https://github.com/CrommaAI/crommacode)
**Stars:** 52 | **Last updated:** 2026-11-12 (pushed) | **License:** NOASSERTION (⚠️ no LICENSE file detected)
**Last verified:** 2026-11-15
**Last triaged:** 2026-11-15  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A gamified desktop IDE that watches Claude Code, Codex, Gemini CLI, Cursor
CLI, or OpenCode work as a live game, and can send a swarm of worker agents.
Free for macOS, Windows, and Linux.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a
P3 leave/stamp disposition, not for an ADOPT/KEEP claim about the tool's
behavior.

## Triage note

No structural disqualifier that applies to a `tool` Type (the missing LICENSE
file would only mechanically SKIP a vendored `skill`/`plugin`, not a run-as-a-
program tool). Overlaps thematically with `lot-map`/`sitrep` (live session
observability) but with a distinct gamified-swarm angle. Left at
`discovery-log` for a full hands-on eval rather than a mechanical SKIP.

_Triaged 2026-11-15 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [crommacode](https://github.com/CrommaAI/crommacode) | tool | Gamified IDE (⚠️ license NOASSERTION) watching Claude Code, Codex, Gemini CLI, Cursor CLI, or OpenCode work, with swarms of worker agents | Watching several coding-agent sessions work has no shared, game-like live view across harnesses | lot-map, sitrep, claude-super-sidebar |
