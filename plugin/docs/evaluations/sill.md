# Evaluation: sill

**Repo:** [lemonadesaltbagel/sill](https://github.com/lemonadesaltbagel/sill)
**Stars:** 55 | **Last updated:** 2026-10-28 (pushed) | **License:** none declared
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

A native Windows Bash implementation (Rust) so AI coding-agent CLIs — Claude Code, Codex, opencode, Gemini CLI — run without Git Bash, MSYS2, or WSL; ships with MCP support.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata and the CATALOG one-liner/overlaps. That is sufficient to place the lead, not to judge the tool's behavior hands-on.

## Verdict

**discovery-log — tentative read** — not previously examined; added and triaged this pass as a new lead. No structural signal disposes it mechanically — it has no STACK-pick overlap in "Overlaps with" and carries no license to flag.

## Triage note

P3 backlog. Left at `discovery-log`; the nearest catalogued neighbors (ai-terminal-manager, codex-kit, CLIProxyAPI) manage sessions or route traffic rather than replace the POSIX-shell layer itself on Windows, so this fills a different, narrower gap. No license is declared, which would matter for adoption but isn't itself grounds for a mechanical SKIP (it isn't a vendored skill/plugin). A hands-on look is left for a future pass.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [sill](https://github.com/lemonadesaltbagel/sill) | tool | Native Windows Bash for AI coding agents (⚠️ no license, Rust) — run Claude Code, Codex, opencode, Gemini CLI with no Git Bash, MSYS2, or WSL | Coding-agent CLIs assume a POSIX shell on Windows, forcing Git Bash, MSYS2, or WSL just to run them | ai-terminal-manager, codex-kit, CLIProxyAPI |
