# Evaluation: skills-manage

**Repo:** [iamzhihuix/skills-manage](https://github.com/iamzhihuix/skills-manage)
**Stars:** 2,023 | **Last updated:** 2026-05-02 | **License:** Apache-2.0
**Dev loop stage:** Implement (sits beside the inner loop — manages which skills are installed where, not how the agent uses them)
**Layer:** Infrastructure (skill installation/config management around the agent CLI)

---

## What it does

Catalog one-liner: "Desktop app to manage AI coding agent skills across 20+ platforms from one place." skills-manage is a Tauri v2 (Rust backend + React 19 web UI) desktop application that gives you a single visual interface to install, enable, organize, and uninstall `SKILL.md`-style skills across 28 listed targets (Claude Code, Cursor, Codex CLI, Gemini CLI, Windsurf, Aider, Copilot, OpenCode, plus a cluster of "Lobster"/OpenClaw forks) instead of hand-managing each tool's `~/.<tool>/skills/` directory.

The core mechanism is a **central library + symlink installer**. It adopts the [Agent Skills](https://github.com/anthropics/agent-skills) open pattern and treats `~/.agents/skills/` as the canonical source of truth. Each platform reads skills from its own directory (`~/.claude/skills/`, `~/.cursor/skills/`, `~/.gemini/skills/`, etc.); when you "install" a skill to a platform, skills-manage creates a symlink (or copy) from the central library into that platform's skills directory, so one source skill can drive many tools. Around that it layers: a SQLite-backed metadata store (`~/.skillsmanage/db.sqlite`, WAL mode) for collections/scan-results/settings/cached AI explanations; a skill **detail view** with Markdown preview, raw source, and on-demand "AI explanation generation" (calls an LLM with your own API key); **Collections** for batch-installing groups of skills to platforms; a **Discover** scan that finds project-level skill libraries (`.skills/`, `.agents/skills/`, `.claude/skills/`, Obsidian vaults); and **marketplace browsing + GitHub repo import** (authenticated with a stored PAT, retry fallback) to pull public skills into the central library.

Critically, it is a *skill-installation manager*, not an agent client or a skill *authoring* tool in any deep sense. You do not run the agent inside it and it does not change how a skill behaves once installed — it manages *where the SKILL.md files live and which tools see them*. It is the installation/distribution counterpart to its catalog complement tolaria (which edits the markdown files themselves).

## How we tested it

Inspected the repository and its English README, pulled maturity metrics via the GitHub API, read the supported-platforms table, privacy/security section, tech stack, and project structure to determine the mechanism (central library + per-platform symlink installs vs. a runtime agent client), and checked release/contributor counts. **Did not install or run the desktop app.** The only prebuilt package is an *unsigned, un-notarized* Apple Silicon macOS `.dmg`/`.app.zip` (every other platform must be built from source via `pnpm tauri dev` + Rust + Tauri toolchain), and the app's whole value is in mutating *real* skill directories across many CLIs (`~/.claude/skills/`, `~/.cursor/skills/`, …) and importing skills from GitHub using a stored PAT — exercising that meaningfully would mean installing a native binary that Gatekeeper flags as "damaged" (requiring `xattr -dr com.apple.quarantine`) and wiring live credentials, which is out of scope. The verdict rests on source/README inspection and maturity signals, not a hands-on run.

```bash
gh api repos/iamzhihuix/skills-manage --jq '{stars,license,description,created_at,pushed_at,language,open_issues,forks}'
# 2,023 stars, Apache-2.0, TypeScript (Tauri v2 + React/Rust), created 2026-04-13, pushed 2026-05-02, 46 open issues, 184 forks
gh api repos/iamzhihuix/skills-manage/readme --jq '.content' | base64 -d   # mechanism, 28-platform table, privacy section
gh api repos/iamzhihuix/skills-manage/releases --jq '.[].tag_name'         # v0.10.0, v0.9.1, v0.9.0, v0.8.0 (pre-1.0)
gh api repos/iamzhihuix/skills-manage/contributors --jq '.[].login' | wc -l # 2 contributors
grep -niE 'tolaria|capa|openskills' CATALOG.md                              # overlap check
```

## What worked

- **Solves a real, repetitive friction with the right primitive.** The "central library + symlink to each platform" model is exactly the correct abstraction for skill portability: one source of truth, no copy drift, edit once and every linked tool sees it. For someone running skills across 3+ editors, hand-symlinking and tracking which skill is installed where is genuine toil this removes.
- **Broad, current platform coverage.** 28 targets including all the major CLIs (Claude Code, Codex, Cursor, Gemini, Windsurf, Aider, Copilot, OpenCode) plus collections, batch install, and a project-level Discover scan — more breadth than a single-CLI installer.
- **Honest, local-first privacy posture.** Local-only SQLite store, no telemetry/analytics, network access only on explicit marketplace/GitHub/AI-explanation actions, and an up-front disclaimer that it's unofficial and unaffiliated. This is a notably cleaner posture than cc-switch (no affiliate funnel, no cloud sync of credentials, no "signature bypass" utility).
- **Non-destructive to the underlying tools.** It manages the same skill directories you would manage by hand; the symlink model means stopping use leaves your tools working with whatever skills are currently linked. Low lock-in on the core install feature.
- **Sound, conventional engineering.** Tauri v2 / React 19 / Rust with a documented test+lint+clippy validation suite, a changelog, and per-release notes. The codebase hygiene is solid even if the project is young.

## What didn't work or surprised us

- **It is a convenience/installation layer, not a dev-loop quality tool.** It changes *which skills are installed where* and *how easily you manage them* — it does not change how the agent plans, implements, verifies, reviews, or ships, nor how well any skill performs. The skill content (the actual quality lever) is authored and improved elsewhere; this just distributes the files.
- **The portability benefit is largely free at the CLI/symlink layer.** A developer can already point multiple tools at one skill source with `ln -s` (or a one-off script), and lighter-weight peers cover the cross-editor install need without a desktop binary: **openskills** is a universal CLI installer for SKILL.md, and **capa** wires skills/tools/rules across 30+ editors from a single declarative `capabilities.yaml` — both fit a scriptable, version-controlled, headless/CI workflow that a GUI cannot.
- **Young and thin on maintainership.** Created 2026-04-13, pre-1.0 (v0.10.0), only 2 contributors, and **last pushed 2026-05-02 — ~6 weeks stale as of this evaluation**. 2K stars is healthy interest but the bus factor and the gap since the last commit are real maturity risks for something you'd route credentials through.
- **Distribution friction.** The only prebuilt binary is an unsigned/un-notarized Apple Silicon macOS build that Gatekeeper flags as "damaged" (manual `xattr` unquarantine required); Windows/Linux/Intel users must build from source. That undercuts the "from one place, easily" pitch for most of its audience.
- **Credentials stored unencrypted at rest.** The README states the GitHub PAT and AI API keys live in the local SQLite settings table and are "not encrypted at rest by the app." Local-first, but a plaintext-on-disk PAT/key is a real exposure for a young, 2-author project.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Does not alter agent reasoning, prompts, or skill behavior — installing a skill via the GUI yields the same SKILL.md the tool would read if symlinked by hand |
| Speed | + (situational) | One-click cross-platform install/uninstall and batch Collections beat hand-symlinking; only matters if you manage skills across several tools |
| Maintainability | neutral / + | No effect on your code; the central-library symlink model reduces skill *file* drift across editors (edit once, all linked tools update) |
| Safety | - (mild) | Stores GitHub PAT and AI API keys unencrypted in local SQLite; unsigned binary requires bypassing Gatekeeper. Offset by no telemetry / no cloud sync, so milder than cc-switch |
| Cost Efficiency | neutral | Free and local; the optional "AI explanation" feature spends your own API tokens but is opt-in and not core |

## Verdict

**SKIP**

skills-manage is a clean, honestly-built desktop manager with the *right* core primitive (a central `~/.agents/skills/` library symlinked into each tool's directory), and for someone juggling skills across many editors it removes real bookkeeping toil. Its privacy posture is markedly better than the closest precedent in this catalog, cc-switch — no affiliate funnel, no cloud-synced credentials, no signature-bypass utility — so it is not rejected on trust grounds the way cc-switch was.

It lands at SKIP for the same structural reason cc-switch did: in this catalog's framework (tools that move quality signals *inside* the dev loop), it has almost no surface area. It distributes skill files; it does not write, author, improve, review, test, or reason about anything — the quality of your skills is unchanged by how they get installed. And the one signal it does touch (Speed/portability) is owned better by lighter, scriptable, CI-friendly peers already in the catalog: **openskills** (universal CLI installer for SKILL.md) and **capa** (one `capabilities.yaml` across 30+ editors) deliver the cross-editor portability without a native binary, version-controlled and headless. Add a pre-1.0, 2-contributor project that has been stale ~6 weeks, a macOS-only unsigned build, and PATs/keys stored unencrypted at rest, and the convenience does not justify a stack slot. Keep the catalog entry as a known option; re-evaluate only if it reaches 1.0 with cross-platform signed builds and you specifically need a *GUI* (not a CLI/config file) to manage skills across many editors daily — in which case it pairs naturally with **tolaria** (edit the files) as the install side.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skills-manage](https://github.com/iamzhihuix/skills-manage) | tool | Desktop app to manage AI coding agent skills across 20+ platforms from one place (2K stars) | Managing skills across Claude Code, Cursor, Codex, Gemini requires per-editor configuration | tolaria, capa, openskills |
