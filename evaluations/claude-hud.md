# Evaluation: claude-hud

**Repo:** [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud)
**Stars:** 27,586 | **Last updated:** 2026-08-18 (last push) | **License:** MIT
**Last verified:** 2026-08-23
**Dev loop stage:** Plan (situational awareness during all stages)
**Layer:** Infrastructure

---

## What it does

A Claude Code plugin that replaces the default status line with a rich HUD showing context window usage, active tools, running subagents, todo progress, git status, model info, usage limits, cost tracking, prompt cache countdown, and session duration. Uses Claude Code's native `statusLine` API — no tmux or separate window required.

The architecture is a **stdin-to-stdout pipe**: Claude Code sends a JSON payload with token counts and rate limits, claude-hud parses that plus the session transcript JSONL for tool/agent/todo activity, and writes a colour-coded multi-line display to stdout. 60 TypeScript source files, 34 test files, configurable via `/claude-hud:configure` or by editing `<claude-config-dir>/claude-hud.json` directly.

## How we tested it

**Evidence:** RUN

Exercised hands-on by **feeding synthetic statusline payloads to the built binary** — the technique the previous review did not consider. That review declined to install it *"because the user has a custom GSD statusline (`~/.claude/hooks/gsd-statusline.js`) already occupying the `statusLine` slot"*, and that reasoning does not survive contact with the architecture: claude-hud is a program that reads JSON on stdin and writes text on stdout. Testing it needs neither the `statusLine` slot nor a Claude Code session, and the repo ships a `test:stdin` script that says so. **Nothing was installed and nothing in the real `~/.claude` was read or written** — the config probes ran against a scratch `HOME`, and all payloads are fabricated (`/tmp/probe-project`, invented token counts), so no real session data appears here.

**Version under test: `claude-hud` 0.8.0**, commit `ef5f1c8` (2026-08-18).

```bash
git clone --depth 1 https://github.com/jarrodwatts/claude-hud.git
npm install && npm run build          # 2 s
cat probe/payload.json | node dist/index.js
npm test                              # its own suite
HOME=<scratch> node dist/index.js     # config surface, real ~/.claude untouched
```

**1. It runs, and the colour bands work.** A payload at 12% context renders a green bar; the same payload at 76% renders yellow; at the fallback-computed 93%, red. Exit code 0 throughout. Build is **2 s** with **zero runtime dependencies** (devDeps are only `typescript`, `c8`, `@types/node`) — for a program Claude Code executes on every render, that is a supply-chain fact worth stating.

**2. The headline accuracy claim needs one qualifier, and it is measurable.** The previous review said the HUD *"reads Claude Code's actual token counts and rate limits from stdin, not estimates — accuracy is inherent to the data source."* True **when Claude Code sends `context_window.used_percentage`** (v2.1.6+). When it does not, `getBufferedPercent` derives one, and the two disagree materially. Same tokens (32k fresh + 120k cache = 152k of a 200k window), one field apart:

| Payload | Rendered | Colour |
|---|---|---|
| with `used_percentage: 76` | **76%** | yellow |
| without it (fallback) | **93%** | red |

The gap is deliberate, not a bug: `AUTOCOMPACT_BUFFER_PERCENT = 0.165` is added, scaled from 0 at ≤5% raw usage to full at ≥50%, so the fallback bar answers *"how close to autocompact"* rather than *"how full is the window"*. The fallback also appends a token breakdown (`(in: 32k, cache: 120k)`) the native path omits. Worth knowing before reading the number as ground truth on an older Claude Code.

**3. Its own test suite is real.** `npm test` on a clean checkout: **1,079 tests, 1,073 pass, 0 fail, 6 skipped, 28.7 s.** A measured maintainability signal rather than an inferred one.

**4. The config surface works, and the shape is nested.** `<claude-config-dir>/claude-hud.json` with `{"display": {"showCost": true}}` renders `Cost $3.42` from the payload's `cost.total_cost_usd`. A **top-level** `{"showCost": true}` is silently ignored — the loader reads it, but the key lives under `display`, so a mis-nested option fails quietly rather than erroring. The loader also refuses symlinks and files over a byte cap before parsing, which is sensible hardening for a file that executes on every render.

**Not exercised:** the plugin's two model-invocable commands (`/claude-hud:setup`, `/claude-hud:configure`), the transcript-JSONL path (tools/agents/todos rendering — all probes used a non-existent transcript, deliberately, to avoid reading real sessions), git-status integration, and the prompt-cache countdown. Also unmeasured: per-render latency inside a live session, which is the number that would decide whether a ~300 ms refresh is free.

## Test design

- **Task/corpus:** four synthetic `statusLine` payloads varying only `context_window` (12% / 76% raw / 76% native / 100%), plus three scratch-`HOME` config files.
- **Baseline:** the previous `REVIEW` eval's written claims — the stated install blocker, the "accuracy is inherent to the data source" framing, and the 46-src/25-test file counts — each chosen so the run could refute it.
- **Metric:** rendered percentage and colour band per payload; pass/fail/skip counts from the vendored suite; build wall-clock; file counts.
- **Reproduce:** the command block above. No API key, no Claude Code session, no writes outside a scratch directory.

### Test design — skills

- **Triggering:** **not measured.** The HUD itself is never model-invoked — Claude Code executes it as a `statusLine` command — so triggering does not apply to the component under test. The plugin's two `/claude-hud:*` commands *are* model-invocable and were not exercised.
- **Output A/B:** the native-vs-fallback comparison in finding 2 **is** a with/without A/B on the same input — one field toggled, 17 percentage points and a colour band apart. There is no "with-skill vs baseline" axis for a statusline beyond that.
- Both gaps are stated rather than papered over; nothing here claims a triggering measurement that was not made.

## What worked

- **Testable without installing it.** The stdin→stdout design means the blocker the previous review named was never a blocker. That is a genuine architectural virtue, not just a convenience for this eval.
- **Zero runtime dependencies**, 2 s build, and a 1,073-passing test suite — unusually disciplined for a statusline plugin.
- **Colour-coded context health works as described**, green→yellow→red across the thresholds.
- **Native token data when available**: with `used_percentage` present the HUD reproduces Claude Code's own figure exactly rather than estimating.
- **Config hardening**: symlink refusal and a size cap before parsing, on a file that runs every ~300 ms.
- **Security stance**: local-only, no network requests, `--extra-cmd` disabled by default with explicit opt-in via environment variable (read from source, not exercised).

## What didn't work or surprised us

- **Occupies the sole `statusLine` slot.** Claude Code supports one `statusLine` command, so installing claude-hud replaces any existing statusline (GSD, ccstatusline, custom scripts). No composition mechanism exists — this is the adopt-if gate and it is a hard one.
- **The fallback percentage is not the window percentage.** 17 points and a colour band separate the two paths on identical tokens. Nothing in the HUD marks which path produced the number.
- **Mis-nested config fails silently.** `{"showCost": true}` at the top level is ignored with no error; the key belongs under `display`. Easy to lose an afternoon to.
- **Information overload risk**: the fullest configuration shows far more than most terminals can usefully display alongside the conversation.
- **The transcript-driven half is unmeasured here** — tools, subagents, todos and git status all read the session JSONL, which these probes deliberately did not supply.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Context health bar prevents operating with degraded context — though on pre-v2.1.6 Claude Code the number is an autocompact-buffered estimate, measured 17 points above raw fill |
| Speed | + | Usage-limit visibility prevents surprise throttling; per-render latency in a live session was not measured |
| Maintainability | + | 1,079 tests (1,073 pass, 0 fail) and zero runtime dependencies — measured on a clean checkout, not inferred |
| Safety | + | Local-only, no network, `--extra-cmd` off by default; config loader refuses symlinks and oversized files before parsing |
| Cost Efficiency | + | `display.showCost` renders Claude Code's native `total_cost_usd` (verified: `Cost $3.42`) |
| Verifiability | + | A stdin→stdout program with a documented payload shape is checkable without installing it — which is how every claim above was produced |

## Verdict

**CONDITIONAL** — adopt-if: your Claude Code `statusLine` slot is **free**, or you are willing to give up the statusline currently in it.

That gate is the whole decision and it is not negotiable in configuration: Claude Code exposes exactly one `statusLine` command and claude-hud takes it. For this user the slot is occupied by a GSD statusline, so adopting means choosing between them — which is why the verdict is conditional on a fact about the environment rather than about the tool. The tool itself came through the run well: zero runtime dependencies, a 1,073-passing suite, and behaviour that matches its description.

Two things to know before installing rather than after: on Claude Code older than v2.1.6 the context number is an autocompact-buffered estimate sitting ~17 points above raw window fill, and config options are nested under `display` — a mis-nested key is ignored silently.

Choose **ccstatusline** for a lighter visual-only statusline with Powerline themes. Choose **abtop** (ADOPT) for cross-session monitoring from outside the agent — claude-hud and abtop are complementary (inside vs outside), and only claude-hud competes for the slot.

This replaces a `discovery-log — tentative read` whose stated reason for not running the tool — the occupied `statusLine` slot — turned out not to be a precondition for testing it at all.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | plugin | Rich Claude Code statusline HUD — context health, usage limits, cost, tools, agents, todos (27K stars) | Can't see context pressure, rate limits, or session cost without running commands | ccstatusline, claude-code-templates, abtop |
