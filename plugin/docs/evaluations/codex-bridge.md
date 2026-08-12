# Evaluation: codex-bridge

**Repo:** [Sateezg/codex-bridge](https://github.com/Sateezg/codex-bridge)
**Stars:** 306 | **Last updated:** 2026-08-10 (pushed) | **License:** MIT
**Last verified:** 2026-08-12
**Last triaged:** 2026-08-12  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin that bridges an existing Codex CLI login to add gpt-image-2 image
generation and GPT-5 subagents inside Claude Code sessions, without a separate OpenAI API key.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell. That is sufficient to place it against nearby provider-bridge
tools, not to support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. It is a fresh (created 2026-08-09), single-purpose bridge distinct from
the general-purpose model routers it neighbors (`cursor-bridge`, `claude-code-router`,
`CLIProxyAPI`) — those route arbitrary providers/subscriptions, this one specifically imports two
capabilities (image gen, GPT-5 subagents) via a Codex login. Not clearly redundant with anything
catalogued; worth a real look rather than a mechanical dispose.

_Triaged 2026-08-12 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-bridge](https://github.com/Sateezg/codex-bridge) | plugin | Claude Code plugin (MIT) bridging your existing Codex CLI login for gpt-image-2 generation and GPT-5 subagents | Want image generation and GPT-5 subagents inside Claude Code without paying for a separate OpenAI API key | cursor-bridge, claude-code-router, CLIProxyAPI |
