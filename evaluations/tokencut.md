# Evaluation: tokencut

**Repo:** [00200200/tokencut](https://github.com/00200200/tokencut)
**Stars:** 10 | **Last updated:** 2026-09-22 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local CLI + MCP server that folds verbose tool output before it reaches Claude Code, Codex,
Cursor, or Claude Desktop, to keep the context window from filling with noise.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG "Overlaps with" cell (headroom, lean-ctx, token-optimizer-mcp). That is sufficient to
decide whether this lead is clearly dominated by a catalogued incumbent, not to judge the tool's
actual behavior — it would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `headroom` (STACK, Tier 1, `MEASURED`). headroom already compresses tool
outputs, logs, and files before they reach the LLM (60-95% fewer tokens, reversibly via local cache)
— the same core problem (context bloat from verbose tool output) tokencut addresses, for the same
client set (Claude Code, Codex, Cursor). The description discloses no mechanism distinct from
headroom's compress-after-the-fact approach, and at 10 stars and 4 days old there is no measured
comparison against the validated incumbent — not a reason to carry a second unvalidated tool in an
already-served niche.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tokencut](https://github.com/00200200/tokencut) | tool | Local CLI + MCP (MIT) folding verbose tool output before it reaches Claude Code, Codex, Cursor, or Claude Desktop | Verbose tool output fills the context window with nothing trimming it before the model reads it | headroom, lean-ctx, token-optimizer-mcp |
