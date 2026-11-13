# Evaluation: contraband

**Repo:** [knight-byte/contraband](https://github.com/knight-byte/contraband)
**Stars:** 0 | **Last updated:** 2026-11-11 (pushed) | **License:** Apache-2.0
**Last verified:** 2026-11-13
**Last triaged:** 2026-11-13  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A local-first egress auditor attributing outbound network traffic to package
installs, dev tools, and AI agents — process-level attribution via eBPF on Linux
and Endpoint Security + pktap on macOS.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
the repo's own description plus the CATALOG "Overlaps with" cell.

## Triage note

Freshly catalogued (added today, 2026-11-13). Overlaps `numbat`, `onlyread`, and
`toolpermit` — none a STACK incumbent — so this is ordinary P3 backlog. Left at
`discovery-log`; stamped only. (A same-day candidate, `hamarshehmhmd/egresswall`,
covers the same niche but is AGPL-3.0 and was not catalogued — noted in the scan
issue rather than added as a second, license-barred lead for the same job.)
