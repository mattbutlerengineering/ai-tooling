# Evaluation: claude-command-center

**Repo:** [amirfish1/claude-command-center](https://github.com/amirfish1/claude-command-center)
**Stars:** 182 | **Last updated:** 2026-10-11 (pushed) | **License:** FSL-1.1-MIT (source-available; converts to MIT 2 years after each release — releases before 2026-07-28 are already MIT)
**Last verified:** 2026-10-11
**Last triaged:** 2026-10-11  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local-first dashboard ("CCC") that puts sessions from several coding-agent CLIs —
Claude Code, Codex, Cursor, and five more — on one board and flags which session is
stalled waiting on your input.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata and a README skim. No catalogued STACK pick resolves from this row's
"Overlaps with" cell (agent-of-empires, vibe-kanban, Nimbalyst are catalogued leads/SKIPs,
not STACK picks), so this is not a P2 redundancy call — see Triage note.

## Catalog entry

| [claude-command-center](https://github.com/amirfish1/claude-command-center) | tool | Local dashboard (FSL-1.1-MIT, converts to MIT after 2 years) tracking sessions across 8 coding-agent CLIs and flagging which one needs your input | Running several coding-agent CLIs in parallel gives no single view of which session is stalled waiting on you | agent-of-empires, vibe-kanban, Nimbalyst |  |

## Triage note

Left at `discovery-log`: a multi-CLI session dashboard with real (if early) traction
(182 stars, active development) and no STACK incumbent to call it redundant against.
Its license is source-available rather than purely permissive (FSL-1.1-MIT), which a
hands-on eval should weigh if it is ever exercised. Deserves a real look rather than a
mechanical SKIP; left for the P0/eval-runner lane.

_Triaged 2026-10-11 by the P3 backlog band._
