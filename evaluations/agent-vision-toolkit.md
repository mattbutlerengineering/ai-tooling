# Evaluation: agent-vision-toolkit

**Repo:** [Anionex/agent-vision-toolkit](https://github.com/Anionex/agent-vision-toolkit)
**Stars:** 288 | **License:** MIT
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling (CLI + skill)

---

## What it does

A vision toolkit + skill that gives text-only LLM agents image Q&A, OCR, screenshot
analysis, and visual grounding (including image-to-SVG), with drop-in integration for
Codex, Claude Code, OpenCode, and Pi.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (UI-TARS-desktop, MinerU, midscene). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: UI-TARS-desktop and midscene are vision-driven *action* agents
(controlling a GUI, running tests); MinerU is document/PDF-to-markdown extraction. None is a
general-purpose vision *toolkit a text-only agent calls as a skill* across four harnesses
(Codex/Claude Code/OpenCode/Pi). Fast-growing (288 stars in ~4 days) and differentiated
enough to deserve a real hands-on eval rather than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
