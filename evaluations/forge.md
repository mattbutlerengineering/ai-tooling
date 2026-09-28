# Evaluation: forge

**Repo:** [brightstack/forge](https://github.com/brightstack/forge)
**Stars:** 10 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-28
**Last triaged:** 2026-09-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A Spec→Plan→Build→Acceptance→Ship delivery process for coding agents, aimed at Claude Code, Codex, and Cursor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `GSD` (STACK ADOPT, MEASURED) — GSD already covers this exact job (a structured, phase-gated Discuss→Plan→Execute→Verify→Ship loop) with restricted-tool subagents and durable state, proven in a real hands-on eval. forge is a 10-star, 12-day-old repo doing the same job with no stated differentiator from GSD's approach; a second unexercised tool for this slot earns nothing over the incumbent.

_Triaged 2026-09-28 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [forge](https://github.com/brightstack/forge) | tool | Spec→Plan→Build→Acceptance→Ship delivery process (MIT) for coding agents across Claude/Codex/Cursor | Agent-driven delivery has no trusted, structured process from spec through acceptance to ship | GSD, factory (addyosmani), claude-sdlc-skills |
