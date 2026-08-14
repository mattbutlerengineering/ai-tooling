# Evaluation: deepseek-harness

**Repo:** [deepseek-ai/deepseek-harness](https://github.com/deepseek-ai/deepseek-harness)
**Stars:** 88,958 | **Last updated:** 2026-08-13 (pushed) | **License:** MIT
**Last verified:** 2026-08-14
**Last triaged:** 2026-08-14  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Catalog one-liner: "DeepSeek's first-party 'everything is a plugin' coding agent harness (MIT), launched alongside an already-sprawling dsh-plugin ecosystem." DeepSeek's own first-party terminal coding-agent harness, comparable in shape to Claude Code, OpenAI's `codex`, and `opencode` — a first-party agent loop from a major model lab rather than a third-party wrapper around an API.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata (created 2026-08-13, MIT license, official `deepseek-ai` org — the same org publishing DeepSeek-V3/R1) plus the CATALOG "Overlaps with" cell. That is sufficient to catalog the lead and note its scale, not to reach a verdict on the tool's behavior. It would not support an ADOPT, and this eval offers none.

## Verdict

**discovery-log — tentative read**

## Triage note

Left at `discovery-log`: this is a first-party coding-agent harness launched one day before this
triage pass by DeepSeek (the same org behind DeepSeek-V3/R1), already carrying an ~89K star count
and a fast-growing third-party `dsh-plugin` ecosystem (see the companion lead
`awesome-deepseek-harness`). That scale and provenance make it a clear P0 candidate for a real
hands-on eval, not something to dispose of mechanically — leaving it for the `P0/eval-runner` lane
rather than SKIPping it as redundant with `opencode`/`codex`/`aider`, since "DeepSeek's first-party
harness" is not the same claim as any of those.

_Triaged 2026-08-14 by the P3 backlog band (daily discovery routine)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [deepseek-harness](https://github.com/deepseek-ai/deepseek-harness) | harness | DeepSeek's first-party "everything is a plugin" coding agent harness (MIT), launched alongside an already-sprawling dsh-plugin ecosystem | Want a first-party DeepSeek coding-agent harness on par with Claude Code/Codex/opencode, not a third-party wrapper around the DeepSeek API | opencode, codex, aider, cline |
