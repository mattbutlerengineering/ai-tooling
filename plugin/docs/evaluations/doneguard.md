# Evaluation: doneguard

**Repo:** [abranchesia/doneguard](https://github.com/abranchesia/doneguard)
**Stars:** 7 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Review / Verify — enforces completion during Implement
**Layer:** Tooling

---

## What it does

A Stop hook for Claude Code, Cursor, Codex, Gemini CLI, and Copilot that mechanically
blocks an agent from declaring a task "done" until its own checks (tests, lint, build)
actually pass — instead of relying on the agent to self-report honestly.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Which check commands it recognizes per project,
and how it handles a project with no obvious check command, is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (tdd-guard, ratchet, cc-safety-net are catalogued leads/SKIPs, not
STACK picks). Not examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [doneguard](https://github.com/abranchesia/doneguard) | tool | Stop hook (MIT) for Claude Code, Cursor, Codex, Gemini CLI, and Copilot blocking an agent from declaring a task "done" until its own checks actually pass | Agents claim a task is finished before tests/lint/build actually pass, with nothing mechanically blocking the false "done" | tdd-guard, ratchet, cc-safety-net |
