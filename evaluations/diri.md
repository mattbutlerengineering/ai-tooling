# Evaluation: diri

**Repo:** [cristicretu/diri](https://github.com/cristicretu/diri)
**Stars:** 178 | **License:** Apache-2.0
**Last verified:** 2026-08-05
**Last triaged:** 2026-08-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling (native macOS app)

---

## What it does

A native macOS orchestrator (Rust) that runs Claude Code, Codex, Cursor, Gemini, and shells
in parallel across git worktrees and remote hosts.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell (orca, agent-of-empires, Nimbalyst). That is
sufficient to place the lead and note none of its named overlaps is a native macOS app with
this exact feature set, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: orca is cross-platform (WebGL terminals, mobile companion),
agent-of-empires is tmux+web/PWA, Nimbalyst is a visual workspace formerly Crystal. diri's
pitch — a lightweight, native (not Electron) macOS app for the same worktree-parallel-agent
job — is a real platform differentiator (178 stars in one day) worth a hands-on eval rather
than a redundancy SKIP.

_Triaged 2026-08-05 by the daily discovery routine (today's new lead)._
