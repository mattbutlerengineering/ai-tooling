# Evaluation: ilse

**Repo:** [idantas/ilse](https://github.com/idantas/ilse)
**Stars:** 3 | **Last updated:** 2026-10-03 (pushed) | **License:** MIT
**Last verified:** 2026-10-04
**Last triaged:** 2026-10-04  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A visual design tool (TypeScript, ★3, created 2026-10-01, beta) that lets you point at
a UI element that's wrong in the browser and instructs a coding agent (Claude Code,
Codex, Cursor, Gemini CLI) to fix it in the code.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead
against its closest catalog peers, not to support any verdict, and none is offered here.

## Triage note

Overlaps `airship` (discovery-log — Figma-like visual UI editor), `Remarc`
(discovery-log — point-at-text/screenshots/web-elements macOS feedback layer), and
`why-ui` (discovery-log — Chrome extension surfacing runtime browser evidence); none is
a STACK pick, so this does not band as a P2 challenger despite the crowded "point at
the UI, agent acts" niche. Differentiator from Remarc/why-ui: ilse is specifically
about pointing at a *visual defect* and having the agent *fix* it, not just surfacing
evidence or building new UI. No archived flag, no disqualifying license, no
`Ships inside` container. Left at `discovery-log`.

_Triaged 2026-10-04 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ilse](https://github.com/idantas/ilse) | tool | Visual design tool (MIT) — point at what's wrong with a UI in the browser, the coding agent fixes it in the code | Describing a visual UI bug in words is imprecise; want to point at the element and have the agent fix it directly | airship, Remarc, why-ui |
