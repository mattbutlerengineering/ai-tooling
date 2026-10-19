# Evaluation: agents-contract

**Repo:** [AntoGA/agents-contract](https://github.com/AntoGA/agents-contract)
**Stars:** 40 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

One `AGENTS.md` rules contract for AI coding agents (Claude Code reads it via a `CLAUDE.md`
that imports `@AGENTS.md`), a zero-dependency Python 3.9+ linter that stops it rotting, and a
SessionStart hook that checks the environment before work begins. No vendor lock-in — plain
Markdown under git.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure. Closest peers
(`claude-md-doctor`, `open-skill-sunset`, `reporails/cli`) are themselves discovery-log leads,
not STACK picks, so not a P2 challenger. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [agents-contract](https://github.com/AntoGA/agents-contract) | tool | One AGENTS.md rules contract (MIT), a zero-dependency linter stopping it from rotting, and a SessionStart hook checking the environment first | Agent instruction files drift stale with no linter catching conflicting or dead rules and no pre-session check of the environment | claude-md-doctor, open-skill-sunset, reporails/cli |  |
