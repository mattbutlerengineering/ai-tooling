# Evaluation: CloakBrowser

**Repo:** [CloakHQ/CloakBrowser](https://github.com/CloakHQ/CloakBrowser)
**Stars:** 26,633 | **Last updated:** 2026-06-20 (pushed) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** — (browser automation, but primarily anti-bot-detection — out of dev-loop scope)
**Layer:** Tooling (patched Chromium binary; drop-in Playwright/Puppeteer replacement, Python + JS)

---

## What it does

CloakBrowser is a **stealth Chromium build whose fingerprints are modified at the C++ source level** so anti-bot systems score it as an ordinary browser. It's a **drop-in Playwright/Puppeteer replacement** (swap the import) for Python and JavaScript, distributed via `pip`/`npm` with an auto-downloading, auto-updating binary. Its headline capability is **defeating bot detection** — it advertises passing FingerprintJS, Cloudflare Turnstile, and reCAPTCHA-class checks, plus a `humanize` mode for human-like input behavior, with guidance to pair it with residential proxies for protected sites.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection only — deliberately not installed or run.** Assessment is based on the repository README and metadata. The tool's anti-detection mechanics are described here only at the level needed to evaluate fit and risk; this evaluation does not reproduce or endorse evasion techniques.

```bash
gh api repos/CloakHQ/CloakBrowser --jq '{stars,license:.license.spdx_id,desc:.description}'   # 26.6K, MIT
```

## What worked

- **Technically credible.** Source-level fingerprint patching (rather than JS injection / config flags) is a genuinely more robust approach, and a true drop-in Playwright/Puppeteer API lowers adoption cost.
- **Easy distribution.** `pip install` / `npm install` with an auto-updating binary and a zero-install Docker `cloaktest` is well-packaged.
- **MIT, popular, active.**

## What didn't work or surprised us

- **It's a bot-detection-evasion tool, not a dev-loop tool.** Its purpose is to make automated browsing indistinguishable from a human to *defeat* anti-bot defenses. That does not move any of this catalog's quality signals (Correctness, Speed, Maintainability, Safety, Cost Efficiency) for the code you ship — it's web-scraping/automation infrastructure.
- **Dual-use with a malicious-leaning default.** Legitimate uses exist (testing *your own* anti-bot defenses, authorized data collection, QA against your own properties). But the primary advertised use — bypassing third-party bot detection, CAPTCHAs, and Cloudflare, with residential-proxy guidance — is the kind of detection-evasion that is frequently used against sites without authorization. Adopting it carries ToS and legal exposure.
- **Out of scope for this catalog.** The catalog already covers legitimate agent browser automation/testing (agent-browser, browser-use, playwright). CloakBrowser's distinguishing feature is precisely the evasion layer those tools intentionally don't provide.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | n/a | Not a code-quality tool. |
| Speed | n/a | — |
| Maintainability | n/a | — |
| Safety | − | Dual-use evasion; default use case (bypassing third-party bot detection) carries ToS/legal risk and is misuse-prone. |
| Cost Efficiency | n/a | — |

## Verdict

**SKIP** (recorded for triage hygiene, not adopted). CloakBrowser is a technically credible, MIT, drop-in stealth-Chromium replacement, but it's a **bot-detection-evasion / scraping tool**, not an AI-assisted-development tool — it doesn't move this catalog's quality signals, and its primary use case (defeating third-party anti-bot defenses) is dual-use with real ToS/legal risk. For legitimate agent browser automation and verification, use the catalog's existing tools (agent-browser, playwright, browser-use). Only consider CloakBrowser for explicitly authorized work against your own properties (e.g. testing your own anti-bot posture), and never as a way to access systems you don't control.

Compared to neighbors: **agent-browser**, **browser-use**, and **playwright** automate/test browsers for legitimate agent interaction and QA. CloakBrowser's distinguishing feature — source-level fingerprint evasion to defeat bot detection — is what places it outside this catalog's intended scope.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CloakBrowser](https://github.com/CloakHQ/CloakBrowser) | tool | Stealth Chromium with source-level (C++) fingerprint patches — drop-in Playwright/Puppeteer replacement (⚠️ SKIP: bot-detection-evasion tool, dual-use; out of dev-loop scope, authorized-use-only) | (Out of scope) defeating third-party bot detection for scraping/automation — not a code-quality concern | playwright, agent-browser, browser-use |
