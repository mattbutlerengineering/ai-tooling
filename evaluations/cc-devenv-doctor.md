# Evaluation: cc-devenv-doctor

**Repo:** [killernay/cc-devenv-doctor](https://github.com/killernay/cc-devenv-doctor)
**Stars:** 13 | **Last updated:** 2026-08-06 (pushed) | **License:** MIT
**Last verified:** 2026-08-07
**Last triaged:** 2026-08-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

One command that takes a bare Windows or Mac machine to a working Claude Code setup, plus a
plugin that keeps diagnosing the environment afterwards.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (HolyClaude, claude-code-templates). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: HolyClaude solves a related but different problem (a full
containerized workstation via `docker compose up`), and claude-code-templates is a
component installer/marketplace, not a bare-machine bootstrapper with ongoing health checks.
The bootstrap-plus-continuous-diagnosis combination is a real differentiator worth a
hands-on eval rather than a redundancy SKIP.

_Triaged 2026-08-07 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cc-devenv-doctor](https://github.com/killernay/cc-devenv-doctor) | tool | One command (MIT) taking a bare Windows or Mac machine to a working Claude Code setup, plus a plugin that keeps diagnosing it afterwards | Bootstrapping a new machine for Claude Code means manually installing and configuring dependencies with no ongoing health check | HolyClaude, claude-code-templates |
