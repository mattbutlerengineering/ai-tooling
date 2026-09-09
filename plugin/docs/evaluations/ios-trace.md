# Evaluation: iOS-Trace

**Repo:** [kmgcc/iOS-Trace](https://github.com/kmgcc/iOS-Trace)
**Stars:** 5 | **Last updated:** 2026-09-08 (pushed) | **License:** MIT
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Process/Tooling (a skill wrapping headless xctrace profiling)

---

## What it does

Agent skill for closed-loop iOS/iPadOS performance optimization: headless `xctrace`
profiling on physical devices and simulators, targeted code fixes based on the profile, and
differential A/B re-testing to confirm the fix actually helped. Works with Claude Code,
Codex, Cursor, Antigravity, and other agent hosts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a SKIP that turns on
redundancy with a catalogued incumbent, not on the tool's behaviour — a question the overlap
answers directly. It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies — it doesn't overlap a STACK
pick (existing catalog performance-testing entries like passmark/midscene target web UI, not
native iOS `xctrace` profiling), isn't vendored under a disqualifying license, and declares no
`Ships inside` container. Differential A/B re-testing tied to on-device profiling is a real,
narrow niche (iOS perf regression closed-loop) worth a hands-on look if iOS work becomes
relevant, but not urgent at 5★ and days old.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [iOS-Trace](https://github.com/kmgcc/iOS-Trace) | skill | Agent skill (MIT) for closed-loop iOS/iPadOS performance optimization — headless xctrace profiling, targeted fixes, differential A/B re-testing | Agents can't verify a performance fix actually helped without manual Instruments profiling and re-testing on device | passmark, midscene, vet |
