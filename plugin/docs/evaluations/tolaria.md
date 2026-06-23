# Evaluation: tolaria

**Repo:** [refactoringhq/tolaria](https://github.com/refactoringhq/tolaria)
**Stars:** 16,738 | **Last updated:** 2026-06-19 | **License:** AGPL-3.0-or-later
**Dev loop stage:** Plan / Reflect (sits beside the loop — authoring and organizing the markdown *context* an agent reads, not driving the agent)
**Layer:** Tooling (a GUI editor over the files; the files themselves are the substance)

---

## What it does

Catalog one-liner: "Desktop app to manage markdown knowledge bases; visual editor for CLAUDE.md, skills, and documentation files." That framing is narrower than what the project actually is. Per the README, Tolaria is a general-purpose **markdown knowledge-base / "second brain" desktop app** for macOS, Windows, and Linux — an Obsidian-class vault editor built by Luca Rossi of the *Refactoring* newsletter, who runs a 10,000+ note personal vault in it. Its stated use cases are personal knowledge management, organizing company docs *as context for AI*, and storing assistant memory/procedures.

The mechanism: every vault is a plain directory of markdown files with YAML frontmatter, and **every vault is a git repository** — you get version history and any git remote, with no Tolaria server in the loop. The app is the editing/navigation surface over that directory: a keyboard-first editor, a command palette, and "types as lenses" (frontmatter-driven navigation categories that are *not* enforced schemas — no required fields, no validation). It is built with Tauri + React + TypeScript (with a Rust core), the same desktop stack as its catalog complement skills-manage.

The AI-tooling connection is real but secondary and indirect. The project's "AI-first but not AI-only" principle means a vault of files is good *context* for agents; it ships an `AGENTS` file and documents setup paths for Claude Code, Codex CLI, and Gemini CLI, and a bundled MCP server spawns the system `node` at runtime for "external AI tooling flow." But it does not author skills as a first-class object, has no CLAUDE.md-specific editor, and does not run an agent inside it. It is a place to *keep and edit* the markdown an agent consumes — adjacent to the dev loop, not inside it.

## How we tested it

**Evidence:** REVIEW

Inspected the repository and its README via the GitHub API, read the principles/installation/architecture sections and the AI-integration claims, and pulled maturity signals (stars, license, release cadence, contributor count, language breakdown). **Did not install or run the desktop app.** Tolaria's value is a long-lived personal/company markdown vault edited daily over thousands of notes; a one-off launch on an empty vault would not exercise anything meaningful, and the AI angle (vault-as-context, AGENTS file, bundled MCP server) is a thin convenience layer over plain files that an agent already reads directly from disk. The verdict rests on source/README inspection and maturity signals, not a hands-on run. Note: the catalog's supplied one-liner overstates the Claude Code specificity — corrected against the actual README.

```bash
gh api repos/refactoringhq/tolaria --jq '{stars:.stargazers_count,license:.license.spdx_id,desc:.description,created:.created_at,pushed:.pushed_at,lang:.language,open_issues:.open_issues_count,forks:.forks_count}'
# 16,738 stars, AGPL-3.0, "Desktop app to manage markdown knowledge bases", created 2026-02-14, pushed 2026-06-19, TypeScript, 47 open issues, 1,162 forks
gh api repos/refactoringhq/tolaria/readme --jq '.content' | base64 -d   # principles, AI-first claims, AGENTS file, MCP server note
gh api repos/refactoringhq/tolaria/releases --jq '.[].tag_name'         # all alpha-* tags (e.g. alpha-v2026.6.19-alpha.0005) — no stable release
gh api repos/refactoringhq/tolaria/contributors --jq '.[].login' | wc -l # 23 contributors
```

## What worked

- **Excellent data-ownership posture for AI context.** Files-first, git-first, offline-first, zero lock-in, standards-based (markdown + YAML frontmatter). A vault is just a git repo of plain files — exactly the format an agent reads best, and nothing is trapped in the app if you leave. This is a genuinely clean substrate for "docs as context for AI."
- **Real traction and active development.** 16.7K stars, 23 contributors, multiple releases *per day* (alpha tags dated the day of evaluation). It is a live, well-resourced project, not a weekend toy — far more momentum than skills-manage.
- **Sound engineering hygiene.** CI, Codecov, CodeScene health badges, published ARCHITECTURE/ABSTRACTIONS docs and ADRs, signed Windows installers, and a Homebrew cask. Solid for an alpha.
- **Documents agent setup paths.** Ships an `AGENTS` file and setup flows for Claude Code, Codex CLI, and Gemini CLI, plus a bundled MCP server — so it is aware of and accommodating to the agent workflow rather than hostile to it.

## What didn't work or surprised us

- **It is a general PKM app, not a Claude Code tool.** The catalog one-liner ("visual editor for CLAUDE.md, skills, and documentation files") overstates the fit. Tolaria is an Obsidian-class second-brain app whose AI integration is one principle among nine. It has no CLAUDE.md-aware editor, does not treat skills as a first-class object, and does not author, lint, version, or improve agent config — it just edits markdown.
- **The agent already reads the files directly.** The dev-loop value proposition is "a folder of markdown is good context," which is true with or without Tolaria. An agent reads `CLAUDE.md`, `docs/`, and `SKILL.md` straight from disk; a human GUI for editing those files does not change correctness, speed, or quality of the agent's work. The editing convenience accrues to the *human*, off the loop.
- **Pre-stable, fast-moving alpha.** Every release is an `alpha-*` tag (no 1.0, no stable). Multiple alphas per day signals churn; an API/format you depend on could shift under you. Fine for a personal vault, riskier as load-bearing infrastructure.
- **AGPL-3.0 + trademark policy.** Strong copyleft and a name/logo trademark policy — relevant if you wanted to embed or redistribute, less so for personal use, but worth flagging versus the permissive licenses common in this catalog.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | An agent reads the same markdown whether or not a human edited it in Tolaria; the GUI does not touch agent reasoning or output |
| Speed | + (situational, human-side) | Keyboard-first editor + command palette speed up *human* authoring/curation of context docs; no effect on agent throughput |
| Maintainability | + (mild) | Git-first vaults give version history and any remote for your context/docs; helps keep a large doc set tidy, but that benefit is the underlying git, not Tolaria |
| Safety | neutral / + | Offline-first, no accounts, no cloud, plain-file portability means low lock-in and no credential surface; AGPL/trademark are the only caveats |
| Cost Efficiency | neutral | Free and open source, fully local; the optional bundled MCP/agent flows spend your own tokens but are opt-in |

## Verdict

**SKIP**

Tolaria is an impressive, fast-growing, cleanly-architected markdown knowledge-base app with an exemplary data-ownership stance (files-first, git-first, offline-first, zero lock-in) — the *right* substrate for "documentation as AI context." If you want a daily-driver second brain or a git-versioned company doc vault and like Obsidian-style apps, it is a strong pick on its own merits.

It lands at SKIP for this catalog for the same structural reason skills-manage did: it is a human-facing convenience layer that sits *beside* the dev loop, not a tool that moves a quality signal *inside* it. The catalog one-liner oversells the Claude Code angle — Tolaria is a general PKM app, not a CLAUDE.md/skills editor, and an agent already reads markdown straight from disk regardless of which editor a human used. The signal it touches (human authoring speed for context docs) is off-loop, and its maintainability benefit is really just the underlying git. Add a no-stable-release, multiple-alphas-per-day cadence and AGPL/trademark terms, and it does not earn a stack slot as agent tooling. Keep the catalog entry as a known option and re-evaluate only if it ships first-class, Claude-Code-aware skill/CLAUDE.md authoring (lint, scaffold, version) that demonstrably improves agent output — at which point it would pair naturally with **skills-manage** (which installs/distributes the files Tolaria would edit).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [tolaria](https://github.com/refactoringhq/tolaria) | tool | Files-first, git-first desktop app for markdown knowledge bases usable as AI context (16.7K stars) | Keeping a large, portable, version-controlled markdown vault (docs/notes/agent memory) without app lock-in | skills-manage |
