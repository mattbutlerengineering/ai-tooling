# Evaluation: claude-rotate

**Repo:** [doxaras/claude-rotate](https://github.com/doxaras/claude-rotate)
**Stars:** 23 | **Last updated:** 2026-09-04 (pushed) | **License:** MIT
**Last verified:** 2026-09-06
**Last triaged:** 2026-09-06  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A multi-account rotating proxy for Claude Code — consume-first quota rotation, burst-aware 429
handling, hold-until-reset behavior, and per-device analytics, aimed at teams juggling multiple
Claude Code accounts to dodge rate limits.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge the
rotation/analytics behavior hands-on.

## Triage note

Left at `discovery-log`. P3 backlog — no structural disposition. It overlaps `CLIProxyAPI` and
`litellm` on multi-account/proxy mechanics but is narrower and more opinionated (consume-first
rotation specifically for Claude Code quota, not a general multi-provider gateway); doesn't cite a
STACK pick in "Overlaps with" so it isn't banded P2. Stamped and left for a real eval to weigh
against the incumbents.

_Triaged 2026-09-06 by the P3 backlog band._
