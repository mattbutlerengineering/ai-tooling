# Evaluation: omux

**Repo:** [onurozcan/omux](https://github.com/onurozcan/omux)
**Stars:** 112 | **Last updated:** 2026-11-01 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A native macOS terminal (SwiftUI) running many Claude Code and Codex sessions side by
side, with per-project worktrees, live agent status, Allow/Deny from the sidebar,
resumable conversations, PR status, and file previews.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient for
a P2 band disposition that turns on redundancy with the named STACK incumbent, not on
the tool's own behavior — a question the overlap answers directly.

## Verdict

**SKIP** — redundant with `claude-squad`. claude-squad (STACK, CONDITIONAL/RUN) already
covers the job — managing multiple AI terminal agents (Claude Code, Codex, OpenCode,
Amp) in parallel, with visibility into each session. omux covers the same core job
(parallel Claude Code/Codex session management) for a narrower set of harnesses
(two vs. claude-squad's four) on one platform (macOS-only vs. claude-squad's
cross-platform TUI). The added session chrome (native worktree view, PR status, file
previews) is UI polish on the same job the incumbent already does, not a new dev-loop
capability — the pattern P2's "redundant with an incumbent already covering the same
job" disposition is for.

_Triaged 2026-11-02 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [omux](https://github.com/onurozcan/omux) | tool | Native macOS terminal (MIT, SwiftUI) running many Claude Code and Codex sessions side by side with worktrees and live status | Running several coding-agent sessions in separate terminal tabs gives no shared view of worktrees, Allow/Deny prompts, resumable conversations, or PR status | claude-squad, d-code, agent-of-empires |
