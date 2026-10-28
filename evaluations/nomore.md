# Evaluation: nomore

**Repo:** [globalmpc/nomore](https://github.com/globalmpc/nomore)
**Stars:** 61 | **Last updated:** 2026-10-28 (pushed) | **License:** MIT
**Last verified:** 2026-10-28
**Last triaged:** 2026-10-28  <!-- triaged: bulk -->
**Dev loop stage:** Plan
**Layer:** Tooling

---

## What it does

A local CLI that finds the corrections you keep repeating to Claude Code and turns them into evidence-backed CLAUDE.md rules, plus a public rule pack mined from claude-code issues. No LLM call by default.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (claude-reflect). That is sufficient for a SKIP that turns on redundancy with a catalogued incumbent, not on the tool's behavior — a question the overlap answers directly. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `claude-reflect` (KEEP, MEASURED, already installed and validated). Both solve the same job — turning repeated corrections/mistakes into a durable CLAUDE.md instruction — and claude-reflect is the established, run-backed incumbent already covering it in this stack. nomore's local-only, no-LLM-by-default angle is a real design difference worth noting, but not enough on its own to justify a second tool for the same job without a hands-on bake-off.

_Triaged 2026-10-28 by the P2 challenger band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [nomore](https://github.com/globalmpc/nomore) | tool | Finds the corrections you keep repeating to Claude Code and turns them into evidence-backed CLAUDE.md rules (MIT) | The same mistakes keep recurring across sessions because nothing turns repeated corrections into a durable instruction file | requirement-ledger, cli-faq-shortcuts, claude-reflect |
