# Evaluation: seanswarm

**Repo:** [ccai40359-wq/seanswarm](https://github.com/ccai40359-wq/seanswarm)
**Stars:** 53 | **Last updated:** 2026-09-16 (pushed) | **License:** MIT
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Multi-agent workflow skills for Claude Code, Codex, and Cursor: evidence-governed research
fan-out, dual-channel document reading, and dev delivery with independent review and visual
acceptance.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (claude-squad, oh-my-agent, agents-council). Not enough to
support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped, despite citing STACK pick `claude-squad` in its overlaps.
claude-squad is a lean TUI session manager for running parallel agent sessions; seanswarm is a
skill *pack* (multi-agent workflow skills: research fan-out, doc-reading, review/acceptance
gates) — a different mechanism solving an adjacent-but-distinct problem (skill-defined workflow
vs. session management). Treating a skill collection as redundant with a session-manager tool
would be the wrong-incumbent mistake this repo's own identity rules warn against. 53 stars, two
days old — worth a real eval if it keeps traction.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
