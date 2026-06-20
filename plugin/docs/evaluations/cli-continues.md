# Evaluation: continues (cli-continues)

**Repo:** [yigitkonur/cli-continues](https://github.com/yigitkonur/cli-continues)
**Stars:** 1,280 | **Last updated:** 2026-05-07 (pushed) | **License:** MIT | **Language:** TypeScript (npm: `continues`)
**Dev loop stage:** Dev Workflow — cross-tool session handoff
**Layer:** Tooling (CLI, `npx continues`)

---

## What it does

continues **hands off your AI coding session from one tool to another** — "you hit the rate limit mid-debug… now you either wait hours or start fresh in another tool. `continues` grabs your session from whichever AI coding tool you were using and hands it off to another one." It supports **16 agents** (Claude Code, Codex, GitHub Copilot CLI, Gemini CLI, Cursor, Amp, Cline, Roo Code, Kilo Code, Kiro, Crush, OpenCode, Factory Droid, Antigravity, Kimi CLI, Qwen Code) for **any-to-any handoff (240 paths)**. It works by: **discovery** (scan each tool's session directories), **parsing** (read each tool's native format — JSONL/JSON/SQLite/YAML), **extraction** (recent messages, file changes, tool activity, AI reasoning), and **handoff** (generate a structured context doc and inject it into the target tool so the receiving agent immediately understands what you were doing). `npx continues` — no install needed.

## How we tested it

**Source-grounded inspection — not installed, not run.** No session handed off.

```bash
gh api repos/yigitkonur/cli-continues --jq '{stars,license:.license.spdx_id,pushed:.pushed_at}'   # 1280, MIT, pushed 2026-05-07
gh api repos/yigitkonur/cli-continues/readme --jq '.content' | base64 -d | head -45               # 16 tools, 240 paths, discovery/parse/extract/handoff
```

## What worked

- **Solves a real, specific pain.** Rate limits, quota exhaustion, or wanting a second model's take mid-task are common; losing 30 messages of context to start fresh elsewhere is genuinely costly. continues targets exactly that.
- **Any-to-any across 16 tools.** Reading each agent's *native* session format (JSONL/JSON/SQLite/YAML) and normalizing to a handoff doc is real work, and the breadth (240 paths) is impressive.
- **Zero-install, zero-config.** `npx continues` — nothing to set up; it discovers installed tools automatically.
- **Right output shape.** A structured context doc (what you were doing, files touched, commands run, what's left) is exactly what a receiving agent needs to resume coherently.
- **MIT, focused.** Does one thing well.

## What didn't work or surprised us

- **Lossy by nature.** A handoff doc is a *summary* of state, not the live session — the receiving agent resumes from a reconstruction, so nuance/working memory can be lost.
- **Fragile to format changes.** It parses 16 tools' private, undocumented session formats; any tool changing its on-disk format silently breaks that path. Maintenance burden is inherent.
- **Niche utility.** Valuable, but it's a convenience for a specific moment (switch tools mid-task), not an everyday tool — moderate stars (1.3K) reflect that.
- **Trust/scope.** It reads your local session histories across tools (conversations, file changes) — fine locally, but it's touching sensitive transcripts.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Preserves intent/context across tools; a reconstructed doc can drop nuance the live session held. |
| Speed | + | Avoids waiting out a rate limit or re-explaining context in a new tool — resume immediately elsewhere. |
| Maintainability | neutral | For you, frictionless; for the project, parsing 16 private formats is brittle to upstream changes. |
| Safety | neutral | Local-only; reads sensitive session transcripts across tools. |
| Cost Efficiency | + | Switch to a tool/model with available quota instead of burning time or paying for premium overflow. |

## Verdict

**CONDITIONAL** — continues is a focused, MIT utility that solves a real friction: **handing your AI coding session (history + file changes + working state) from any of 16 tools to any other**, zero-install via `npx`. Adopt it if you regularly hit rate limits mid-task or like switching models/tools and don't want to lose context — it's the cleanest cross-tool handoff option around. It's CONDITIONAL because the handoff is a *reconstruction* (inherently lossy) and parsing 16 tools' private session formats is brittle to upstream changes. For occasional use it's a great convenience; don't expect a perfect live-session transfer.

Compared to neighbors: **re_gent** tracks prompt-level provenance of agent changes; **cc-switch** swaps Claude accounts/providers; **storybloq** persists cross-session context within Claude Code. continues' distinguishing pitch is **any-to-any session handoff across 16 different coding agents.**

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cli-continues](https://github.com/yigitkonur/cli-continues) | tool | Cross-tool AI coding session handoff (MIT) — `npx continues` scans 16 agents' native session formats (Claude Code, Codex, Copilot, Gemini, Cursor, Cline, OpenCode, Factory Droid…) and hands conversation history + file changes + working state to another (240 any-to-any paths) | You hit a rate limit or want to switch tools mid-task; don't lose context starting fresh in another agent | re_gent, cc-switch, storybloq |
