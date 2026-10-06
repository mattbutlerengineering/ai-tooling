# Evaluation: ThinkTerm

**Repo:** [RoversX/ThinkTerm](https://github.com/RoversX/ThinkTerm)
**Stars:** 6 | **Last updated:** 2026-10-05 (pushed) | **License:** GPL-3.0
**Last verified:** 2026-10-06
**Last triaged:** 2026-10-06  <!-- triaged: bulk -->
**Dev loop stage:** Agent Orchestration
**Layer:** Tooling

---

## What it does

A GPU-rendered Rust terminal with a built-in multiplexer — sessions outlive the window and can be
picked up from desktop, browser, or TUI; built for running shells and many AI agents across
machines, with no Electron/GPUI/webview, per the repo description.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the GitHub
repository description, topics, and metadata. That is sufficient to place the lead, not to judge
its multiplexer/session-persistence claims hands-on. GPL-3.0 is noted but does not block cataloguing
a tool that is run rather than vendored — copyleft on a CLI you merely invoke imposes nothing on the
consuming repo.

## Triage note

Left at `discovery-log`. No `Overlaps with` cell names a STACK pick, so this is plain P3 backlog.
It is a brand-new (1-day-old, 6-star) terminal in a crowded field (`herdr`, `VelaTerm`, `rmux`);
worth a look only once it has more than a day of track record.

_Triaged 2026-10-06 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ThinkTerm](https://github.com/RoversX/ThinkTerm) | tool | GPU-rendered Rust terminal (⚠️ GPL-3.0) with a built-in multiplexer — sessions outlive the window, pick them up from desktop, browser, or TUI; runs shells and many AI agents across machines | Generic terminals aren't built to keep agent sessions alive across devices; want a multiplexer-native terminal with no Electron/GPUI/webview overhead | herdr, VelaTerm, rmux |
