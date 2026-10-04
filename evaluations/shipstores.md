# Evaluation: shipstores

**Repo:** [FidelisMM/shipstores](https://github.com/FidelisMM/shipstores)
**Stars:** 14 | **Last updated:** 2026-10-03 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Ship
**Layer:** Tooling

---

## What it does

An MCP server (★14, created 2026-10-01) that lets an AI agent ship iOS and Android
apps end to end — App Store Connect, Google Play Console, and Expo EAS — instead of
clicking through each console by hand.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Flagged in yesterday's scan overflow as "plausibly in-scope (Ship stage) but borderline
general shipping tooling" and left out of the 2026-10-03 pass; re-examined today and
added. `CATALOG.md` has no existing row for app-store/release automation specifically —
`golive-skill` covers taking an app live on your own hosting/DB/domain, a different
(earlier) step than app-store publication. No archived flag, no disqualifying license
(MIT), no `Ships inside` container, and its overlap cell names no STACK pick, so this
does not band as a P2 challenger. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shipstores](https://github.com/FidelisMM/shipstores) | MCP server | Ships iOS/Android apps from an AI agent (MIT) — App Store Connect, Google Play Console, and Expo EAS over one MCP server | Publishing to app stores is manual console-clicking agents can't do; want release/metadata/build steps exposed as MCP tools | golive-skill, oh-my-android, Infracost |
