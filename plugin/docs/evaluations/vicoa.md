# Evaluation: vicoa

**Repo:** [vicoa-ai/vicoa](https://github.com/vicoa-ai/vicoa)
**Stars:** 32 | **Last updated:** 2026-09-03 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-09-03
**Last triaged:** 2026-09-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A self-hostable ADE (agent development environment) for running a team of coding agents (Claude Code, Codex, OpenCode) from any device — desktop, mobile, or VPS. Open-source, self-hostable.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`useagent`, `gastown`, `claude-squad`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. The P2 band flags it as challenging `claude-squad` (STACK pick), but the overlap is not a defensible redundancy SKIP: `claude-squad` manages parallel terminal sessions on one machine, while vicoa's stated differentiator is cross-device access (desktop/mobile/VPS) via a hosted ADE — a meaningfully different form factor and use case, not the same job twice. Also carries AGPL-3.0, which would bar an ADOPT/KEEP regardless (it's a "platform" Type, run rather than vendored, so the license doesn't trigger a mechanical P4 skip — but it does mean any future positive verdict needs to reckon with the license). Worth a real look rather than a mechanical dismissal.

_Triaged 2026-09-03 by the P2 challenger band ([#579](https://github.com/mattbutlerengineering/ai-tooling/issues/579))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vicoa](https://github.com/vicoa-ai/vicoa) | platform | Self-hostable ADE (⚠️ AGPL-3.0) for running a team of coding agents (Claude Code, Codex, OpenCode) from desktop, mobile, or VPS | Monitoring/steering multiple coding agents across devices needs a dedicated app, not ad hoc terminal sessions per machine | useagent, gastown, claude-squad |
