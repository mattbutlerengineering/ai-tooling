# Evaluation: ai-design-check

**Repo:** [enmerasoftware/ai-design-check](https://github.com/enmerasoftware/ai-design-check)
**Stars:** 207 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A set of design rules plus a zero-dependency checker that audits interfaces an AI
coding agent built on the web, in SwiftUI, and in Jetpack Compose, flagging departures
from the stated rules. Documentation and the checker itself are available in English
and Turkish.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. Whether the checker reliably flags real design
drift versus false-positives across three different UI frameworks is untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ai-design-check](https://github.com/enmerasoftware/ai-design-check) | tool | Design rules + zero-dependency checker (MIT) for AI-built web, SwiftUI, and Jetpack Compose interfaces | AI coding agents ship interfaces with no automated design-consistency check across web and native UI frameworks | bricks, design.md, airship |
