# Evaluation: easy-unlocker

**Repo:** [cyancity/easy-unlocker](https://github.com/cyancity/easy-unlocker)
**Stars:** 10 | **Last updated:** 2026-09-18 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-09-18
**Last triaged:** 2026-09-18  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Infrastructure

---

## What it does

Secrets management for AI agents — approve API keys and credentials on your phone with biometrics,
delivered end-to-end encrypted into the target process, so plaintext never enters the chat, logs,
or relay.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (agent-vault, kru, envlatch). Not enough to support an
ADOPT — this eval offers none.

## Triage note

Left at `discovery-log`: no overlapping STACK pick (P3 backlog). Its phone-biometric-approval
mechanism is a distinct approach from the local vault/keychain tools it's catalogued beside
(`agent-vault` is an HTTP credential proxy, `kru` and `envlatch` are local credential stores) —
none of them gate on an out-of-band human approval step the way this does. 10 stars, two days
old — worth a real eval if it keeps traction.

_Triaged 2026-09-18 by the daily discovery routine (today's new lead)._
