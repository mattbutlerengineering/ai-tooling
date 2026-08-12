# Evaluation: ai-pulse

**Repo:** [leog/ai-pulse](https://github.com/leog/ai-pulse)
**Stars:** 28 | **Last updated:** 2026-08-12 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

An ambient macOS light strip — a Dock-adjacent pill of LEDs showing whether an AI coding agent is
working, waiting, finished, or broken, at a glance without switching windows.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: repo metadata plus the CATALOG
"Overlaps with" cell. Enough to place it against nearby status-indicator tools, not enough for any
verdict, and none is offered.

## Triage note

Left at `discovery-log`. `ping-island` and `claude-nanny` both solve the same "am I being ignored by
an agent" problem with a different UI surface (notch, menu bar) — `ai-pulse` uses an always-visible
ambient light strip instead. Genuinely a UI-form-factor variant worth comparing on its own, not an
obvious mechanical dispose.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-pulse](https://github.com/leog/ai-pulse) | tool | Ambient macOS light strip (MIT) — a Dock-adjacent pill of LEDs showing whether an AI coding agent is working, waiting, finished, or broken | Checking on multiple agent sessions means switching windows; want an at-a-glance ambient status signal | ping-island, claude-nanny, claude-hud |
