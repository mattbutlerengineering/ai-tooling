# Evaluation: kru

**Repo:** [omaekumiko2-create/kru](https://github.com/omaekumiko2-create/kru)
**Stars:** 43 | **Last updated:** 2026-08-29 (pushed) | **License:** MIT
**Last verified:** 2026-08-29
**Last triaged:** 2026-08-29  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

A local-first MCP server (Rust) acting as a password and credential manager for AI agents — passwords, API keys, SSH identities, and TOTP codes, used without exposing the underlying plaintext to the model.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell (`agent-vault`, `envlatch`, `secretguard-mcp`). It would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log` — a first-time lead with no overlap pressure yet. Not SKIPped: the catalog already carries `agent-vault` (HTTP credential proxy) and `envlatch` (macOS Keychain launcher) in the same Security & Safety credential-management cluster, but neither is local-first + cross-platform + MCP-native the way this claims to be; whether it's genuinely differentiated or redundant with those two needs a real read, not a mechanical guess.

_Triaged 2026-08-29 by the P3 backlog band ([#565](https://github.com/mattbutlerengineering/ai-tooling/issues/565))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [kru](https://github.com/omaekumiko2-create/kru) | MCP server | Local-first MCP password/credential manager (MIT, Rust) for AI agents — passwords, API keys, SSH identities, and TOTP, without exposing hidden plaintext to the model | Agents need credentials to do useful work, but handing them plaintext secrets in context is a leak waiting to happen | agent-vault, envlatch, secretguard-mcp |
