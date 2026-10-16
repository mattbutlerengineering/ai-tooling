# Evaluation: browser-use

**Repo:** [browser-use/browser-use](https://github.com/browser-use/browser-use)
**Stars:** 107,900 | **Last updated:** 2026-08-05 | **License:** MIT
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Catalog one-liner: "AI browser agent for autonomous web interaction" — solves "Need agents to navigate and interact with web pages autonomously."

The catalog files browser-use as an "MCP server," but that undersells what it actually is. browser-use is primarily a **Python agent framework** for building autonomous, LLM-driven browser agents. You hand it a natural-language task ("Find the number of stars of the browser-use repo") and an LLM; the agent then plans and executes a multi-step loop — read page state, decide the next action, click/type/navigate, observe, repeat — until it judges the task complete. As of 0.13 the action loop runs on a Rust core ("Python API -> Rust core -> Browser harness -> Web task done") with recovery loops inspired by coding agents. It ships three usage surfaces relevant to a Claude Code dev loop:

1. **Library** (`from browser_use.beta import Agent`) — build your own autonomous web agents. This is the product's center of gravity.
2. **Stateful CLI** (`browser-use open/state/click/type/screenshot/close`) — keeps a browser alive between commands for fast iteration; agent drives discrete actions by element index.
3. **Claude Code skill** (curl the `SKILL.md` into `~/.claude/skills/browser-use/`) — the most direct way to use it inside a Claude Code Verify loop.

MCP is offered as one more integration ("custom tools, MCP, and more on our Docs"), so the catalog's "MCP server" type is technically available but is not how most people use it. The defining characteristic for evaluation purposes is **autonomy**: browser-use is goal-driven (you give intent, the LLM figures out the steps), whereas Playwright MCP is action-driven (you specify each step) and agent-browser is intent-per-action.

There is a heavily-promoted hosted **Cloud** offering (stealth browsers, proxy rotation, CAPTCHA solving, 1000+ integrations) layered on top of the OSS core; the OSS library is MIT and free, but production scaling is steered toward the paid cloud.

**Correction from the 2026-10-16 run:** the installed 0.13.11 package's `browser-use` command is no longer the `open/state/click/type` indexed CLI described above. It is a thin wrapper over `browser-harness` 0.1.13: a Python snippet on stdin with pre-imported CDP helpers (`new_tab`, `fill_input`, `js`, `wait_for_element`, `capture_screenshot`, ...) drives a Chrome/Chromium the daemon attaches to. The autonomous loop is the separate `browser_use.Agent` library class.

## How we tested it

**Evidence:** MEASURED

**Hands-on, measured.** Installed `browser-use` 0.13.11 from PyPI into a fresh venv and drove a local Chromium 141 (headless, `--remote-debugging-port=9222`) through the `browser-use` stdin harness. Fixture: a 40-line Python HTTP server on 127.0.0.1:8765 serving a login form; it logs every POST body and answers `Welcome alice` only for `alice`/`s3cret`, otherwise `Denied`. Task: open the page, fill both fields, submit, read `#msg`. Oracle: the server-side POST log (exact credentials received) plus the text of `#msg`. Baseline arm: the same task as a 12-line Playwright script attached to the same Chromium over CDP; treatment arm: a 9-line `browser-use` harness script.

```
$ browser-use <<'PY'   # treatment (bu_task.py)
new_tab("http://127.0.0.1:8765/"); wait_for_load()
fill_input("#user","alice"); fill_input("#pw","s3cret")
js("document.querySelector('#go').click()")
wait_for_element("#msg", timeout=10); wait_for_load()
print("RESULT", js("document.querySelector('#msg').textContent"))
PY
RESULT Welcome alice            # server.log: {"user":["alice"],"pw":["s3cret"]}

arm  correct/10   median wall-clock (s, incl. process start)
pw   10/10        1.127  (min 1.007, max 1.490)
bu   10/10        1.002  (min 0.732, max 60.809)   # first pass, one 60.8s run
bu sequential re-run, wrong password x10: 10/10 correct, 7 of 10 took 60.8-61.5s, 3 took 0.81-0.93s
bu three further instrumented runs: INSCRIPT 0.76-0.83s, total 1.08-1.20s
```

Across the 23 sequential `browser-use` runs every result and every POST body was correct (23/23); 8 of 23 took about 61 seconds, and the 15 fast runs had median 0.98s (min 0.73, max 1.20). Per-step timing of a fast run: `new_tab` 0.04s, `fill_input` 0.04-0.11s each, `wait_for_element` 0.3-0.9s.

## Test design

- **Task / corpus:** one login-form task, two credential sets (valid, invalid), 5 runs each per arm in the main A/B (20 runs), plus 13 extra harness runs. The fixture is described above and rebuilds in a few lines.
- **Baseline:** Playwright `connect_over_cdp` to the same browser, same task, same selectors.
- **Metric:** correctness (server-side POST log equals the intended credentials and `#msg` text matches) and wall-clock per invocation including interpreter start.
- **Reproduce:** `pip install browser-use playwright`, start Chromium with `--remote-debugging-port=9222`, run the server, set `BU_CDP_URL=http://127.0.0.1:9222`, pipe the snippet into `browser-use`.

## What worked

- **The CDP harness matched Playwright on a scripted form task.** 23/23 correct, and the fast runs' median (0.98s) sat below Playwright's 1.13s, with a 9-line script against 12.
- **Zero-config attach.** With `BU_CDP_URL` set, the daemon connected to an already-running Chromium on the first call; helpers such as `fill_input` (framework-safe typing) and `wait_for_element` behave as documented.
- **Ecosystem and licence** per repo-metadata: MIT, about 107.9K stars, last push 2026-08-05, not archived.

## What didn't work or surprised us

- **Intermittent 61-second stalls.** 8 of 23 sequential harness runs spent about 61s before returning, although the result printed correctly and the same script took 0.8s in other runs. A run launched concurrently with another failed with `Cannot read properties of null` because both shared the daemon's attached tab. Three clean instrumented re-runs afterwards did not reproduce the stall, so the cause is unconfirmed. The harness also never closed its tabs (38 page targets had accumulated in the browser), a candidate cause that was not isolated. Playwright had no stall in 10 runs.
- **The autonomous agent, the product's headline, was not run.** `ChatBrowserUse()` raises `ValueError: BROWSER_USE_API_KEY is not set`, and this sandbox has no model credentials, so the goal-driven loop, its cost per step and its determinism are unmeasured. The earlier cost and non-determinism concerns remain reasoning, not data.
- **The CLI described in the earlier review is gone.** Version 0.13.11 ships the stdin harness instead of `open/state/click`.
- **Install weight.** The venv was 346 MB (108 packages) against 171 MB for Playwright.
- **Single fixture, one browser, five runs per cell** in the main A/B; no third-party sites, CAPTCHA or stealth claims tested.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | 23/23 harness runs matched the server-side oracle, same as Playwright's 10/10; autonomous planning accuracy unmeasured |
| Speed | neutral / - | Fast runs median 0.98s vs Playwright 1.13s, but 8 of 23 runs stalled about 61s |
| Maintainability | neutral | 9-line script vs 12; the package surface changed between the reviewed version and 0.13.11 |
| Safety | neutral | Attaches to whatever browser the CDP URL exposes; the domain allowlist was not exercised |
| Cost Efficiency | neutral | Harness path needs no LLM; the agent path's token cost is unmeasured |
| Verifiability | neutral | Output is plain text plus a screenshot checkable against a server log; the harness has no built-in assertion layer |

## Verdict

**discovery-log — tentative read** — the scripted CDP harness matched Playwright on correctness (23/23) and fast-run speed (0.98s vs 1.13s median) but stalled about 61s in 8 of 23 runs with an unconfirmed cause, and the autonomous Agent loop that defines the product needs an API key unavailable here, so no verdict-grade read of its stated job exists. The earlier conclusion (redundant with Playwright MCP and agent-browser for deterministic UI verification, additive only for genuinely autonomous web tasks) is unchanged by this run.

## Triage note

Re-run 2026-10-16 by the eval-runner routine at Evidence MEASURED for the harness surface only. A human with a model key could run the `Agent` arm against the same fixture to settle the verdict; this lane may not.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [browser-use](https://github.com/browser-use/browser-use) | framework | Autonomous LLM-driven browser agent for goal-based web tasks | Agent must complete under-specified, multi-step web tasks without scripted steps | playwright, agent-browser, chrome-devtools-mcp |
