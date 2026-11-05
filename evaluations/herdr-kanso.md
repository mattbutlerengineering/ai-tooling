# Evaluation: herdr-kanso

**Repo:** [jlopezlira/herdr-kanso](https://github.com/jlopezlira/herdr-kanso)
**Stars:** 8 | **Last updated:** 2026-11-05 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-05
**Last triaged:** 2026-11-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A layout for the Herdr terminal multiplexer that keeps every terminal a fixed width in a
row instead of Herdr's default grid, and binds a PR's incoming feedback to starting an
agent on it, with the editor one key away.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The claimed PR-feedback-to-agent binding is
untested here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today. It is a companion layout
for the already-catalogued `herdr` (not a component shipped inside the same repo — a
separate author, a separate install), the same relationship `herdr-gpui` already has to
`herdr`. Not examined further in this pass.

_Triaged 2026-11-05 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [herdr-kanso](https://github.com/jlopezlira/herdr-kanso) | tool | A Herdr layout (Apache-2.0) keeping terminal widths fixed in a row, where a PR's feedback starts an agent and the editor is one key away | Herdr's default grid layout doesn't fit a row-based workflow of stable-width terminals plus a one-key jump to the editor | herdr, herdr-gpui, VelaTerm |
