# Evaluation: arguseye

**Repo:** [DarkWorldCoder/arguseye](https://github.com/DarkWorldCoder/arguseye)
**Stars:** 7 | **Last updated:** 2026-11-03 (pushed) | **License:** MIT
**Last verified:** 2026-11-04
**Last triaged:** 2026-11-04  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Previews React, browser-renderable Next.js, and Vue components directly from source,
without starting the dev server — giving coding agents (and VS Code) rendered "UI edit
evidence" to check a change against instead of eyeballing code or waiting on a running
app.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. How reliably it renders components with real data
dependencies, routing, or context providers (vs. a trivial presentational component) is
untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. Cites no STACK pick in
`Overlaps with` (passmark, claude-skill-playwright-browser, pixelpact are catalogued
leads, not STACK picks). Not examined further in this pass.

_Triaged 2026-11-04 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [arguseye](https://github.com/DarkWorldCoder/arguseye) | tool | Previews React, Next.js, and Vue components from source (MIT) — UI edit evidence for coding agents and VS Code, without starting the dev server | Checking a UI change means starting the dev server just to look; want rendered evidence straight from source instead | passmark, claude-skill-playwright-browser, pixelpact |
