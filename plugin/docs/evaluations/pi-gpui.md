# Evaluation: pi-gpui

**Repo:** [bytesbay/pi-gpui](https://github.com/bytesbay/pi-gpui)
**Stars:** 168 | **Last updated:** 2026-11-15 (pushed) | **License:** MIT
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A native GUI for the `pi` coding agent, built in Rust with GPUI, for macOS (Apple
Silicon) and Linux.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient for a P3
leave-at-discovery-log call, not to judge the tool's actual behavior — it would not
support an ADOPT, and this eval offers none.

## Triage note

A companion GUI for an already-catalogued harness (`pi`), not a competitor to it —
differentiated from `Pi-Remote` (browser-based remote mirroring) by being a native
desktop client. Worth a real look at what the GUI actually adds over the TUI before
disposing; left at `discovery-log`.

_Triaged 2026-11-16 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi-gpui](https://github.com/bytesbay/pi-gpui) | tool | Native GUI (MIT) for the pi coding agent, built in Rust with GPUI, for macOS Apple Silicon and Linux | The pi coding agent is terminal/TUI-only; want a native desktop GUI instead of a text interface | pi, Pi-Remote, oh-my-pi |
