# Evaluation: BossConsole

**Repo:** [risa-labs-inc/BossConsole](https://github.com/risa-labs-inc/BossConsole)
**Stars:** 215 | **Last updated:** 2026-08-04 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-agent session management)
**Layer:** Tooling

---

## What it does

A multi-platform operator's console built on the JVM rather than Electron, running Claude Code,
Codex, Gemini or OpenCode alongside a browser, terminal, editor, secrets store and 100+ MCP tools.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04 — the
repo had no record in `repo-metadata.json` before this pass) plus the CATALOG one-liner and
"Overlaps with" cell (`cc-switch`, `Nimbalyst`, `claude-squad`, `HolyClaude`). Sufficient for a SKIP
that turns on *redundancy with a catalogued incumbent*; not sufficient for a positive verdict, and
none is offered.

## Verdict

**SKIP** — redundant with [`claude-squad`](https://github.com/smtg-ai/claude-squad) (STACK, `RUN`).
Running several coding agents from one console with visibility into each is the incumbent's job; the
additions here — an embedded browser, editor and secrets store — make it a workspace around that
job rather than a different one.

Not-Electron is the differentiator the description leads with, and it is an implementation choice
rather than a capability. It matters to whoever maintains the console; it does not change what the
tool lets an agent do.

★215 against the incumbent's ★8.1K is the deciding fact. This cluster is unusually crowded — the
same pass disposed `Nimbalyst`, `agent-of-empires`, `dmux`, `eigent` and `superset` against the same
incumbent and left `herdr` (★24K, Apache-2.0) open as the one genuine head-to-head. A 215-star entry
is not that challenger.

Re-open if the 100+ MCP tool surface turns out to be the point, in which case it is an MCP
aggregation question rather than a session-management one.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [BossConsole](https://github.com/risa-labs-inc/BossConsole) | platform | Multi-platform operator's console (JVM, not Electron) running Claude Code, Codex, Gemini, or OpenCode with browser, terminal, editor, secrets, and 100+ MCP tools | Want one operator surface for several agents without an Electron app | cc-switch, Nimbalyst, claude-squad, HolyClaude |
