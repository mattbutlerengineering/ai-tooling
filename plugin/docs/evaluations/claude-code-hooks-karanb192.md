# Evaluation: claude-code-hooks (karanb192)

**Repo:** [karanb192/claude-code-hooks](https://github.com/karanb192/claude-code-hooks)
**Stars:** ~462 | **License:** MIT
**Last verified:** 2026-08-02
**Last triaged:** 2026-08-02  <!-- triaged: bulk -->
**Dev loop stage:** Skills & Plugins
**Layer:** Tooling

---

## What it does

An installable plugin marketplace of Claude Code hooks: safety guardrails (block dangerous commands, protect secrets/tests, git-safety), cost/token tracking (context-hogs), session logging, and productivity automation (auto-format, auto-stage). Seven installable plugins in total, each addressing a distinct hook use case, with configurable risk levels (critical/high/strict).

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: README and metadata gathered via web fetch. Sufficient to catalog and compare scope against existing hook tools, not to verify the hooks behave correctly in a live session.

## Triage note

Left at `discovery-log` rather than SKIPped: `cc-safety-net` (already catalogued) covers destructive-command safety specifically, and `claude-code-hooks-multi-agent-observability` covers observability specifically — this repo bundles safety + cost tracking + observability + productivity hooks as one installable marketplace, a broader scope than either single-purpose incumbent. That breadth is worth a real hands-on eval rather than a mechanical SKIP against either narrower tool.

_Triaged 2026-08-02 by the daily discovery routine (today's new lead)._
