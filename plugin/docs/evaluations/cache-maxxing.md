# Evaluation: cache-maxxing

**Repo:** [5m0k3/cache-maxxing](https://github.com/5m0k3/cache-maxxing)
**Stars:** 27 | **Last updated:** 2026-11-17 (pushed) | **License:** MIT
**Last verified:** 2026-11-18
**Last triaged:** 2026-11-18  <!-- triaged: bulk -->
**Dev loop stage:** Outer Loop
**Layer:** Tooling

---

## What it does

A status bar above the chat showing when Claude's prompt cache will expire and what the next
message is projected to cost, so you can see both before you send.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner plus repo metadata (stars, license, push date). That is sufficient for the verdict
below, which turns on *redundancy with an already-catalogued tool solving the same problem*, not
on the tool's behaviour. It would not support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — redundant with `cache-tax` (already catalogued, MIT): both show a pre-send warning for
prompt-cache-expiry/cost before a cold send, and `cache-tax` additionally keeps the cache warm
during breaks rather than only reporting on it. No distinct capability here that `cache-tax` (or
the broader `ccusage`/`token-step-tracker` cost-reporting cluster) doesn't already cover.

_Triaged 2026-11-18 by the P2 challenger band._
