# Evaluation: coordinator

**Repo:** [petekp/coordinator](https://github.com/petekp/coordinator)
**Stars:** 45 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-17
**Last triaged:** 2026-11-17  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code skill that turns one session into a coordinator running, watching, and
cleaning up a fleet of agent sessions inside Herdr (the terminal agent multiplexer).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG one-liner. That is sufficient to place the lead, not to judge
whether the coordination/cleanup actually works across a real fleet — it would not
support an ADOPT, and this eval offers none.

## Triage note

Not a `Ships inside` case — this is a skill that *drives* Herdr from one session, not a
component vendored inside the `herdrdev/herdr` repo, so it is an independent artifact with
its own install. `herdr` is cataloged but not itself a STACK pick, so there is no
incumbent to call this redundant with; its nearest catalog peers (`herdr-gpui`, `numbrone`)
are themselves un-adopted leads. Left at `discovery-log` per the P3 band's default
disposition.

_Triaged 2026-11-17 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [coordinator](https://github.com/petekp/coordinator) | skill | Claude Code skill (MIT) turning one session into a coordinator that runs, watches, and cleans up a fleet of Herdr agent sessions | Running a fleet of agent sessions in Herdr has no coordinator session to run, watch, and clean them up | herdr, herdr-gpui, numbrone |
