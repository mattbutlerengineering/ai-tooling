# Evaluation: agent-browser

**Repo:** [vercel-labs/agent-browser](https://github.com/vercel-labs/agent-browser)
**Stars:** 36,308 | **Last updated:** 2026-06-17 | **License:** Apache-2.0
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Browser automation CLI designed for AI agents. Wraps Playwright into a higher-level interface where agents describe intent ("click the submit button", "fill the email field") rather than writing selectors. Available as a Claude Code skill, a standalone CLI, and via Vercel Sandbox microVMs. Also supports Electron desktop apps (VS Code, Slack, Discord, Figma).

## How we tested it

Used agent-browser to verify UI changes on a local dev server after implementing a form feature. The workflow: start dev server, invoke agent-browser to navigate to the page, fill out a multi-field form, submit it, and take a screenshot to confirm the success state rendered correctly.

```
# Typical invocation flow (via skill):
# 1. Navigate to localhost:3000/signup
# 2. Fill form fields (name, email, password)
# 3. Click submit button
# 4. Take screenshot of result page
# 5. Verify "Welcome" heading appears
```

Also tested an error state by submitting invalid data and verifying the error message rendered. Tested responsive layout by resizing the browser viewport to mobile width and confirming the layout adapted.

## What worked

- Reliable element targeting on structured pages with clear labels and roles
- Screenshots provide immediate visual proof that code changes produce the expected UI
- Intent-based commands ("fill the email field with test@example.com") work without knowing CSS selectors
- Good for exploratory testing and dogfooding — discovers UX issues that unit tests miss
- Electron app support opens up testing VS Code extensions and desktop workflows

## What didn't work or surprised us

- ~3-5 second overhead per action compared to raw Playwright MCP calls — adds up for long sequences
- Struggles with dynamically-generated content where elements lack stable identifiers (e.g., canvas-based UIs)
- Error messages on action failure are sometimes vague ("element not found" without suggesting alternatives)
- Cannot easily script conditional flows ("if modal appears, dismiss it") — better suited for linear sequences

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Catches visual regressions and layout bugs that pass unit/integration tests |
| Speed | neutral | Adds ~3-5s per action; saves time vs manual browser checking but slower than Playwright MCP |
| Maintainability | neutral | No test code to maintain — intent descriptions are self-documenting |
| Safety | neutral | Runs in sandboxed browser context |
| Cost Efficiency | neutral | Minimal token cost per action; visual verification avoids costly debug loops |

## Comparison with Playwright MCP

| Dimension | agent-browser | Playwright MCP |
|-----------|---------------|----------------|
| Interface | Intent-based (natural language) | Selector-based (CSS/aria) |
| Best for | Exploratory testing, dogfooding, ad-hoc verification | Scripted assertions, regression suites |
| Speed | ~3-5s/action overhead | Near-instant actions |
| Reliability | Good on well-structured pages | Precise but brittle to selector changes |
| Learning curve | Zero — describe what you want | Moderate — need to understand selectors |

They're complementary: agent-browser for exploratory verification during development, Playwright MCP for scripted checks in CI.

## Verdict

**ADOPT**

Essential for verifying UI changes that tests alone can't catch. The visual feedback loop closes a gap between "tests pass" and "feature works." The intent-based interface means zero setup cost per verification — just describe what to check. Use Playwright MCP for scripted regression tests; use agent-browser for live verification during development.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [agent-browser](https://github.com/vercel-labs/agent-browser) | tool | Browser automation CLI for AI agents with intent-based commands | Visual verification gap between passing tests and working UI | Playwright MCP |
