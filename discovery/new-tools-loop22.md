# Discovery Loop 22 — 2026-08-16 Daily Discovery

**Date:** 2026-08-16
**Scope:** GitHub repos created in last ~7 days across topics `claude-code`, `claude-skills`, `agent-skills`, `mcp-server`, `ai-agents`, `claude-code-plugin`, `coding-agent`, `opencode` + keyword searches — sorted by stars, deduped against CATALOG.md by slug and display name.

## Headline Finding

`deepseek-ai/deepseek-harness` ("DeepSeek Harness", DSH) launched ~3 days ago and already sits at ★126K, with a sprawling overnight plugin ecosystem (hundreds of `dsh-plugin`-tagged repos). It and its awesome-list were already catalogued by a prior run. Today's pass adds a handful of the most notable DSH ecosystem plugins plus other genuinely new, in-scope tools — not an exhaustive sweep of the DSH plugin explosion, which is now large enough to need its own dedicated future scan.

## Added (10 — cap reached)

| Repo | One-liner | Disposition |
|---|---|---|
| [seyedehsanhadi/sloptrim](https://github.com/seyedehsanhadi/sloptrim) | Local AI-writing-pattern detector, stdlib-only | added, left at discovery-log |
| [ccch1mneyyy/dsh-TUI](https://github.com/ccch1mneyyy/dsh-TUI) | Claude-Code-style TUI plugin for DeepSeek Harness (★1,460) | added, left at discovery-log |
| [Anionex/dsh-vision-toolkit](https://github.com/Anionex/dsh-vision-toolkit) | DSH-native adapter for agent-vision-toolkit | added, left at discovery-log |
| [Nagi-ovo/dsh-find-plugins](https://github.com/Nagi-ovo/dsh-find-plugins) | Finds/installs/verifies DSH plugins | added, left at discovery-log |
| [lennney/stop-that-shit](https://github.com/lennney/stop-that-shit) | Anti-overengineering guardrail for Codex | added, left at discovery-log |
| [chl03ks/shut-up-and-code](https://github.com/chl03ks/shut-up-and-code) | Load-bearing-comments-only skill | added, left at discovery-log |
| [SaladDay/pi-from-scratch](https://github.com/SaladDay/pi-from-scratch) | 600-line build-your-own-agent-loop walkthrough (★1,019) | added, left at discovery-log |
| [svy04/ballast](https://github.com/svy04/ballast) | Goal-decomposition/context-carryover plugin | added, left at discovery-log |
| [artemnovichkov/xcode-skills](https://github.com/artemnovichkov/xcode-skills) | Xcode 27 beta 5 skills as a Claude Code plugin | added, **SKIPped — no LICENSE file, vendored `plugin` Type** |
| [nmdra/opencode-cache-stats](https://github.com/nmdra/opencode-cache-stats) | opencode cache-hit/cost TUI plugin | added, left at discovery-log |

## Duplicates / Already Catalogued (not re-added)

`deepseek-harness`, `awesome-deepseek-harness`, `anti-slop` (AgriciDaniel's), `book-to-skill`, `skilldoctor`, `agent-safe-pipeline`, `tokentab`, `codex-bridge`, `unlazy`, `HERO-Anti-OverDefense`, `agent-link`, `bar-observatory`, `moli`, `doctrine`, `godmode`, `repo2skill`, `agent-vision-toolkit`, `hud-mode`, `pristine-skill`.

## Out of Scope (not added)

`vibe-aso` (App Store marketing), `free-my-arch` (Arch Linux disk cleanup utility), `vuln-report-skill` (bug-bounty report writing), `guizang-sports-skill` (sports/FIT-file analysis), `GEOHub` (SEO), `1c-quality-gate` (vertical-specific 1C:Enterprise/BSL tooling), `rakazo` (general chatbot), `loomfeed` (social platform), `mac-developer-bridge` (ChatGPT terminal bridge, not coding-agent specific), `freebuff-proxy` (API gateway with stealth/anti-detection framing — declined on ethics grounds, not a straightforward dev-tooling lead), `eliviz`/`vibe-coding-toolkit`/`kunpeng-skill`/`raincode` (lower-signal or heavily overlapping with existing catalogued tools; deprioritized under the 10-add cap).

## Triage This Run

- **New leads (10):** all triaged — 9 left at `discovery-log` (none clearly redundant with a STACK incumbent; two are P2 challengers judged non-redundant — `dsh-find-plugins`/`opencode-cache-stats` target different harnesses than the STACK picks they cite), 1 SKIPped (`xcode-skills`, license bar).
- **Oldest 5 re-triaged** (stalest `Last triaged` stamps, none SKIP-eligible on re-read — reasoning held, re-stamped 2026-08-16): `sigbound`, `deer-workflow`, `envlatch`, `trace-file-lineage`, `langhost`.

## Result

`make fix` then `make check` — green. Catalog total 720 → 730.
