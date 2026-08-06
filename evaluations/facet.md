# Evaluation: facet

**Repo:** [Smitner-Studio/facet](https://github.com/Smitner-Studio/facet)
**Stars:** 4 | **Last updated:** 2026-08-03 (pushed) | **License:** NOASSERTION (GitHub reports "Other" — no LICENSE file found)
**Last verified:** 2026-08-06
**Last triaged:** 2026-08-06  <!-- triaged: bulk -->
**Dev loop stage:** Dev Workflow
**Layer:** Tooling

---

## What it does

Renders agent-written Markdown as a live local page and sends the human's click back to the agent as typed data — a human-in-the-loop approval gate for coding agents, shipped as an MCP server.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (README, topics, license) via the GitHub API, plus the CATALOG "Overlaps with" cell. That is sufficient for a license-based SKIP, which turns on the repo's declared license rather than the tool's behavior.

## Verdict

**SKIP** — no permissive license. GitHub's licensee detector finds no LICENSE file (`license.spdx_id: NOASSERTION`, `key: other`), and per repo policy only permissive MIT-like OSS is adoptable; copyleft or missing-license tools are SKIPped regardless of merit. Revisit if the repo adds a permissive LICENSE file — the idea (visual human-in-the-loop approval for agents) is otherwise differentiated from `plannotator` (which reviews plans/diffs, not ad-hoc approval requests).

_Triaged 2026-08-06 by the daily discovery routine._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [facet](https://github.com/Smitner-Studio/facet) | MCP server | Human-in-the-loop approval gates for coding agents (⚠️ no license) — renders agent-written Markdown as a live local page and sends the human's click back to the agent as typed data | Agents need a human decision mid-task but only have blocking chat prompts or nothing at all; want a lightweight local approval UI | plannotator, claude-hud |
