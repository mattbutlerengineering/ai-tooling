# Evaluation: envlatch

**Repo:** [Raylinkh/envlatch](https://github.com/Raylinkh/envlatch)
**License:** MIT
**Last verified:** 2026-07-31
**Last triaged:** 2026-07-31  <!-- triaged: bulk -->
**Dev loop stage:** Security & Safety
**Layer:** Tooling

---

## What it does

Native macOS Keychain launcher for API keys used by local agents, SDKs, scripts, and backends.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (agent-vault, cc-safety-net). That is sufficient to place
the lead and note none of its named overlaps are STACK incumbents, not to support an ADOPT —
this eval offers none.

## Triage note

Left at `discovery-log`: agent-vault is an HTTP credential proxy/vault (cross-platform, network
service); envlatch is a macOS-only native Keychain launcher with no running service. Different
mechanism and platform scope, not clearly dominated. Left for the P0/eval-runner lane.

_Triaged 2026-07-31 by today's discovery lead._
