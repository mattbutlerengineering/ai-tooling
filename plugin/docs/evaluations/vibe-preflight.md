# Evaluation: vibe-preflight

**Repo:** [globalmpc/vibe-preflight](https://github.com/globalmpc/vibe-preflight)
**Stars:** 65 | **Last updated:** 2026-11-09 (pushed) | **License:** MIT
**Last verified:** 2026-11-12
**Last triaged:** 2026-11-12  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Process

---

## What it does

A Claude Code skill (`/vibe-preflight`) that runs a pre-flight check on a vibe-coded app
before it goes live: security (keys in code, missing auth, SQL injection), cost/abuse
(unmetered paid APIs), unfinished code (TODO stubs, fake data, disabled auth), deploy
readiness (missing env docs, dev mode in prod), containers (Docker/Podman misconfig), and
hosting-platform-specific pitfalls (Vercel/Netlify/Cloudflare/Render/Railway/Fly.io), per
the repo's own README. Writes a plain-language report for the user and a technical
details file for the agent/developer, and changes nothing until the user picks which
findings to fix.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (fetched 2026-11-12) plus the CATALOG one-liner and "Overlaps with" cell, and a
README skim (confirmed via `raw.githubusercontent.com`, not an install). That is
sufficient to decide whether this lead is clearly dominated by a cataloged incumbent, not
to judge the tool's actual behavior — it would not support an ADOPT, and this eval offers
none.

## Triage note

Left at `discovery-log`, not SKIPped as redundant with `prod-readiness` (catalog SKIP, no
license) or `AXguard` (discovery-log, security-only). `prod-readiness` is itself already
SKIPped for having no license, so it cannot be the incumbent this lead is redundant
against; `AXguard` covers security scanning only, while vibe-preflight's scope is broader
(security + cost/abuse + unfinished code + deploy/hosting-platform readiness). That
breadth is a real differentiator worth a hands-on eval rather than a mechanical SKIP.
