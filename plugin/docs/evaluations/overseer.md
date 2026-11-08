# Evaluation: overseer

**Repo:** [basilelt/overseer](https://github.com/basilelt/overseer)
**Stars:** 7 | **Last updated:** 2026-11-08 (pushed) | **License:** AGPL-3.0
**Last verified:** 2026-11-08
**Last triaged:** 2026-11-08  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Runs and supervises AI coding agents side by side, locally or on a server over SSH.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
(license, description) plus the CATALOG "Overlaps with" cell. That is sufficient for the verdict
below, because the verdict turns on *license*, not on the tool's behaviour. It would not support
an ADOPT, and this eval offers none.

## Verdict

**SKIP** — AGPL-3.0. This run's license bar disqualifies copyleft: only permissive, MIT-like OSS
is adoptable for this catalog. AGPL-3.0 imposes network-use copyleft obligations that a
permissive-only adoption policy is not prepared to take on, independent of whether the artifact
would otherwise be vendored. `claude-squad` (MIT, a STACK pick) already covers the "manage
multiple AI terminal agents" job this repo overlaps with, under unambiguous terms.

_Triaged 2026-11-08 under this run's license bar (copyleft or missing license ⇒ SKIP), stated in
the scheduled discovery-and-triage task's hard rules._
