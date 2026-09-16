# Evaluation: Argus

**Repo:** [NathanWu8343/Argus](https://github.com/NathanWu8343/Argus)
**Stars:** 5 | **Last updated:** 2026-09-15 (pushed) | **License:** none specified
**Last verified:** 2026-09-16
**Last triaged:** 2026-09-16  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A confirm-first protection gate for Claude Code and OpenAI Codex — intercepts tool calls
and forces a restate-and-confirm step before the agent acts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for the disposition
below, not for an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. P3 backlog — nothing structural flags it for a mechanical
disposition; stamping records that it was examined. No declared license, which the
catalog's SKIP bar does not reach on its own for a `tool` Type without a copyleft or
missing-grant finding to state.

_Triaged 2026-09-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Argus](https://github.com/NathanWu8343/Argus) | tool | Confirm-first protection gate (⚠️ no license) for Claude Code and OpenAI Codex — intercepts tool calls and forces a restate-and-confirm before acting | Agents misread intent and edit code wrongly before a human can catch it; want tool calls blocked pending explicit confirmation | toolpermit, ctrlrun, cc-safety-net |
