# Evaluation: claude-skill-playwright-browser

**Repo:** [AndyShiu/claude-skill-playwright-browser](https://github.com/AndyShiu/claude-skill-playwright-browser)
**Stars:** 12 | **Last updated:** 2026-09-26 (pushed) | **License:** MIT
**Last verified:** 2026-09-26
**Last triaged:** 2026-09-26  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Claude Code skill (MIT) that keeps a background Playwright browser available in any project
for desktop/tablet/mobile screenshots, frontend health checks, visual diffs, scripted UI flows,
and logged-in pages — without wiring Playwright by hand each time.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this skill. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (passmark, agentic-playwright, dev3000). That is sufficient
to note the overlap with existing Playwright-based tools, not to judge whether the always-on
background-browser mechanism is materially better or redundant — it would not support an ADOPT,
and this eval offers none.

## Triage note

Left at `discovery-log` rather than SKIPped as redundant: `passmark` and `agentic-playwright`
address browser regression testing and test scaffolding respectively, neither is a STACK pick,
and neither ships as a lightweight Claude Code skill that keeps a persistent background browser
session available across arbitrary tasks (screenshots, health checks, visual diffs) rather than
a dedicated test-authoring tool. Worth a first-time hands-on eval before any redundancy call.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-skill-playwright-browser](https://github.com/AndyShiu/claude-skill-playwright-browser) | skill | Claude Code skill (MIT) running a background Playwright browser for screenshots, frontend health checks, and visual diffs | Claude Code has no persistent browser for screenshots, health checks, visual diffs, or scripted UI flows without wiring Playwright by hand each project | passmark, agentic-playwright, dev3000 |
