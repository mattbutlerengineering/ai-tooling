# Evaluation: webapp-testing

**Repo:** [anthropics/skills](https://github.com/anthropics/skills/tree/main/skills/webapp-testing)
**Stars:** 179,396 (the container, `anthropics/skills`; the skill has no count of its own) | **Last updated:** 2026-09-29 | **License:** Apache-2.0 (the skill folder's own `LICENSE.txt`; the container repo root declares none)
**Last verified:** 2026-10-02
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Anthropic's skill for testing local web apps by writing native Python Playwright scripts, with a helper that manages the dev server. It lives inside `anthropics/skills` (`skills/webapp-testing/`: `SKILL.md`, `LICENSE.txt`, `scripts/with_server.py`, and three `examples/` scripts covering element discovery, static HTML via `file://`, and console logging). skills.sh listed **169K installs** on 2026-10-02.

The mechanism is a decision tree. For static HTML, read the file to find selectors. For a dynamic app with no server running, call `scripts/with_server.py --help`, then wrap your automation in it. If a server is already running, follow **reconnaissance, then action**: wait for `networkidle`, screenshot or dump the DOM, find selectors in the *rendered* page, then act. `with_server.py` (105 lines) starts one or more servers with `subprocess.Popen(..., shell=True)`, polls each port until it is ready (30 s default timeout), runs the command after `--`, and stops the servers afterwards. The skill tells the agent to treat bundled scripts as **black boxes** ("Always run scripts with `--help` first… DO NOT read the source"), so a large helper doesn't fill the context window.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read `SKILL.md` and the full `with_server.py` through the GitHub API, listed the folder, and checked the license situation. The container's repo metadata returns `license: null` and the repo root has no LICENSE file, while `skills/webapp-testing/LICENSE.txt` is the Apache License 2.0 text, and the SKILL.md frontmatter says `license: Complete terms in LICENSE.txt`. I compared it with the existing [playwright-skill.md](playwright-skill.md), [playwright-mcp.md](playwright-mcp.md), [agent-browser.md](agent-browser.md) and [playwright-best-practices.md](playwright-best-practices.md) evals. No browser was installed and no page was automated.

```bash
gh api repos/anthropics/skills --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/anthropics/skills/contents --jq '.[].path'          # no LICENSE at root
gh api repos/anthropics/skills/contents/skills/webapp-testing --jq '.[].path'
gh api repos/anthropics/skills/contents/skills/webapp-testing/SKILL.md --jq .content | base64 -d
gh api repos/anthropics/skills/contents/skills/webapp-testing/LICENSE.txt --jq .content | base64 -d | head -5
gh api repos/anthropics/skills/contents/skills/webapp-testing/scripts/with_server.py --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **Server lifecycle is solved, and it's the part people usually get wrong.** Multi-server support (backend + frontend), port polling and guaranteed shutdown remove the most common reason agent-driven browser checks fail: testing against a server that isn't up yet, or leaving zombie dev servers behind.
- **Reconnaissance-then-action is the right habit for agents.** Finding selectors in the *rendered* DOM after `networkidle`, rather than guessing them from source, is exactly the advice that prevents "element not found" loops.
- **Context discipline.** "Run `--help`, don't read the source" is a useful pattern for any script-backed skill. The container eval ([anthropics-skills.md](anthropics-skills.md)) singles out this repo as the reference for *how to build* script-backed skills.
- **Script-based, not MCP.** The output is a Python file you can keep, re-run and review, unlike tool calls in an MCP session that leave nothing behind.

## What didn't work or surprised us

- **The license lives in a subfolder and repo metadata misses it.** GitHub reads only the root LICENSE, so tooling that consumes metadata (this repo's `triage.py` included) would record `NONE` for the container. This skill is Apache-2.0 because of the folder's own `LICENSE.txt`. That is detector Z's #372 shape one level down: a subfolder grant, not a README one.
- **Python only, in mostly TypeScript-Playwright shops.** Teams with an existing `@playwright/test` suite get throwaway Python scripts in a second language rather than tests that go into their suite.
- **Verification, not a test suite.** No assertions framework, fixtures, reporters or CI story. It is good for "does this page work right now" and doesn't keep regression coverage.
- **`shell=True` and `networkidle` caveats.** The server command is passed to a shell (fine for the agent's own commands, not for untrusted input). `networkidle` is discouraged by Playwright's own docs for apps with long-polling or websockets, where it can hang until the timeout.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Rendered-DOM selector discovery and server readiness polling remove two common false-failure sources |
| Speed | + | One helper call replaces hand-rolled server start/wait/kill logic |
| Maintainability | neutral | Scripts are disposable Python, outside the project's own test suite |
| Safety | neutral | Headless local browsing; `shell=True` on agent-supplied server commands |
| Cost Efficiency | + | Black-box script use keeps a 105-line helper out of context |
| Verifiability | + | Leaves a re-runnable script plus screenshots/console logs a human can inspect |

## Verdict

**discovery-log — tentative read** — the best-built lightweight option in this scan for "drive my local web app and look at it". Server lifecycle and rendered-DOM recon are the two things agent browser checks most often get wrong, and both are handled. It is Apache-2.0 by its own folder license even though the container has no root license. Next to [playwright-skill](playwright-skill.md) (stale) it is the maintained choice for scripts. Next to the [playwright](playwright-mcp.md) MCP server and [agent-browser](agent-browser.md) it is a script-first alternative to driving a browser through tool calls. For writing a real `@playwright/test` suite, [playwright-best-practices](playwright-best-practices.md) is the better fit. It wasn't exercised, and its container is itself only a `discovery-log` lead, so it gets no real verdict until a hands-on A/B against the MCP route.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [webapp-testing](https://github.com/anthropics/skills/tree/main/skills/webapp-testing) | skill | Anthropic skill: Python Playwright scripts plus a multi-server lifecycle helper for testing local web apps | Agents can't reliably start a dev server, wait for it, and inspect the rendered UI to verify frontend changes | playwright-skill, playwright, agent-browser, chrome-devtools-mcp, playwright-best-practices |
