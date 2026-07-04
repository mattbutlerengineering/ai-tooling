# Evaluation: Kaku

**Repo:** [tw93/Kaku](https://github.com/tw93/Kaku)
**Stars:** 5,423 | **Last updated:** 2026-06-18 (pushed; created 2026-02-07) | **License:** MIT (README/LICENSE.md; GitHub API reports NOASSERTION)
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Cross-cutting environment — the terminal you run coding agents *in*, not a stage participant; light Implement/Verify conveniences via its AI panel
**Layer:** Infrastructure (a macOS terminal emulator — a deeply customized WezTerm fork in Rust)

---

## What it does

The catalog one-liner: "A fast, out-of-the-box terminal built for AI coding." Kaku (書く, "to write") is a **fork of WezTerm** that ships opinionated zero-config defaults (JetBrains Mono, macOS font rendering, dark/light auto-switch, curated zsh plugins, copy-on-select, clickable paths, pane broadcast) plus a 40%-smaller stripped binary and faster startup. It keeps full WezTerm Lua-config compatibility, so it's a drop-in with better defaults rather than a new config surface.

Its AI-specific layer is a built-in assistant (`Cmd+Shift+A`): **error recovery** (on a failed command it suggests a fix you apply with `Cmd+Shift+E`), **natural-language-to-command** (type `# <description>` and it injects the resulting shell command for review), and an **AI Tools config page** that manages settings for Claude Code, Codex, Gemini CLI, Copilot CLI, Kimi Code, etc. It is the code-writing member of the author's trilogy — Kaku (writes code / terminal), [Waza](https://github.com/tw93/Waza) (drills engineering-habit skills), Kami (ships docs).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** Kaku is a macOS-only desktop app (DMG / `brew install tw93/tap/kakuku`); it was not installed and no AI panel or command was exercised. Claims below come from the repository (GitHub metadata, README, file tree, commit/release counts), not observed behavior. The performance table (40% smaller binary, ~100ms shell bootstrap) is the author's self-reported methodology, not measured here.

```bash
gh api repos/tw93/Kaku --jq '{desc,stars:.stargazers_count,pushed:.pushed_at,created:.created_at,license:.license.spdx_id,lang:.language}'
gh api repos/tw93/Kaku/readme --jq '.content' | base64 -d
gh api "repos/tw93/Kaku/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/tw93/Kaku/releases --jq 'length'   # 18
```

## What worked

- **Genuinely well-maintained.** 5.4k★ / 273 forks, **18 tagged releases**, Apple-notarized builds, CI (audit/build-validation/checks), `CLAUDE.md`/`AGENTS.md` and bundled maintainer skills — strong release discipline, consistent with the author's Waza repo.
- **Zero-config quality-of-life.** Sensible defaults out of the box (fonts, theme-awareness, clickable paths, lazygit/yazi hotkeys) lower the setup tax of running terminal coding agents.
- **AI conveniences are practical, not gimmicky.** Error-recovery suggestions and `# nl→command` are small but real time-savers at the prompt; the AI Tools config centralizes provider setup for Claude Code / Codex / Gemini / Copilot.
- **WezTerm-compatible.** Existing WezTerm Lua config works unchanged — low switching cost for that userbase.

## What didn't work or surprised us

- **It's a terminal emulator, not a dev-loop tool.** Kaku is the *environment* you run agents in; it doesn't plan, implement, verify, review, or ship — it doesn't move the catalog's quality signals except marginally via prompt-level AI helpers. This is the core scope caveat.
- **macOS-only.** No Linux/Windows; immediately out of scope for a large share of developers.
- **Overlaps the whole terminal-emulator field.** WezTerm (its upstream), Ghostty, iTerm2, Warp (which has far deeper AI integration) all compete; Kaku's edge is curated defaults + a light AI panel, not a category-defining capability.
- **License metadata mismatch.** README/LICENSE.md say MIT but the GitHub API returns NOASSERTION — minor, but worth confirming before redistribution.
- **AI features depend on your own provider keys/models** and are conveniences layered on the terminal, not an agent harness — don't confuse it with opencode/goose/gemini-cli (those *are* the agent; Kaku just hosts them).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / + | Error-recovery suggestions can fix a failed command, but Kaku doesn't touch code correctness in the loop. |
| Speed | + | Faster startup, curated hotkeys (lazygit/yazi), and `# nl→command` shave small amounts of terminal friction. |
| Maintainability | neutral | A terminal emulator has no bearing on your codebase's maintainability. |
| Safety | neutral | NL→command and error-recovery inject commands for *review* before running; standard terminal trust model. |
| Cost Efficiency | neutral | Free/open; AI features spend your own provider tokens. |

## Verdict

**CONDITIONAL** — adopt if you're on macOS and want a polished, zero-config WezTerm-compatible terminal pre-tuned for running coding agents, and you value the small built-in AI conveniences. It is well-built and actively maintained, but it is *infrastructure you run agents inside*, not a tool that intervenes in the dev loop — so it earns a catalog row as the environment layer, not as a quality-signal mover. Skip it if you're not on macOS or are happy with your current terminal; the AI panel is a nicety, not a reason to switch on its own.

Compared to neighbors: its sibling **Waza** (CONDITIONAL) is a *skill* suite that does intervene in the loop (think/check/hunt); Kaku is the terminal beneath it. Against agent CLIs like **gemini-cli / opencode / goose**, Kaku is orthogonal — it *hosts* them rather than competing. The honest framing is "a better terminal for AI coders," not "an AI coding tool."

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Kaku](https://github.com/tw93/Kaku) | tool | Zero-config WezTerm fork (macOS) tuned for AI coding — built-in AI panel (error recovery, `# nl→command`), agent-tool config for Claude Code/Codex/Gemini, faster/smaller binary | Want a polished, out-of-the-box terminal for running coding agents without hand-tuning WezTerm | Waza & Kami (same trilogy); hosts gemini-cli/opencode/goose rather than competing |
