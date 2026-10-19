# Evaluation: orchestra

**Repo:** [theorchestradev/orchestra](https://github.com/theorchestradev/orchestra)
**Stars:** 18 | **Last updated:** 2026-10-19 (pushed) | **License:** MIT
**Last verified:** 2026-10-19
**Last triaged:** 2026-10-19  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A desktop app for running coding agents (Claude Code, Codex, OpenCode, Pi, Mistral Vibe,
Antigravity CLI, Grok Build, or a plain shell) side by side in project-based terminal
sessions, each optionally in its own git worktree/branch. Sessions can send requests to each
other and share a project Scratchpad through the `orchestra` CLI. Also browses GitHub issues
and PRs and can start a session from one.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the README,
the CATALOG one-liner, and GitHub repo metadata (stars, license, topics). No hands-on run was
performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

New lead, cataloged today. P3 backlog — zero overlap pressure (none of `diri`, `cross-harness`,
`orca` are STACK picks today), so not a P2 challenger despite the functional overlap with
those worktree-based parallel-agent desktop orchestrators. Left at `discovery-log`; stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [orchestra](https://github.com/theorchestradev/orchestra) | tool | Desktop app (MIT) running coding agents side by side in project-based terminal sessions, each in its own git worktree, with cross-session messaging and a shared scratchpad | Running several coding agents in parallel across worktrees means separate terminals with no shared scratchpad or way for sessions to message each other | diri, cross-harness, orca |  |
