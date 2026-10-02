# Evaluation: ReMe

**Repo:** [agentscope-ai/ReMe](https://github.com/agentscope-ai/ReMe)
**Stars:** 3,500 | **Last updated:** not independently verified (GitHub API unavailable for this repo in this session) | **License:** Apache-2.0
**Last verified:** 2026-10-02
**Last triaged:** 2026-10-02  <!-- triaged: bulk -->
**Dev loop stage:** Reflect
**Layer:** Infrastructure

---

## What it does

A modular memory management kit that turns conversations and resources into file-based,
long-term memory, continuously indexed, linked, and consolidated so agents can retrieve,
maintain, and evolve shared knowledge across users, tasks, and agents.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This session's GitHub API access is scoped to the
`ai-tooling` repo only, so repo facts came from the public repo page rather than `gh api`.
Source-grounded only: the repo's own README description plus the CATALOG "Overlaps with" cell.
Sufficient to place the lead, not to support any verdict, and none is offered.

## Triage note

Left at `discovery-log`. Cites `claude-mem` (STACK) in "Overlaps with", which bands this P2, but
the two differ in scope: `claude-mem` is a Claude-Code-specific plugin capturing session activity
automatically via hooks, while ReMe is a general, cross-agent memory kit (not tied to one harness)
with an explicit "modular" architecture for indexing/linking/consolidating shared memory across
users and tasks. At 3.5K stars from an established agent-tooling org (agentscope-ai), it is
significant and differentiated enough to deserve a real hands-on look rather than a mechanical
SKIP.

_Triaged 2026-10-02 by the P2 challenger band (daily discovery pass)._
