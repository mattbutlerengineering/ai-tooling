# Evaluation: eca

**Repo:** [editor-code-assistant/eca](https://github.com/editor-code-assistant/eca)
**Stars:** 909 | **Last updated:** 2026-07-08 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

Editor Code Assistant — an editor-agnostic AI pair-programming backend exposing chat, context, and agentic edit/run capabilities over a single protocol, so any editor (Emacs, VS Code, …) gets the same coding-agent loop without a bespoke integration per editor.

## Triage note

Left at `discovery-log`, not SKIPped. eca's differentiated pitch is architectural: it decouples the agent loop from the editor frontend via a shared protocol, which is not quite the same job as any single named catalog incumbent. `aider`/`continue`/`opencode` are themselves either significant standalone tools (aider, left above) or not yet confirmed as adopted STACK picks in their own right, so there is no clearly dominating incumbent to SKIP against without overreaching on a source-only read. Left for a real hands-on evaluation to determine whether the protocol-decoupling angle is a genuine differentiator worth adopting.

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool this pass. This stamp records that the lead was examined during bulk triage; it is not a verdict.

_Triaged 2026-07-27 by the P2 challenger band._
