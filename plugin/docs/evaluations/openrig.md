# Evaluation: openrig

**Repo:** [mvschwarz/openrig](https://github.com/mvschwarz/openrig)
**Stars:** 4,000 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Builds a persistent network of AI coding agents from Claude Code, Codex, and Pi — teams are
defined in YAML, booted with one command, and run as native sessions over tmux with
inter-agent messaging (`rig_send`, `rig_chatroom_send`) and a topology MCP server agents can use
to manage their own structure.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Sufficient to place the lead, not to support any verdict, and none is offered.

## Triage note

Left at `discovery-log`. No STACK pick is cited in its "Overlaps with" cell (orca,
agent-of-empires, and AgentsMesh are all catalogued but none is a STACK pick), so this bands P3
rather than P2 — nothing structural forces a disposition. At 4K stars it is a significant,
differentiated tool (durable, messaging-capable agent *teams* rather than a session manager) that
deserves a real hands-on eval rather than disposal.

_Triaged 2026-10-02 by the P3 backlog band (daily discovery pass)._
