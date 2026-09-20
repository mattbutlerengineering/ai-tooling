# Evaluation: codex-remote-pro

**Repo:** [Vuk97/codex-remote-pro](https://github.com/Vuk97/codex-remote-pro)
**Stars:** 12 | **Last updated:** 2026-08-31 (pushed) | **License:** MIT
**Last verified:** 2026-09-07
**Last triaged:** 2026-09-07  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A ChatGPT↔Codex bridge — local coding agents ask ChatGPT for advice, and ChatGPT can inspect or remotely steer a running Codex session, with no API key required.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata plus the CATALOG "Overlaps with" cell. That is sufficient to decide whether this
lead is clearly dominated by a cataloged incumbent, not to judge the tool's actual behavior —
it would not support an ADOPT, and this eval offers none.

## Triage note

Left at `discovery-log`. Overlaps codex-with-chatgpt closely (both bridge ChatGPT reasoning into a Codex session); a real eval would need to compare the no-API-key bidirectional-steering claim against codex-with-chatgpt's design before a defensible redundancy SKIP could be written. Not attempting that comparison in a bulk pass.

_Triaged 2026-09-07 by the P3 backlog band._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codex-remote-pro](https://github.com/Vuk97/codex-remote-pro) | tool | ChatGPT↔Codex bridge (MIT) — local coding agents ask ChatGPT for advice, and ChatGPT can inspect or steer a running Codex session, no API key | Codex sessions run in isolation from ChatGPT's reasoning; want bidirectional advice and remote steering without an API key | codex-with-chatgpt, codex-plugin-cc, agy-staff |
