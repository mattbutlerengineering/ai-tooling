# Evaluation: midscene

**Repo:** [web-infra-dev/midscene](https://github.com/web-infra-dev/midscene)
**Stars:** ~13,800 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Verify (UI testing / automation)
**Layer:** Tooling

---

## What it does

Midscene.js is open-source, **vision-driven UI testing and automation**: you write tests and automations in natural language, and a vision model executes them across platforms — web, iOS, and Android (and, via Midscene Skills, any platform driven by OpenClaw).

Mechanically, instead of brittle CSS/XPath selectors, Midscene uses a vision model to perceive what's actually on screen and act on natural-language instructions ("click the login button", "fill the registration form and pass all validations") plus assertions about visible state. The README showcases web form automation with field validation, iOS app flows (Meituan coffee order, auto-like a tweet), and Android flows (car specs, hotel booking) — the same natural-language approach across all three. It targets both automated UI testing and general cross-platform automation.

## How we tested it

Architecture review against the README and showcase list (web/iOS/Android natural-language automation, Midscene Skills for OpenClaw). Confirmed the vision-driven, selector-free model and the cross-platform (web + mobile) coverage. Did not run a live automation, so condition-gated.

```bash
gh api repos/web-infra-dev/midscene --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/web-infra-dev/midscene/readme --jq '.content' | base64 -d
```

## What worked

- **Selector-free, resilient tests.** Asserting on what's on screen (vision) rather than DOM selectors means tests survive markup refactors that break Playwright/Selenium selectors.
- **One approach, web + mobile.** Natural-language automation across web, iOS, and Android from a single tool is rare — most frameworks are web-only or mobile-only.
- **ByteDance web-infra backing.** A maintained project from a serious frontend-infra team; not an abandoned experiment.

## What didn't work or surprised us

- **Vision cost + nondeterminism.** A vision model per step spends tokens and can be flaky; you'll want stable prompts and possibly retries for reliable CI.
- **Overlaps Playwright/scenario/UI-TARS.** For pure web, Playwright is faster/cheaper; scenario tests agents; UI-TARS is a GUI agent. Midscene's niche is natural-language, vision-based cross-platform UI.
- **Verification vs. correctness.** Vision assertions can pass on a visually-plausible-but-wrong state; design assertions carefully.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Vision assertions catch real on-screen regressions across platforms |
| Speed | - | Per-step vision inference is slower/pricier than selector engines |
| Maintainability | + | Selector-free tests survive DOM/markup refactors |
| Safety | neutral | Testing tool; no direct safety effect |
| Cost Efficiency | - | Vision-model calls per step add cost vs. Playwright |

## Verdict

**CONDITIONAL**

Adopt when you need cross-platform (web + mobile) UI automation/testing in natural language and want resilience to selector/DOM churn — its standout over Playwright/Selenium. Accept the per-step vision cost and nondeterminism, and pin prompts for stable CI. For web-only, high-volume testing, a selector engine is cheaper; reach for Midscene when mobile coverage or selector-free robustness matters.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [midscene](https://github.com/web-infra-dev/midscene) | tool | Vision-driven UI testing/automation (MIT, ★14K, by ByteDance web-infra) — write tests/automations in natural language executed by a vision model across web, iOS, and Android; assert on what's on screen, not brittle selectors | UI tests break on selector/DOM changes and don't cover mobile; want natural-language, vision-based cross-platform automation | scenario, chrome-devtools-mcp, UI-TARS-desktop, agent-browser |
