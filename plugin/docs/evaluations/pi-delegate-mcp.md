# Evaluation: pi-delegate-mcp

**Repo:** [howznguyen/pi-delegate-mcp](https://github.com/howznguyen/pi-delegate-mcp)
**Stars:** 14 | **Last updated:** 2026-08-25 (pushed) | **License:** MIT
**Last verified:** 2026-08-30
**Last triaged:** 2026-08-30  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

An MCP server (npm: `pi-delegate-mcp`) turning the `pi` coding agent into a steerable background worker — delegate a task to it, redirect it mid-run, and keep its context out of the caller's own.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`devfleet`, `claude-squad`, `gastown`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` (P2 challenger: cites `claude-squad` in "Overlaps with"). Not SKIPped as redundant — `claude-squad` is a tmux-based multi-session manager for running several agent instances in parallel, while pi-delegate-mcp is a narrower MCP-protocol mechanism for one caller to delegate to and steer a single `pi`-agent background worker mid-run. Different mechanism, different scope; whether it's differentiated enough to earn a seat needs a real look.

_Triaged 2026-08-30 by the P2 challenger band ([#567](https://github.com/mattbutlerengineering/ai-tooling/issues/567))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [pi-delegate-mcp](https://github.com/howznguyen/pi-delegate-mcp) | MCP server | MCP server (MIT) turning the pi coding agent into a steerable background worker — delegate, redirect mid-run, keep its context out of yours | Delegating a subtask to another agent means losing steering control or polluting your own context with its output | devfleet, claude-squad, gastown |
