# Evaluation: DebugMCP

**Repo:** [microsoft/DebugMCP](https://github.com/microsoft/DebugMCP)
**Stars:** ~390 | **Last updated:** 2026-06-20 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-03  <!-- triaged: bulk -->
**Dev loop stage:** Verify (interactive debugging / MCP server)
**Layer:** Infrastructure

---

## What it does

An MCP server (shipped as a VS Code extension) that gives AI agents a **real interactive debugger**. Instead of debugging by adding print statements, an agent can set breakpoints, step through execution, inspect variables, and evaluate expressions inside VS Code.

Mechanically it bridges MCP-compatible assistants (Codex, GitHub Copilot, Copilot CLI, Cline, Cursor, Windsurf, Roo Code) to the VS Code debug adapter, working with any VS Code-supported language. The 2.0 release adds a `/really-debug` **agent skill** auto-installed into each configured harness's skills directory (e.g. `~/.copilot/skills/really-debug/`) that loads a systematic debugging workflow and invokes the DebugMCP tools with the right context. `start_debugging` with a `testName` uses the VS Code **Testing API** to discover/launch tests reliably across pytest, Jest/Vitest, Java, .NET, Go, etc., producing consistent breakpoint hits inside individual test cases.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and the 2.0 feature notes. Confirmed the MCP-server-over-VS-Code-debug-adapter design, the breakpoint/step/inspect/evaluate capabilities, the multi-assistant compatibility, the `/really-debug` companion skill, and the VS Code Testing API integration for test-level debugging. Did not run a live debug session, so condition-gated.

```bash
gh api repos/microsoft/DebugMCP --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/microsoft/DebugMCP/readme --jq '.content' | base64 -d
```

## What worked

- **A real debugger beats print debugging.** Giving agents breakpoints, stepping, and variable inspection is a categorical upgrade over log-and-guess — the right way to diagnose state-dependent bugs.
- **Test-aware via the Testing API.** Launching individual tests and hitting breakpoints inside them (pytest/Jest/Java/.NET/Go) is exactly what's needed to debug a failing test, not just a script.
- **Broad assistant support + companion skill.** MCP-standard, works across many agents, and the `/really-debug` skill packages a systematic workflow so the agent uses the tools well.

## What didn't work or surprised us

- **VS Code-bound.** It rides the VS Code debug/Testing APIs, so it's for VS Code-based agents — not terminal-only CLIs without that integration.
- **Young project.** ~390 stars; capability breadth depends on each language's VS Code debug-adapter maturity.
- **Agent must drive it well.** A debugger is only as good as the debugging strategy; the `/really-debug` skill helps, but undirected stepping can still wander.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Real breakpoint/variable inspection finds root causes vs. guessing |
| Speed | + | Test-level debugging shortens the diagnose loop for failing tests |
| Maintainability | neutral | A debugging capability; doesn't alter code structure |
| Safety | + | Inspection-based diagnosis reduces blind speculative edits |
| Cost Efficiency | + | Free/OSS; fewer wasted agent turns guessing at bugs |

## Verdict

**discovery-log — tentative read**

Adopt when you use a VS Code-based AI assistant and want it to debug with a real debugger — breakpoints, stepping, variable inspection, and test-level launches — instead of print statements. The `/really-debug` skill makes the agent use it systematically. Less relevant for terminal-only CLI harnesses without VS Code; for those, systematic-debugging discipline plus logs remains the path.

## Triage note

Left at `discovery-log`, not SKIPped — no STACK pick covers what it does.
[`serena`](https://github.com/oraios/serena) appears in its overlaps, but the two only meet at
"code-aware MCP server": serena does *static* symbol navigation and editing, DebugMCP does
*runtime* debugging — breakpoints, stepping, variable inspection, expression evaluation via the
VS Code debug and Testing APIs. Nothing in STACK gives an agent a real debugger, so there is no
incumbent for it to be redundant with.

It is also first-party Microsoft and MIT, and it attacks a genuine failure mode this catalog
cares about (agents debugging by adding print statements and guessing). A capability with no
incumbent and a plausible Correctness claim belongs in the P0 measure band, not a skip list.

_Triaged 2026-08-03 by the P2 challenger band ([#266](https://github.com/mattbutlerengineering/ai-tooling/issues/266))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [DebugMCP](https://github.com/microsoft/DebugMCP) | MCP server | Real interactive debugger for AI agents (MIT, by Microsoft) — lets VS Code-based agents (Copilot/Codex/Cline/Cursor/Windsurf/Roo) set breakpoints, step, inspect variables, and evaluate expressions via the VS Code debug + Testing APIs; ships a `/really-debug` skill | Agents debug by adding print statements and guessing; want them to use a real debugger like a human | chrome-devtools-mcp, DesktopCommanderMCP, serena |
