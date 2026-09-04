# Evaluation: codex-with-chatgpt

**Repo:** [XiaoDuoYa/codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt)
**Stars:** 2,339 | **Last updated:** 2026-09-02 (pushed) | **License:** MIT
**Last verified:** 2026-09-03
**Last triaged:** 2026-09-03  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

An MCP bridge letting ChatGPT act as the planning brain for a local OpenAI Codex coding-agent session — Codex keeps executing (editing files, running commands) while ChatGPT is consulted for reasoning/planning, over OAuth, no separate API key.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`codex`, `lazycodex`, `codex-plugin-cc`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet (P3 backlog). It's a narrow augmentation of the `codex` harness rather than a competing harness in its own right, so no redundancy SKIP applies; whether cross-model planning is worth the added complexity over Codex's own reasoning needs a real look.

_Triaged 2026-09-03 by the P3 backlog band ([#579](https://github.com/mattbutlerengineering/ai-tooling/issues/579))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-with-chatgpt](https://github.com/XiaoDuoYa/codex-with-chatgpt) | tool | MCP bridge (MIT, ★2.3K) letting ChatGPT act as the planning brain for a local OpenAI Codex coding-agent session, while Codex keeps doing the execution | Codex plans within its own context window; want ChatGPT's reasoning steering a Codex run without replacing the Codex harness | codex, lazycodex, codex-plugin-cc |
