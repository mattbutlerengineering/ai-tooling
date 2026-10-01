# Evaluation: claude-codex-coop

**Repo:** [youagainchen/claude-codex-coop](https://github.com/youagainchen/claude-codex-coop)
**Stars:** 19 | **Last updated:** 2026-10-01 (pushed) | **License:** MIT
**Last verified:** 2026-10-01
**Last triaged:** 2026-10-01  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Lets the Claude and Codex desktop apps call each other automatically to cross-review, cross-check,
or implement, with a live side panel showing model, token usage, and the full interaction log.
Structured so both models verify each other's findings before handing back a consolidated answer.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to support an
ADOPT, and none is offered here.

## Triage note

Left at `discovery-log`. Nothing it cites (`codex-with-chatgpt`, `codex-remote-pro`,
`claude-octopus`) is a STACK pick, so this isn't a P2 redundancy call — pure backlog. New (today,
19 stars) with no adoption signal, but a genuinely different mechanism from its closest peers
(bidirectional desktop-app calling rather than a browser/API bridge), worth a real look later.

_Triaged 2026-10-01 by the P3 backlog band (today's new lead)._
