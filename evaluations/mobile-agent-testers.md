# Evaluation: mobile-agent-testers

**Repo:** [pierridotite/mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers)
**Stars:** 45 | **Last updated:** 2026-11-19 (pushed) | **License:** MIT
**Last verified:** 2026-11-19
**Last triaged:** 2026-11-19  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Runs 20 Claude Code agents as testers across 20 different iOS Simulators and Android
emulators in parallel via GitHub Actions, for no cost beyond Actions minutes.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. That is sufficient to confirm the lead has no
overlap with a STACK pick, not to judge the tool's own behavior. It would not support
an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. The named overlaps (`simfleet`, `dsh-ios`, `plain`) build or
preview mobile apps on simulators, or run natural-language browser E2E tests; none
run parallel, agent-driven mobile UI testing across many simulators/emulators via CI.
Differentiated enough to deserve a real eval rather than a mechanical SKIP.

_Triaged 2026-11-19 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [mobile-agent-testers](https://github.com/pierridotite/mobile-agent-testers) | tool | Runs coding-agent-driven tests (MIT) across 20 iOS Simulators and Android emulators in parallel via GitHub Actions, for $0 | Mobile UI regressions need real-device-class coverage across many simulators/emulators, which means paid device farms or slow serial runs | simfleet, dsh-ios, plain |
