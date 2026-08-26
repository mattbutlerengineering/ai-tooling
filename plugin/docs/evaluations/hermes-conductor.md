# Evaluation: hermes-conductor

**Repo:** [forcewake/hermes-conductor](https://github.com/forcewake/hermes-conductor)
**Stars:** 65 | **Last updated:** 2026-08-25 (pushed) | **License:** MIT
**Last verified:** 2026-08-26
**Last triaged:** 2026-08-26  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A patterns-and-playbooks guide (not a standalone runnable tool) for orchestrating
multiple external coding CLIs (Claude Code, OpenCode, MiMo, etc.) under one conductor.
Documents controller-verified worktree lanes, recovery checklists, and structured
patterns to prevent agents claiming success without verification, parallel mutations
colliding in shared checkouts, and evidence-free completions — from 18 kanban boards
and the incidents that tried to break them.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool — there is nothing to install; it is a
documentation/patterns repository consumed by a Hermes Agent conductor. This
evaluation rests on the README and repo metadata only.

## Triage note

A methodology document, not a tool, so it's a different shape than its neighbors
(gastown, orca, agent-of-empires) — those are runnable orchestrators, this is the
worktree-lane-and-verification-gate playbook one might build such an orchestrator
from. Genuinely useful reading for anyone running multi-agent lanes, and not clearly
redundant with a runnable STACK pick. Left at `discovery-log` for a human to decide
whether it merits a real read-through eval or a reference-only catalog note.
