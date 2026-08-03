# Evaluation: codex

**Repo:** [openai/codex](https://github.com/openai/codex)
**Stars:** 96,747 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-03
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

OpenAI's open-source terminal coding agent — a sandboxed local agent that reads/edits your repo and
runs commands with configurable approval modes, MCP support, and config profiles.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (opencode, aider, cline, gemini-cli, codex-plugin-cc). That is
sufficient to place the lead, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: at ~97K stars, Codex is OpenAI's first-party terminal coding agent and a
direct, highly significant peer to Claude Code itself — clearly not redundant with any single
catalogued tool, and far too consequential to mechanically SKIP. Left for the P0/eval-runner lane.

_Triaged 2026-08-03 by today's discovery lead (5-oldest-untriaged pass)._
