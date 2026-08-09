# Evaluation: fleetpost

**Repo:** [StanimirTenev/fleetpost](https://github.com/StanimirTenev/fleetpost)
**Stars:** 1 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Implement (multi-machine agent coordination)
**Layer:** Infrastructure

---

## What it does

Offline-tolerant, server-less coordination for AI coding agents across machines, carried by any rclone remote (Drive/S3/Dropbox) instead of a running daemon or open ports.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge how well the mailbox-over-cloud-storage pattern holds up under real multi-agent load.

## Verdict

**discovery-log — tentative read** — Different problem than claude-squad (single-machine parallel terminal sessions): fleetpost is cross-machine, async, and needs no running server, which claude-squad doesn't attempt. Worth a real look rather than a mechanical SKIP as redundant.

_Triaged 2026-08-09 by the P2 challenger band._
