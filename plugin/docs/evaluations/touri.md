# Evaluation: touri

**Repo:** [touri-ai/touri](https://github.com/touri-ai/touri)
**Stars:** 67 | **Last updated:** 2026-10-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local-first macOS/Linux desktop app (Tauri v2 shell, Bun sidecar, React UI) for running
persistent AI "bot" teammates on top of the Codex, Claude Code, or OpenCode CLIs. Bots keep
their own instructions, memory, skills, and branching chat history; routines are cron-scheduled
bot runs with overlap/catch-up control; projects connect a local repo and run supervised
processes with in-app preview; an agent browser supports human take-over; optional computer use
ships a visible indicator and kill switch; bot machines run in Apple `container` (macOS) or
rootless Podman/Docker (Linux). Everything stays on-device unless a remote is explicitly
configured.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow
clone's README and LICENSE. That confirms the license and the feature claims as documented, not
whether the sandboxing (containers, approval modes, kill switch) holds up hands-on.

## Verdict

**discovery-log — tentative read** — newly catalogued this pass; not previously examined.

## Triage note

New lead, added today. Not a P2 challenger: the catalog's nearest peers (`acryl`, `d-code`,
`agentaps`) are themselves `discovery-log` leads, not STACK picks, so there's no incumbent to
be redundant with — and touri's persistent-bot + cron-routine + multi-runtime (Codex/Claude
Code/OpenCode) combination is differentiated enough from any one of them to deserve its own
first-time look rather than a mechanical SKIP. Left at `discovery-log`.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [touri](https://github.com/touri-ai/touri) | tool | Local-first macOS/Linux desktop app (Apache-2.0, Tauri) running persistent AI "bot" teammates on Codex, Claude Code, or OpenCode with cron routines and approval modes | Coding-agent sessions are terminal-only and ephemeral; want persistent, scheduled bot teammates with their own memory and an approval-gated desktop shell | acryl, d-code, agentaps |  |
