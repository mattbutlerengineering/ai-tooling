# Evaluation: castra

**Repo:** [beyondworks/castra](https://github.com/beyondworks/castra)
**Stars:** 18 | **Last updated:** 2026-09-14 (pushed) | **License:** MIT
**Last verified:** 2026-09-15
**Last triaged:** 2026-09-15  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An execution posture harness for Claude Code, framed around the idea that a coding agent stops one step early (or barrels past a risky action) — Castra inserts the mandatory checkpoint in between.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. None of its overlap citations (`dot-reflex`, `humanlayer`, `Aegis`) are STACK picks, so it doesn't clear the P2 challenger bar. It's 18★ and days old — too early to call it dominated by the more established execution-guardrail tools it overlaps, and its specific framing (a mandatory posture checkpoint, not a general recovery controller or human-approval SDK) looks differentiated enough to leave for a real look.

_Triaged 2026-09-15 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [castra](https://github.com/beyondworks/castra) | harness | Execution posture harness (MIT) for Claude Code — inserts a mandatory checkpoint before the agent's next step | Coding agents stop one step early or barrel past a risky action with no posture check in between | dot-reflex, humanlayer, Aegis |
