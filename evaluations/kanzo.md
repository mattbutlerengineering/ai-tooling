# Evaluation: kanzo

**Repo:** [emanuele-em/kanzo](https://github.com/emanuele-em/kanzo)
**Stars:** 111 | **Last updated:** 2026-10-28 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A self-hosted kanban board for humans and agents (Rust): one 4 MB binary, starts in 2 ms, zero setup, exposed over MCP so a human and several coding agents can share one task board.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and the CATALOG one-liner/overlaps (CallBoard, vibe-kanban, tasktrooper). That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. It overlaps CallBoard/vibe-kanban/tasktrooper on the shared-task-board job, but none of those is an ADOPT/KEEP STACK pick today, so it doesn't land in P2 challenger. It ships AGPL-3.0, which matters for adoption of the binary's own source but imposes nothing on a team that merely *runs* it (it is a `tool`, not a vendored skill/plugin), so that isn't grounds for a mechanical SKIP either.

## Triage note

P3 backlog. Left at `discovery-log`; worth a hands-on comparison against CallBoard/vibe-kanban given its minimal-footprint pitch (single binary, no setup) once one of those becomes a real incumbent to measure against.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kanzo](https://github.com/emanuele-em/kanzo) | tool | Self-hosted kanban for humans and agents (AGPL-3.0, Rust) — one 4 MB binary, starts in 2 ms, zero setup | Coordinating tasks between a human and several coding agents has no lightweight, self-hosted shared board | CallBoard, vibe-kanban, tasktrooper |
