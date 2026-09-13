# Evaluation: agent-launcher

**Repo:** [agent-launch/agent-launcher](https://github.com/agent-launch/agent-launcher)
**Stars:** 81 | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-13
**Last triaged:** 2026-09-13  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Cross-platform Electron desktop app that configures and launches existing
coding-agent CLIs (Claude Code, Codex, Gemini CLI, and others) from one place,
instead of installing/configuring each CLI separately.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the
lead and note it isn't redundant with an existing STACK pick; it would not support an
ADOPT, and this eval offers none.

## Triage note

Overlaps `ai-terminal-manager` (tmux-based, terminal-only) and
`agentic-stack-desktop` (macOS-only, knowledge-graph-focused) but is neither: a
cross-platform Electron GUI purely for launching/configuring CLIs, no shared memory
or session unification claim. None of its overlaps is a STACK pick, so no overlap
pressure yet. Left at `discovery-log`; differentiated enough (and early enough — 81
stars in 3 days) to deserve a real eval rather than a mechanical disposition.

## Verdict

**discovery-log — tentative read** — a cross-platform coding-agent-CLI launcher
worth a look if the desktop-app angle turns out to matter; not evaluated hands-on.
