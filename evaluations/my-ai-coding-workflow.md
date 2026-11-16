# Evaluation: my-ai-coding-workflow

**Repo:** [vaibhav-space/my-ai-coding-workflow](https://github.com/vaibhav-space/my-ai-coding-workflow)
**Stars:** 209 | **Last updated:** 2026-11-14 (pushed) | **License:** ⚠️ no license declared
**Last verified:** 2026-11-16
**Last triaged:** 2026-11-16  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Process

---

## What it does

Curated coding instructions and skills bundled with a 3-stage review pipeline — Planning,
Critical Review, and Diff Audit — distilled from the author's reported 4,500+ hours
working with AI coding agents. Agent-agnostic (not tied to Claude Code specifically).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `GSD` (STACK pick, overlap-cited).
GSD is a context-engineering Discuss→Plan→Execute→Verify→Ship loop with durable state
files; this is a curated skill/instruction bundle plus a 3-stage review gate (Planning,
Critical Review, Diff Audit) — a different shape of methodology, not an obvious subset.
No license is declared, which would route it to a mechanical P4 skip once `repo-metadata.json`
picks it up (this is a vendored `skill`-type artifact) — that is a license finding for a
future pass to make mechanically, not a judgement this pass should pre-empt by hand.

_Triaged 2026-11-16 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [my-ai-coding-workflow](https://github.com/vaibhav-space/my-ai-coding-workflow) | skill | Curated coding instructions and skills (⚠️ no license) with a 3-stage review pipeline — Planning, Critical Review, Diff Audit | Ad hoc AI-assisted coding has no structured planning-then-review gate before a diff ships | requirement-ledger, claude-sdlc-skills, GSD |
