# Evaluation: ccstatusline

**Repo:** [sirmalloc/ccstatusline](https://github.com/sirmalloc/ccstatusline)
**Stars:** 10,981 | **Last updated:** 2026-06-17 | **License:** MIT
**Dev loop stage:** Plan (situational awareness across all stages)
**Layer:** Infrastructure

---

## What it does

A highly customizable status line formatter for the Claude Code CLI. It renders model name, git branch/status, context-window usage, token counts, session cost, usage limits, block timers, and dozens of other widgets into Claude Code's native single-line `statusLine` slot, with Powerline rendering, themes, gradients, and multi-line layouts.

The mechanism is the standard Claude Code `statusLine` stdin-to-stdout contract: Claude Code spawns the command (`npx -y ccstatusline@latest`, `bunx`, or a pinned global `ccstatusline`) and pipes a JSON payload (model, token metrics, context window size, cost, session data) on stdin; ccstatusline parses that payload plus the session transcript JSONL and, for usage/limit widgets, makes a direct call to Anthropic's usage API. It then prints a fully styled ANSI string back to stdout, which Claude Code displays beneath the prompt. Configuration is done through an interactive React/Ink TUI (launched by running the package), which writes widget layout and colors to `~/.config/ccstatusline/settings.json` and installs the `statusLine` command into Claude Code's `settings.json`. Written in TypeScript, runs on both Node and Bun.

## How we tested it

**Evidence:** REVIEW

Inspected the repository metadata, full README (416 lines including the complete changelog through v2.2.22), and npm registry stats. Did NOT install or run hands-on — the user already runs a custom GSD statusline (`~/.claude/hooks/gsd-statusline.js`) in the sole `statusLine` slot, and Claude Code supports only one statusline command, so installing ccstatusline would displace it. This is an architecture-and-evidence review, consistent with the calibration `claude-hud.md` evaluation (which is in the same statusline category and also not hands-on installed).

```
gh api repos/sirmalloc/ccstatusline --jq '{stars,license,description,pushed_at,forks,open_issues}'
# stars 10981, license MIT, forks 475, open_issues 83, pushed_at 2026-06-17

curl -s "https://api.npmjs.org/downloads/point/last-month/ccstatusline"
# downloads 184964 (2026-05-20 .. 2026-06-18)

gh api repos/sirmalloc/ccstatusline/readme --jq '.content' | base64 -d   # full README
```

## What worked

- **Native data source**: reads Claude Code's own statusline JSON metrics (token counts, context window size, model, cost) rather than estimating. Recent versions explicitly prefer cumulative transcript metrics and dedupe streaming JSONL entries for accurate token counts.
- **Genuine context awareness**: Context %, Context Bar, Context Window, and Compaction Counter widgets surface context pressure inline — the load-bearing dev-loop signal a statusline can provide. Handles `[1m]` / 1M-context models correctly.
- **Cost and usage visibility**: Session Cost widget (Claude Code 1.0.85+), plus Session Usage, Weekly Usage (split by Sonnet/Opus to match `/usage`), Extra Usage overage widgets, and Block/Weekly Reset Timers — real-time spend and rate-limit awareness without leaving the prompt.
- **Deep git integration**: ~25 git widgets (branch, staged/unstaged/untracked counts, ahead/behind, conflicts, SHA, PR/MR with clickable links for GitHub + GitLab, worktree mode/name). Output is cached under `~/.cache/ccstatusline/git-cache` with mtime checks and `--no-optional-locks` to avoid `index.lock` races — thoughtful for repeated subprocess work on every render.
- **Maturity signals are strong**: ~185K npm downloads/month, 10.9K stars, 475 forks, pushed 2 days before evaluation, 83 open issues against a fast release cadence (v2.2.22). Listed in Awesome Claude Code. npm provenance attestations + trusted publishing.
- **Safer config handling**: invalid `settings.json` is left untouched, defaults render in memory, and an invalid-config warning shows in the line rather than crashing or corrupting user config.
- **No-install usage**: runs via `npx`/`bunx` with zero global footprint, or a pinned global install for version stability — sensible for a tool invoked on every render.

## What didn't work or surprised us

- **Single statusLine slot**: Claude Code exposes exactly one `statusLine` command. Installing ccstatusline replaces any existing statusline (GSD, claude-hud, custom scripts). There is no composition with other statusline tools — it is mutually exclusive with claude-hud.
- **Per-render subprocess cost**: with `npx -y ...@latest` as the command, every render risks an npx resolution overhead; the pinned global install and git cache mitigate this, but the default `@latest` invocation is the slower path. Configurable `refreshInterval` (Claude Code >=2.1.97) helps throttle.
- **Usage widgets make a network call**: the Session/Weekly/Extra usage widgets call Anthropic's usage API directly (honoring `HTTPS_PROXY`). This is more network surface than a purely local statusline; cost/limit accuracy is the tradeoff. Most widgets (context, git, cost, model) are fully local.
- **Configuration breadth is large**: dozens of widgets, color modes (16/256/truecolor/gradients), Powerline caps, flex separators, minimalist mode. Powerful but a deep TUI — the "Zero Config" default is the right entry point; full customization is a time sink.
- **Not hands-on tested**: verdict rests on architecture review plus very strong adoption metrics, not a local install.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Context %/bar/compaction widgets surface context pressure inline, helping avoid work in degraded context; reads native token metrics, not estimates |
| Speed | + | Inline git/PR state and usage/reset timers reduce context-switching to run `/context`, `git status`, `/usage`; reset timers prevent surprise throttling |
| Maintainability | neutral | No effect on the codebase being worked on |
| Safety | neutral | Mostly local; usage widgets make a direct Anthropic API call (opt-in by adding the widget); invalid-config is handled defensively, not corrupted; MIT, npm provenance |
| Cost Efficiency | + | Session Cost + Session/Weekly/Extra usage widgets give real-time spend and quota visibility inline |

## Verdict

**CONDITIONAL**

Adopt when you want a polished, visual statusline (Powerline, themes, gradients, deep git widgets) and you don't already run a statusline you prefer — it occupies the single `statusLine` slot, so it's an either/or choice with claude-hud or a custom statusline. A statusline is more than cosmetic here: the context %/bar, compaction counter, session cost, and usage/reset-timer widgets deliver real outer-loop situational awareness that reduces command round-trips and prevents working in degraded context or hitting surprise rate limits. ccstatusline is the most mature, widely adopted (~185K downloads/month) tool in this niche, but its value is roughly equivalent to claude-hud's (both read the same native data); pick by aesthetic preference (ccstatusline = Powerline/visual polish; claude-hud = denser multi-line HUD). It is complementary to abtop (ADOPT), which monitors sessions from *outside* the agent — ccstatusline lives inside the single CC session's prompt. The user's existing GSD statusline already fills this slot, so for this environment it is a "evaluated, not adopted because the slot is taken" CONDITIONAL.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ccstatusline](https://github.com/sirmalloc/ccstatusline) | plugin | Highly customizable Claude Code statusline — context %, tokens, cost, usage limits, deep git widgets, Powerline themes | Want a richer, configurable status display (context pressure, cost, git, limits) without running commands | claude-hud, claude-code-templates, abtop |
