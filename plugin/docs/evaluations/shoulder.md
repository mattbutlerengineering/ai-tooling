# Evaluation: shoulder

**Repo:** [bjarneo/shoulder](https://github.com/bjarneo/shoulder)
**Stars:** 73 | **Last updated:** 2026-10-31 (pushed) | **License:** MIT
**Last verified:** 2026-11-02
**Last triaged:** 2026-11-02  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A TUI that shows, live, what Claude Code, Codex, Gemini CLI, and opencode are doing in
your project — a cross-harness activity view rather than a single-tool monitor.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
CATALOG one-liner, repo metadata, and the "Overlaps with" cell. That is sufficient for
a P2 band disposition that turns on redundancy with the named STACK incumbent, not on
the tool's own behavior — a question the overlap answers directly. It would not
support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`, not SKIPped. `triage.py` challenges it against `abtop`
(STACK, CONDITIONAL/MEASURED), but abtop's real-time TUI is scoped to tokens,
context %, rate limits, and ports for AI-agent sessions — a quota/resource view.
shoulder's pitch is a cross-harness **activity** feed (four different coding-agent
CLIs at once: Claude Code, Codex, Gemini CLI, opencode) rather than per-session
resource stats. That is a genuine scope difference, not a thinner clone, so a bulk
SKIP would overreach what this source-only read can defensibly conclude.

_Triaged 2026-11-02 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [shoulder](https://github.com/bjarneo/shoulder) | tool | TUI (MIT) showing live what Claude Code, Codex, Gemini CLI, and opencode are doing in your project | Running a coding agent in the background gives no at-a-glance live view of what it's doing without switching to its own terminal | claude-super-sidebar, agent-orchestration-standard, abtop |
