# Evaluation: traxagent-claude-plugin

**Repo:** [ccarter01011/traxagent-claude-plugin](https://github.com/ccarter01011/traxagent-claude-plugin)
**Stars:** 137 | **Last updated:** 2026-11-20 (pushed) | **License:** MIT
**Last verified:** 2026-11-21
**Last triaged:** 2026-11-21  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A read-only MCP server plus Claude Code plugin that reports AI spend across several
tools (Claude, ChatGPT, Claude Code, Cursor, VS Code) and surfaces what to fix,
rather than parsing one CLI's own session logs the way the `ccusage`/`tokentab`
cluster does.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the CATALOG one-liner plus repo metadata. Sufficient to place the lead, not to
confirm whether its cross-tool scope and recommendations are a real differentiator
in practice.

## Triage note

Banded P2 (challenges `ccusage`). Both are cost-visibility tools, but `ccusage`
reads local Claude-Code-and-other-CLI session logs while this one claims coverage
of non-CLI tools (ChatGPT, Cursor, VS Code) plus prescriptive "what to fix"
guidance — a scope `ccusage` doesn't claim. That's enough uncertainty to withhold a
redundancy SKIP; left at discovery-log for a hands-on look at whether the
cross-tool claim holds up.

_Triaged 2026-11-21 by the P2 challenger band._
