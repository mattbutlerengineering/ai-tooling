# Evaluation: sno-station

**Repo:** [sno-ai/sno-station](https://github.com/sno-ai/sno-station)
**Stars:** 80 | **Last updated:** 2026-09-22 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Local squad coordination (TypeScript, Apache-2.0) for Claude Code and Codex running on one machine —
shared encrypted memory, agent-to-agent messaging ("Reach"), squad skills for handoff and cross-vendor
review, and a nightly loop that proposes rewrites to the agents' own skills for human approval. No
daemon, no cloud required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of the memory/messaging/self-rewrite features. That is sufficient to catalog
it and place it relative to existing peers, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P2 challenger by citation — `Overlaps with` names `claude-squad`, a STACK pick (ADOPT-eligible
terminal-agent multiplexer). Not a clean redundancy, though: `claude-squad` manages *sessions*
(workspaces/tabs/panes across terminal agents), while sno-station adds a different layer — shared
encrypted memory, direct agent-to-agent messaging, and a self-rewriting skill loop — none of which
`claude-squad` does. Left at `discovery-log` rather than SKIPped; the overlap is real but not
dominating.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [sno-station](https://github.com/sno-ai/sno-station) | tool | Local squad coordination (Apache-2.0) for Claude Code and Codex — shared encrypted memory, agent-to-agent messaging, handoff skills, and a nightly self-rewrite loop, no daemon or cloud | Claude Code and Codex on one machine share no memory and can't message each other; want them to work as one squad, fully local | claude-squad, agmsg, herdr |  |
