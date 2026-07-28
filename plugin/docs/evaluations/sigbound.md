# Evaluation: sigbound

**Repo:** [surya-koritala/sigbound](https://github.com/surya-koritala/sigbound)
**Stars:** 52 | **Last updated:** 2026-07-27 | **License:** Apache-2.0
**Last verified:** 2026-07-28
**Last triaged:** 2026-07-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Go CLI that runs multiple AI coding agents in parallel on one git repo and safely auto-merges their work — only changes that build and pass tests land, using optimistic concurrency on top of plain git. Bring-your-own model; no vendor lock-in.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (GitHub API: 52 stars, Apache-2.0, pushed 2026-07-27) plus the CATALOG "Overlaps with" cell against claude-squad/vibe-kanban/agent-orchestrator/weave. Sufficient to catalog and note the gap (automatic build/test-gated merge vs. those tools' session/board management), not to judge merge-safety claims hands-on.

## Triage note

Distinct from claude-squad (session TUI) and agent-orchestrator (planning/CI-fix orchestration) in focusing narrowly on a safe auto-merge gate for parallel agents editing the same repo — a real gap (most orchestration tools assume manual merge review). Worth a future hands-on eval to verify the auto-merge safety claim; left at discovery-log.
