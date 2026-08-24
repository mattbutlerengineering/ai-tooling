# Evaluation: dsh-ios

**Repo:** [ZSeven-W/dsh-ios](https://github.com/ZSeven-W/dsh-ios)
**Stars:** 238 | **Last updated:** 2026-08-23 (pushed) | **License:** MIT
**Last verified:** 2026-08-24
**Last triaged:** 2026-08-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A DeepSeek Harness (DSH) plugin putting a live iOS Simulator — and a USB-connected
iPhone — inside the agent conversation: 22 tools for booting, building, and driving the
UI by accessibility identity, OCR text, or list rows, plus a streaming sidebar panel.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell.

## Triage note

Left at `discovery-log`. Its closest overlap, `deepseek-harness`, is itself a
`discovery-log` lead (not yet adopted), so this doesn't clear the P2 challenger bar — it
extends a harness the catalog hasn't dispositioned yet, it doesn't compete with one
already in STACK. It has no `Ships inside` declared (it is an independently installable
DSH plugin, not a vendored component of a catalogued pack), is not archived, and is
permissively licensed. First-party iOS Simulator/device automation for a coding-agent
harness is differentiated enough (mobile dev workflow, distinct from the Android-focused
`debroid`) to deserve a real look.

_Triaged 2026-08-24 by the P3 backlog band (daily discovery)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [dsh-ios](https://github.com/ZSeven-W/dsh-ios) | plugin | DeepSeek Harness plugin (MIT) putting a live iOS Simulator — and a USB-connected iPhone — inside the conversation, 22 tools for boot/build/UI-drive by accessibility ID or OCR | Mobile-app dev agents can't see or drive a simulator/device; want first-party iOS automation wired into the harness session | deepseek-harness, xcode-skills, debroid |
