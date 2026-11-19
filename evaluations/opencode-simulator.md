# Evaluation: opencode-simulator

**Repo:** [rin-yato/opencode-simulator](https://github.com/rin-yato/opencode-simulator)
**Stars:** 41 | **Last updated:** 2026-11-11 (pushed) | **License:** MIT
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An OpenCode Desktop plugin that embeds a live iOS Simulator inside the app and gives
agents tools to drive it.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. That is sufficient to confirm the lead has no
overlap with a STACK pick, not to judge the tool's own behavior. It would not support
an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. `dsh-ios` and `simfleet` wire a live simulator into DeepSeek
Harness and React Native/macOS workflows respectively; this is the OpenCode-specific
equivalent, wiring the same idea into a different harness's desktop app. Harness-scoped
rather than a thin clone, and no STACK pick covers OpenCode's own simulator story.

_Triaged 2026-11-19 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opencode-simulator](https://github.com/rin-yato/opencode-simulator) | plugin | OpenCode Desktop plugin (MIT) embedding a live iOS Simulator and giving agents tools to drive it | opencode has no built-in iOS Simulator view or driving tools for mobile-app agent sessions | dsh-ios, simfleet, sim-agentation |
