# Evaluation: CC GUI (JetBrains Claude Code / Codex plugin)

**Repo:** [zhukunpenglinyutong/jetbrains-cc-gui](https://github.com/zhukunpenglinyutong/jetbrains-cc-gui)
**Stars:** 4,068 | **Last updated:** 2026-06-17 (pushed; created 2025-11-20) | **License:** MIT | **Releases:** 30
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement (in-IDE agent host; touches all inner-loop stages)
**Layer:** Tooling (TypeScript; IntelliJ/JetBrains plugin via JetBrains Marketplace)

---

## What it does

CC GUI (originally "Claude Code GUI," renamed to mitigate Claude trademark risk) is an **IntelliJ/JetBrains plugin that provides a visual interface for both Claude Code and OpenAI Codex** inside the IDE. It brings the two CLI agents into a native JetBrains panel with IDE-aware affordances.

Key features per the README:
- **Dual AI engine** — Claude Code (Opus 4.5 etc.) and OpenAI Codex.
- **IDE-aware chat** — context-aware assistant, **`@file` references** for precise context, **image sending** for visual requirements, **conversation rewind** to adjust history, enhanced prompts.
- **Agent system** — built-in agents for automated complex tasks, a **Skills slash-command system** (`/init`, `/review`, …), and **MCP server support**.

The maintainer notes a security posture: a `/security-review` audit before each minor release and a comprehensive `claude-code-security` audit every 10 minor versions.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No plugin installed in a JetBrains IDE, no session. Claims come from the repository (GitHub metadata, README feature list, Marketplace link, 30 releases) — the project's own documentation, not observed behavior.

```bash
gh api repos/zhukunpenglinyutong/jetbrains-cc-gui --jq '{stars,created_at,pushed_at,license:.license.spdx_id,lang:.language}'
gh api repos/zhukunpenglinyutong/jetbrains-cc-gui/readme --jq '.content' | base64 -d   # dual-engine, features, rename, audits
gh api repos/zhukunpenglinyutong/jetbrains-cc-gui/releases --jq 'length'              # 30
```

## What worked

- **Fills a real IDE gap.** Claude Code and Codex are terminal-first; a native JetBrains GUI (IntelliJ, PyCharm, WebStorm, etc.) brings them to a large IDE population that wants visual chat + `@file` context without leaving the editor.
- **Dual-engine in one panel.** Hosting both Claude Code and Codex side-by-side is convenient and avoids committing to one agent.
- **Thoughtful IDE affordances.** `@file` references, image input, conversation rewind, and skills slash-commands are genuinely useful editor-integrated features, not just a chat box.
- **Stated security discipline.** Per-release `/security-review` and periodic deep audits are a good sign for a plugin that runs an agent with file/exec access.
- **Active and adopted.** ~4K stars, 30 releases since Nov 2025, published on the JetBrains Marketplace; MIT.

## What didn't work or surprised us

- **It's a front-end, not an agent.** Quality and cost are the underlying Claude Code/Codex CLIs'; it adds a GUI layer to install and keep compatible with both the IDE and the CLIs.
- **JetBrains-only.** No value outside the IntelliJ platform; VS Code users are served by other tools (kilocode).
- **Trademark/branding churn.** The rename from "Claude Code GUI" to "CC GUI" (and logo changes) signals real third-party-branding risk to be aware of for a tool wrapping Anthropic/OpenAI products.
- **Overlaps the IDE's own AI features and other agents.** JetBrains AI and in-editor agents (kilocode) compete for the same slot; the draw is specifically *Claude Code + Codex CLIs* in a GUI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + / neutral | `@file` context + conversation rewind + skills help steer the agent; output quality is the underlying CLI's. |
| Speed | + | Visual agent + `@file` context inside the IDE removes terminal/editor context-switching. |
| Maintainability | neutral | Affects your editing workflow, not codebase structure. |
| Safety | neutral / + | Runs the CLIs' file/exec tools (standard trust model); maintainer's per-release security audits are a positive. |
| Cost Efficiency | neutral | Free/MIT plugin; spends the underlying provider's tokens. |

## Verdict

**CONDITIONAL** — adopt if you work in a **JetBrains IDE** and want Claude Code and/or Codex as a native visual panel with `@file` context, image input, conversation rewind, skills, and MCP — rather than driving them in a terminal. It's mature, actively maintained, dual-engine, MIT, and the maintainer's security-audit cadence is reassuring. Not relevant outside JetBrains, and it's a front-end so cost/quality remain the CLIs'. Note the third-party-branding caveat. For VS Code, use kilocode; for a standalone desktop multiplexer, cc-switch.

Compared to neighbors: **kilocode** is the in-editor agent for VS Code/JetBrains (its own agent, not a CLI wrapper); **cc-switch** is a desktop GUI that switches between CLI agents; **claudian** hosts agents inside Obsidian. CC GUI is the **JetBrains-native GUI specifically for the Claude Code + Codex CLIs** — the IDE-panel host for those two terminal agents.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [jetbrains-cc-gui](https://github.com/zhukunpenglinyutong/jetbrains-cc-gui) | plugin | IntelliJ/JetBrains plugin giving Claude Code and OpenAI Codex a native visual panel — `@file` context, image input, conversation rewind, skills slash-commands, MCP (formerly "Claude Code GUI") | Claude Code/Codex are terminal-first; want them as a native GUI inside a JetBrains IDE with editor-aware context | kilocode, cc-switch, claudian |
