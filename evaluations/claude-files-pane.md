# Evaluation: claude-files-pane

**Repo:** [Marius-Adam/claude-files-pane](https://github.com/Marius-Adam/claude-files-pane)
**Stars:** 31 | **Last updated:** 2026-11-03 (pushed) | **License:** NOASSERTION (⚠️ GitHub could not parse a license grant from the repo)
**Last verified:** 2026-11-03
**Last triaged:** 2026-11-03  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A file explorer for Claude Code: a VS Code-style file tree shown live beside the chat,
updating in real time to show which files the running session is reading, editing, and
committing.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner and repo metadata. The license is `NOASSERTION` — GitHub detected no
parseable LICENSE grant — which is a fact about the repo, not a verdict; whether a real
license exists elsewhere in the repo (README, package.json) was not checked here.

## Triage note

Left at `discovery-log` (P3 backlog) — newly catalogued today, no STACK-pick overlap.
Not examined further in this pass.

_Triaged 2026-11-03 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-files-pane](https://github.com/Marius-Adam/claude-files-pane) | tool | VS Code-style live file tree (⚠️ license NOASSERTION) showing what Claude Code reads, edits, and commits | A bare terminal gives no live, at-a-glance view of which files a running Claude Code session is touching | claude-devtools, claude-super-sidebar, peek |
