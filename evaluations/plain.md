# Evaluation: plain

**Repo:** [gabe4coding/plain](https://github.com/gabe4coding/plain)
**Stars:** 0 | **Last updated:** 2026-10-22 (pushed) | **License:** MIT
**Last verified:** 2026-10-23
**Last triaged:** 2026-10-23  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

End-to-end browser tests written in plain English (TypeScript) — Playwright performs the
actions, the Jev model decides whether they passed; ships as a CLI, MCP server, and
Claude Code/Codex plugin. Topics also name Appium/mobile (Android/iOS) support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Pressure 0 — nothing in the catalog cites it yet. Its "Overlaps with" cell names
`webapp-testing`, `playwright-best-practices`, and `ming-qa`, none of which is a STACK
pick, so this does not band as a P2 challenger. No archived flag, no disqualifying
license (MIT), no `Ships inside` container. Zero stars and zero stars/watchers despite
15 open issues (real usage, no attention yet) — genuinely new (created 2026-09-20) with
a differentiator (natural-language test authoring, mobile support via Appium) over the
existing Playwright-adjacent peers. Left at `discovery-log` rather than SKIPped.

_Triaged 2026-10-23 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [plain](https://github.com/gabe4coding/plain) | tool | End-to-end browser tests written in plain English (MIT) — Playwright performs the actions, the Jev model decides; CLI, MCP server, Claude Code/Codex plugin | Writing and maintaining Playwright test scripts by hand is slow; want natural-language E2E tests an agent can run and judge | webapp-testing, playwright-best-practices, ming-qa |
