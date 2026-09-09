# Evaluation: CodingPlanQuota

**Repo:** [MeIotCOM/CodingPlanQuota](https://github.com/MeIotCOM/CodingPlanQuota)
**Stars:** 53 | **Last updated:** 2026-09-03 (pushed) | **License:** NOASSERTION (no detected LICENSE file)
**Last verified:** 2026-09-09
**Last triaged:** 2026-09-09  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop (Observability)
**Layer:** Tooling

---

## What it does

A mobile app (Android/iOS/HarmonyOS NEXT) for checking AI coding-plan quotas on the go —
5h/weekly/monthly usage across Zhipu GLM, Kimi, MiniMax, ZenMux, OpenCode Go, Volcengine Ark,
DeepSeek, and custom relays. No backend; keys stay on-device.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`: no structural disposition applies — claude-monitor/brink/
claude-statusline-burnrate are desktop/terminal tools scoped to Claude's own usage limits;
CodingPlanQuota is a mobile app covering a different set of providers (mostly Chinese-market
coding plans) and is complementary rather than redundant. `repo-metadata.json` records
`license_spdx: NOASSERTION` (no LICENSE file) — worth confirming before any positive verdict,
per the license bar.

_Triaged 2026-09-09 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CodingPlanQuota](https://github.com/MeIotCOM/CodingPlanQuota) | tool | Mobile app (⚠️ no license) checking AI coding-plan quotas on the go — Zhipu GLM, Kimi, MiniMax, DeepSeek, and custom relays | Coding-plan quota limits across multiple providers aren't visible without opening each provider's own dashboard | claude-monitor, brink, claude-statusline-burnrate |
