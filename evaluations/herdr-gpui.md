# Evaluation: herdr-gpui

**Repo:** [penso/herdr-gpui](https://github.com/penso/herdr-gpui)
**Stars:** 109 | **Last updated:** 2026-09-23 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-23
**Last triaged:** 2026-09-23  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A native macOS client (Rust + GPUI, Apache-2.0) for the Herdr daemon — a GUI view of terminal
sessions, workspaces, git worktrees, and agent activity, talking to the same local Herdr daemon the
`herdr` CLI drives.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and
the README's description of what it renders from the Herdr daemon. That is sufficient to catalog it
as a companion artifact, not to support an ADOPT.

## Verdict

**discovery-log — tentative read**

## Triage note

P3 backlog. Not redundant with `herdr` itself — it's a native GUI client for the same daemon, not a
competing multiplexer, so a SKIP "redundant with herdr" would be the wrong call (companion, not
competitor). `herdr` is catalogued but not a STACK pick, so this isn't P2 either. Left at
`discovery-log` for a maintainer who already runs `herdr` to evaluate hands-on.

_Triaged 2026-09-23 by the P3 backlog band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [herdr-gpui](https://github.com/penso/herdr-gpui) | tool | Native macOS GPUI client (Rust, Apache-2.0) for the Herdr daemon — terminal sessions, workspaces, git worktrees, and agent activity in one app | Herdr's multiplexer is terminal-only; want a native GUI view of running agents, worktrees, and workspaces | herdr, cc-switch, VelaTerm |  |
