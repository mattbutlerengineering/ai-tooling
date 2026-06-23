# Evaluation: Claudian

**Repo:** [YishenTu/claudian](https://github.com/YishenTu/claudian)
**Stars:** 12,963 | **Last updated:** 2026-06-18 (pushed; created 2025-12-05) | **License:** MIT | **Releases:** 30
**Dev loop stage:** Implement / cross-cutting (an agent host inside Obsidian; also Plan via Plan Mode)
**Layer:** Tooling (TypeScript Obsidian plugin; desktop)

---

## What it does

Claudian is an **Obsidian plugin that embeds AI coding agents (Claude Code, Codex, Opencode, Pi) directly in your vault** — your vault becomes the agent's working directory, so file read/write, search, bash, and multi-step workflows all work against your notes out of the box. It turns the agent's terminal experience into a native Obsidian sidebar + inline-edit surface.

Feature set is mature for a plugin:
- **Inline Edit** — select text (or start at cursor) + hotkey to edit directly in a note with **word-level diff preview**.
- **Slash commands & Skills** (`/`, `$`) — reusable prompt templates and Skills at user- and vault-level scope.
- **`@mention`** — pull in vault files, subagents, MCP servers, or external-directory files.
- **Plan Mode** (`Shift+Tab`) — explore/design before implementing, then present a plan for approval.
- **Instruction Mode** (`#`) and refined custom instructions from chat input.
- **MCP servers** (stdio/SSE/HTTP) — Claude-managed in-app; Codex uses its own CLI config.
- **Multi-tab conversations** with history, fork, resume, and compact.

Requirements: the relevant agent CLI installed (Claude Code CLI for the Claude provider; Codex/Opencode/Pi optional), a provider subscription/API (or compatible providers like OpenRouter/Kimi), Obsidian 1.7.2+, desktop only.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No plugin installed, no vault session. Claims come from the repository (GitHub metadata, README feature list, requirements, 30 releases) — the project's own documentation, not observed behavior.

```bash
gh api repos/YishenTu/claudian --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/YishenTu/claudian/readme --jq '.content' | base64 -d   # features, providers, requirements
gh api repos/YishenTu/claudian/releases --jq 'length'             # 30
```

## What worked

- **Meets a real population where they already work.** Many people live in Obsidian for notes, docs, and PKM; making the vault an agent workspace (with all file/search/bash tools) is a genuinely useful host that's not "yet another IDE."
- **Mature interaction model.** Inline word-level diff edits, Plan Mode approval, slash/skills, `@mention`, multi-tab + fork/resume/compact is a complete agent UX — closer to a polished editor integration than a thin wrapper.
- **Multi-provider** (Claude Code, Codex, Opencode, Pi) and MCP support mean it isn't locked to one agent; it's a host, not a vendor front-end.
- **Strong adoption + maintenance.** ~13K stars, 30 releases since Dec 2025, in the official Obsidian community plugin directory — credible traction and upkeep.
- **MIT-licensed.**

## What didn't work or surprised us

- **Best fit is docs/notes/PKM, not large software repos.** The vault-as-working-directory model shines for Markdown knowledge work and small projects; for a big code repo you'd more likely run the agent in a real IDE/terminal. It's an agent host *in Obsidian*, with Obsidian's strengths and limits.
- **Requires the underlying agent CLI + subscription.** It's a front-end, not an agent — quality and cost are entirely the provider's; it adds a layer to install/maintain.
- **Desktop-only.** No mobile Obsidian support.
- **Same trust model as any file/bash agent** — it reads/writes/executes in your vault; treat its permissions like any coding agent's.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | Plan Mode approval + word-level inline diffs give human checkpoints; underlying output quality is the provider's. |
| Speed | + | Agent + vault files + inline edit in one surface removes context-switching for note/doc-centric work. |
| Maintainability | neutral | Affects your authoring workflow, not codebase structure. |
| Safety | neutral | File/bash agent in your vault; standard trust model, with Plan-Mode approval as a gate. |
| Cost Efficiency | neutral | Free/MIT plugin; spends the underlying provider's tokens. |

## Verdict

**CONDITIONAL** — adopt if you work in **Obsidian** and want a polished, multi-provider agent host that treats your vault as the working directory, with inline diff edits, Plan Mode, skills, and MCP. It's mature, popular, actively maintained, MIT, and not locked to one agent — an excellent fit for notes/docs/PKM and small projects. Less compelling if your work is a large code repo (use an IDE/terminal agent) or you're not an Obsidian user. It's a front-end, so cost/quality remain the provider's.

Compared to neighbors: **Nimbalyst** is a standalone Electron workspace; **cc-switch** is a desktop GUI multiplexer for CLI agents; **kilocode** lives in VS Code/JetBrains; AgriciDaniel's **claude-obsidian** is a second-brain *workflow* for Obsidian. Claudian is the **agent-host plugin inside Obsidian** — the most complete way to run coding agents against your vault, distinct from the IDE- and desktop-app hosts.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claudian](https://github.com/YishenTu/claudian) | plugin | Obsidian plugin that embeds Claude Code/Codex/Opencode/Pi in your vault — vault as working dir, inline word-level diff edits, Plan Mode, skills, @mention, MCP, multi-tab | Want to run coding agents against your Obsidian notes/docs without leaving Obsidian for a terminal or IDE | Nimbalyst, cc-switch, kilocode |
