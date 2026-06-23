# Evaluation: Claude Fleet

**Repo:** [tianyilt/claude-fleet](https://github.com/tianyilt/claude-fleet)
**Stars:** 34 | **Last updated:** 2026-06-16 (pushed; created 2026-05-30) | **License:** MIT
**Dev loop stage:** Outer loop / Observability (monitoring parallel agent sessions; touches Implement by helping you triage which session to attend to)
**Layer:** Tooling (local Python web dashboard + optional signed macOS app)

---

## What it does

Claude Fleet is a **local, read-only dashboard for watching many concurrent Claude Code / Codex windows at once** — "who's stuck, who's waiting on you, who's done." It runs as a local web app (`bash run.sh` → `http://127.0.0.1:7878`, auto-creates a venv) or a signed double-clickable macOS `.app`; the dashboard, history, search, and monitoring are cross-platform (Windows/Linux too).

Unlike the session *managers* (claude-squad, agent-of-empires) it doesn't spawn or drive agents — it **observes the transcripts they already write**. Its three pillars:
- **Triage classification.** A patrol engine reads each transcript's `stop_reason`, `queue-operation` events, and background-task state to assign a status — 🟢 working / 🔴 waiting (permission prompt open) / 🟡 stalled (`tool_use` + idle >5 min) / 🔵 completed (`end_turn` + idle >5 min) / ⚪ closeable (completed + idle >1 h). Background tasks (`Bash run_in_background`, persistent `Monitor`) are tracked by pairing tool_use/tool_result so they aren't misread as "working." A persistent red bar surfaces missed permission prompts; click to jump back to that terminal.
- **Full-text transcript search.** ripgrep across all Claude + Codex transcripts in ~50 ms, matching conversation *content* (not just titles), with up to 3 match-context snippets per hit.
- **Skill / memory analytics.** Counts skill usage across three dimensions (formal `/invoke` + Read/Write/Edit of skill files + Bash references to `skills/`), and shows per-memory in/out-degree (sessions that read vs. wrote it).

Resume/Fork open a real terminal (macOS `open -a`; Linux gnome-terminal/kitty/wezterm/…; Windows copies the `claude --resume` command to clipboard). **Focus** (raising the owning tab) is macOS-only via AppleScript.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No dashboard launched, no sessions observed. Claims come from the repository (GitHub metadata, README feature tables, screenshots described) — the project's own documentation, not observed behavior.

```bash
gh api repos/tianyilt/claude-fleet --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/tianyilt/claude-fleet/readme --jq '.content' | base64 -d   # triage state machine, search, analytics
```

## What worked

- **Triage state machine is the differentiator.** Deriving status from `stop_reason` + queue events + tool_use/tool_result pairing (not a naive busy/idle flag) is a genuinely better answer to "which of my 7 windows needs me *right now*?" The "closeable" state and missed-permission red bar are practical touches.
- **Read-only by design = low risk.** It only reads on-disk transcripts and never drives agents, so it composes alongside whatever session manager you already use — no lock-in, minimal trust surface.
- **Fast content search across all transcripts** (~50 ms ripgrep, content not titles) directly solves "find that session from last week," a real recurring pain.
- **Skill/memory analytics are unusually thoughtful.** Counting informal skill usage (file reads + bash refs, not just `/invoke`) and memory in/out-degree is a feedback signal most tools don't surface — useful for pruning unused skills.
- **Zero-setup, cross-platform, MIT.** 30-second first run, signed Mac app, Windows/Linux fallbacks.

## What didn't work or surprised us

- **Very young and tiny.** 34 stars, created late May 2026 — minimal social proof and unproven longevity; a one-maintainer project.
- **Read-only, so it's a complement, not a replacement.** It doesn't manage sessions; you still need claude-squad / agent-of-empires / tmux to *run* them. Value is purely the monitoring/triage layer.
- **Tightly coupled to Claude Code / Codex transcript formats.** The triage logic depends on specific `stop_reason` / queue-event shapes; format changes upstream could silently break classification, and other agents aren't covered.
- **Mac-favored.** Focus is macOS-only; full polish (signed app, LaunchServices Resume/Fork) is best on Mac, with clipboard fallbacks elsewhere.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Surfacing waiting/stalled sessions and missed permission prompts means fewer agents silently stuck on a bad path; doesn't change agent output itself. |
| Speed | + | At-a-glance triage + ~50 ms transcript search removes the "check each window" tax of multi-session work. |
| Maintainability | neutral | Affects your monitoring workflow, not your codebase. |
| Safety | + | Read-only (reads transcripts, never drives agents) — minimal trust surface; runs locally on 127.0.0.1. |
| Cost Efficiency | + / neutral | Free/MIT; skill/memory analytics can guide pruning, but it doesn't track token spend (see codeburn for that). |

## Verdict

**CONDITIONAL** — adopt if you routinely run 5+ Claude Code/Codex windows and want a lightweight, read-only command center to see who's waiting/stalled/done plus fast cross-transcript search, *on top of* whatever runs your sessions. The triage state machine and skill/memory analytics are genuinely well thought out and the read-only design makes it safe to bolt on. Hold off if you run one or two agents (the dashboard is overkill), want one tool that both runs *and* monitors sessions (use agent-of-empires/claude-squad), or need maturity — it's brand new and small.

Compared to neighbors: **abtop** is the closest — a real-time TUI monitor of agent sessions (tokens/context/rate-limits) — where Claude Fleet is a web dashboard centered on *triage + transcript search + skill/memory analytics*; **codeburn** focuses on *cost* attribution; the session *managers* drive agents rather than observe them. Claude Fleet is the read-only **triage + search** layer of the multi-session stack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-fleet](https://github.com/tianyilt/claude-fleet) | tool | Local read-only dashboard for many concurrent Claude Code/Codex windows — triage state machine (working/waiting/stalled/completed/closeable), ~50ms ripgrep transcript search, skill/memory usage analytics | Running 5–7 agent windows, you miss permission prompts and can't tell who's stuck, waiting, or done — or find last week's session | abtop, codeburn, agent-of-empires |
