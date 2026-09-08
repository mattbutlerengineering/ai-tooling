# Evaluation: mobilecode

**Repo:** [hsandhu/mobilecode](https://github.com/hsandhu/mobilecode)
**Stars:** 218 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-08
**Last triaged:** 2026-09-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A fork of opencode that builds and live-previews iOS and Android projects directly from the coding-agent session — embedded simulator/emulator previews, automated build orchestration, and agent-driven app launching for React Native development.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Neither overlap citation (`opencode`, marked external, and `dsh-ios`) is a STACK pick, so this doesn't clear the P2 bar — it's genuinely P3 backlog. Mobile-build-and-preview inside a coding-agent session is a narrow but real gap (opencode itself has no native mobile build/preview loop); 218★ in 3 days is a signal worth a real look eventually, but not urgent enough to escalate today.

_Triaged 2026-09-08 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mobilecode](https://github.com/hsandhu/mobilecode) | harness | Fork of opencode (MIT) that builds and live-previews iOS and Android projects from the coding-agent session | Coding agents can edit mobile app code but can't build or preview it on a simulator/device without leaving the harness | opencode (ext.), dsh-ios |
