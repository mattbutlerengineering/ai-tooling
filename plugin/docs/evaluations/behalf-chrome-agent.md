# Evaluation: behalf-chrome-agent

**Repo:** [GKihlstadius/behalf-chrome-agent](https://github.com/GKihlstadius/behalf-chrome-agent)
**Stars:** 0 | **Last updated:** 2026-08-09 (pushed) | **License:** MIT
**Last verified:** 2026-08-09
**Last triaged:** 2026-08-09  <!-- triaged: bulk -->
**Dev loop stage:** Verify (browser automation)
**Layer:** Tooling

---

## What it does

A command line driving a real, already-signed-in Chrome via the Chrome DevTools Protocol, so an agent gets "hands" in the browser session you're already logged into, rather than a fresh headless instance.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata plus the CATALOG "Overlaps with" cell. That is sufficient to place the lead, not to judge how reliably it drives a real browser session in practice.

## Verdict

**discovery-log — tentative read** — playwright (ADOPT) is headless-first; behalf-chrome-agent's pitch is reusing your existing logged-in session, which reaches sites gated behind auth that a fresh headless context can't. A real capability gap, not just a repackaging, but 0 stars and day-old — worth a look once it has some track record rather than a mechanical SKIP as redundant with playwright.

_Triaged 2026-08-09 by the P2 challenger band._
