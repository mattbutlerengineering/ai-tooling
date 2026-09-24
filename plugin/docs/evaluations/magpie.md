# Evaluation: magpie

**Repo:** [yetone/magpie](https://github.com/yetone/magpie)
**Stars:** 479 | **Last updated:** 2026-09-24 (pushed) | **License:** MIT
**Last verified:** 2026-09-24
**Last triaged:** 2026-09-24  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A macOS menu-bar app that routes each coding-agent CLI to a different backend model from one place —
e.g. Codex on DeepSeek, Claude Code on Kimi — instead of each CLI defaulting to its own vendor's model.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus
the CATALOG "Overlaps with" cell (claude-code-router, CLIProxyAPI, litellm). That is sufficient to
place the lead against its incumbents, not to support an ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`. Not a P2 challenger — none of its catalogued peers (claude-code-router,
CLIProxyAPI, litellm) are STACK picks, so there is no incumbent to weigh redundancy against. At 479
stars and one day old it is already one of the more traction-heavy leads in today's batch; a native
macOS menu-bar UI is a different shape from the CLI-proxy/gateway peers it overlaps, which argues for
a real look rather than a mechanical disposition either way.

_Triaged 2026-09-24 by the daily discovery routine (today's new lead)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [magpie](https://github.com/yetone/magpie) | tool | macOS menu-bar app (MIT, Go) routing each coding-agent CLI to a different backend model — Codex on DeepSeek, Claude Code on Kimi | Coding-agent CLIs default to one vendor's model with no quick way to swap backends per agent from one place | claude-code-router, CLIProxyAPI, litellm |
