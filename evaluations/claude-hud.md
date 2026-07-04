# Evaluation: claude-hud

**Repo:** [jarrodwatts/claude-hud](https://github.com/jarrodwatts/claude-hud)
**Stars:** 25,431 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan (situational awareness during all stages)
**Layer:** Infrastructure

---

## What it does

A Claude Code plugin that replaces the default status line with a rich HUD showing context window usage, active tools, running subagents, todo progress, git status, model info, usage limits, cost tracking, prompt cache countdown, and session duration. Uses Claude Code's native `statusLine` API — no tmux or separate window required.

The architecture is a stdin-to-stdout pipe: Claude Code sends JSON payloads with token counts and rate limits, claude-hud parses those plus the session transcript JSONL for tool/agent/todo activity, and renders a color-coded multi-line display updated every ~300ms. 46 TypeScript source files, 25 test files, 3 presets (Full/Essential/Minimal), configurable via `/claude-hud:configure` interactive flow or direct JSON editing.

## How we tested it

**Evidence:** REVIEW

Architecture review and README analysis. Not hands-on installed because the user has a custom GSD statusline (`~/.claude/hooks/gsd-statusline.js`) already occupying the `statusLine` slot. Evaluated the implementation by reading source structure and configuration surface.

```
gh api repos/jarrodwatts/claude-hud --jq '.stargazers_count, .updated_at, .license.spdx_id'
# 25431, 2026-06-19T04:31:39Z, MIT
```

## What worked

- **Native token data**: reads Claude Code's actual token counts and rate limits from stdin, not estimates — accuracy is inherent to the data source
- **Context health visualization**: color-coded bar (green → yellow → red) with configurable thresholds gives immediate read on context pressure without running `/context`
- **Prompt cache countdown**: shows live TTL since last response — unique feature for optimizing response timing around the 5-minute cache window
- **Usage limit tracking**: subscriber rate limits (5h window + 7-day window) with remaining time and percentage — prevents surprise throttling
- **Cost display**: uses Claude Code's native `cost.total_cost_usd` when available, local transcript estimate as fallback
- **Comprehensive configurability**: 60+ options covering colors, thresholds, layout, element ordering, language (en/zh), and 3 presets — unusually thorough for a statusline plugin
- **Security stance**: local-only, no network requests, `--extra-cmd` disabled by default with explicit opt-in via environment variable

## What didn't work or surprised us

- **Occupies sole statusLine slot**: Claude Code only supports one `statusLine` command — installing claude-hud replaces any existing statusline (GSD, ccstatusline, custom scripts). No composition mechanism exists.
- **Information overload risk**: Full preset shows 10+ lines of data — more than most terminals can usefully display alongside the conversation. Essential or Minimal presets are the pragmatic choice.
- **Not hands-on tested**: evaluation is architecture-review-based. The 25K stars and active community (multiple forks for DeepSeek, GLM, enhanced themes) suggest it works well in practice.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Context health bar prevents operating with degraded context; prompt cache timing improves response quality |
| Speed | + | Usage limit visibility prevents surprise throttling; prompt cache countdown enables timing optimization |
| Maintainability | neutral | No effect on code quality |
| Safety | neutral | Local-only, no network; extra-cmd disabled by default |
| Cost Efficiency | + | Cost display and usage tracking provide real-time spending visibility |

## Verdict

**CONDITIONAL**

Use when you want rich context/usage/cost visibility and don't already have a statusline you prefer. The context health bar and prompt cache countdown are genuinely useful for session management. Choose ccstatusline (10.9K stars) if you want a lighter visual-only statusline with Powerline themes. Choose abtop (ADOPT) if you want cross-session monitoring from outside the agent — claude-hud and abtop are complementary (inside vs outside).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-hud](https://github.com/jarrodwatts/claude-hud) | plugin | Rich HUD for Claude Code — context health, usage limits, cost, tools, agents, todos, prompt cache | Can't see context pressure, rate limits, or session cost without running commands | ccstatusline, abtop |
