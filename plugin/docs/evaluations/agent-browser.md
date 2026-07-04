# Evaluation: agent-browser

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
**Stars:** 36,308 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Browser automation CLI designed for AI agents. Wraps Playwright into a higher-level interface where agents describe intent ("click the submit button", "fill the email field") rather than writing selectors. Available as a Claude Code skill, a standalone CLI, and via Vercel Sandbox microVMs. Also supports Electron desktop apps (VS Code, Slack, Discord, Figma).

## How we tested it

**Evidence:** REVIEW

**Capability/README review — not run hands-on.** This is a documentation-and-design review of the skill's surface (its description, the actions it exposes, and how it positions itself versus Playwright MCP), not a recorded live run. Exercising it meaningfully needs a running dev server (or an Electron target) and an interactive browser session rather than a scriptable one-shot, so no timing, reliability, or per-action numbers are claimed here as measured.

For a *measured* browser-automation eval in this catalog, see [playwright-mcp.md](playwright-mcp.md), where a live navigate + accessibility snapshot was actually captured.

## What it offers (from the surface review)

- Intent-based commands ("fill the email field with …", "click the submit button") so the agent describes goals instead of authoring CSS/aria selectors — the headline ergonomic difference from raw Playwright MCP.
- Screenshot capture for visual confirmation of UI state, useful for catching layout/visual regressions that unit and integration tests don't.
- Multiple delivery modes: Claude Code skill, standalone CLI, and Vercel Sandbox microVMs.
- Electron desktop-app support (VS Code, Slack, Discord, Figma), which extends it beyond web pages to desktop workflows.

## Open questions (would need a hands-on run to answer)

- Per-action overhead versus raw Playwright MCP calls — the intent-resolution step plausibly adds latency, but this was not measured.
- Behavior on dynamically-generated content where elements lack stable identifiers (e.g. canvas-based UIs).
- Quality of failure messages and whether conditional flows ("if a modal appears, dismiss it") are expressible.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (claimed) | Visual/intent-based verification targets UI bugs that pass unit/integration tests — not yet confirmed by a run here. |
| Speed | neutral | Saves manual browser checking; per-action overhead vs Playwright MCP unmeasured. |
| Maintainability | neutral | No test code to maintain — intent descriptions are self-documenting. |
| Safety | neutral | Runs in a sandboxed browser context. |
| Cost Efficiency | neutral | Screenshots carry image-token cost; Playwright MCP's text snapshot is cheaper for reading state. |

## Comparison with Playwright MCP

| Dimension | agent-browser | Playwright MCP |
|-----------|---------------|----------------|
| Interface | Intent-based (natural language) | Snapshot-ref / selector-based |
| Best for | Exploratory testing, dogfooding, ad-hoc verification | Scripted assertions, regression suites |
| State readout | Screenshots (image payload) | YAML accessibility snapshot (no image) — verified |
| Reliability | Claimed good on structured pages (unverified here) | Precise but brittle to selector changes |
| Learning curve | Zero — describe what you want | Moderate — operate on refs/selectors |

They're complementary: agent-browser for exploratory verification during development, Playwright MCP for scripted checks in CI.

## Verdict

**CONDITIONAL** (review-based; promote to ADOPT after a hands-on run)

On its design, agent-browser targets a real gap — intent-based UI verification that closes the distance between "tests pass" and "feature works," with no per-check selector authoring. That's a strong fit for exploratory verification during development, with Playwright MCP (measured in this catalog) as the precise scripted-checks counterpart. Held at CONDITIONAL rather than ADOPT only because this evaluation is a surface review, not a recorded live run; the open questions above (per-action overhead, dynamic content, conditional flows) should be confirmed before treating it as a default.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-browser](https://github.com/vercel-labs/agent-browser) | tool | Browser automation CLI for AI agents with intent-based commands | Visual verification gap between passing tests and working UI | Playwright MCP |
