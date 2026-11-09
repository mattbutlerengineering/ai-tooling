# Evaluation: harness-relay

**Repo:** [Agentic-System-Lab/harness-relay](https://github.com/Agentic-System-Lab/harness-relay)
**Stars:** 8 | **Last updated:** 2026-11-09 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-09
**Last triaged:** 2026-11-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local group chat for the real Claude Code, Codex, and Grok CLIs — you give each a role,
choose how they take turns, and they work on your code (or any question) and answer each
other in a shared channel.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and its "Overlaps with" cell (`tucano`, `orchestra (TheAlejo160)`,
`imbo`). That is sufficient to check for a named STACK redundancy; it is not sufficient to
support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read** — brand new (created 2026-11-07) at 8 stars. None of
its cited peers is a STACK pick, so no mechanical SKIP applies. The multi-CLI (not
multi-session-of-one-CLI) turn-taking angle distinguishes it from `tucano`/`orchestra`
enough to be worth a real look rather than a redundancy dismissal, despite the low star
count.

## Triage note

Left at `discovery-log` for the P0/eval-runner lane.

_Triaged 2026-11-09 by the daily discovery-and-triage routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [harness-relay](https://github.com/Agentic-System-Lab/harness-relay) | tool | Local group chat (Apache-2.0) for the real Claude Code, Codex, and Grok CLIs — assign roles, set turn order, they work and answer each other | Running several coding-agent CLIs on one task gives them no shared channel to take turns and talk through the work together | tucano, orchestra (TheAlejo160), imbo |
