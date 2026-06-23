# Evaluation: skills-hub

**Repo:** [qufei1993/skills-hub](https://github.com/qufei1993/skills-hub)
**Stars:** ~1,050 | **Last updated:** 2026-06-20 | **License:** MIT
**Dev loop stage:** Plan (skill management)
**Layer:** Tooling

---

## What it does

A cross-platform desktop app (Tauri + React) to manage Agent Skills in one place and **sync them to multiple AI coding tools'** global or project-level skills directories — "install once, sync everywhere."

Mechanically it provides: an **Explore** page to browse curated featured skills and search online (one-click install + sync to all detected tools); a **Tags** system to organize and filter your skills (including untagged); and **global/project sync** that pushes a skill into each detected tool's skills directory, preferring symlinks/junctions and falling back to copy. The premise is that skills today are scattered and must be re-installed per tool (Claude Code, Codex, Cursor, …); skills-hub centralizes curation and propagation.

## How we tested it

**Evidence:** REVIEW

Architecture review against the README and feature list (Explore/Tags/global+project sync, symlink-preferred propagation, multi-tool detection). Confirmed the Tauri desktop model and the "one library, sync to every tool's skills dir" mechanism. Not installed/run live, so condition-gated.

```bash
gh api repos/qufei1993/skills-hub --jq '{stars:.stargazers_count,license:.license.spdx_id,pushed:.pushed_at}'
gh api repos/qufei1993/skills-hub/readme --jq '.content' | base64 -d
```

## What worked

- **Solves real skill sprawl.** As skills multiply across Claude Code/Codex/Cursor/etc., a single manage-and-sync surface is genuinely useful — symlink-based sync keeps one source of truth.
- **Curation + organization.** Browse/search/install plus tagging makes a growing skill library navigable rather than a folder dump.
- **Project vs global scoping.** Syncing skills globally or to specific projects matches how people actually want skills applied.

## What didn't work or surprised us

- **Desktop app overhead.** A Tauri GUI is heavier than a CLI; some users prefer a scriptable sync over an app.
- **Sync correctness risk.** Symlink/junction-with-copy-fallback across tools and OSes is fiddly; verify it does the right thing on your platform before trusting it with many skills.
- **Young project.** ~1K stars; the curated catalog and tool-detection breadth are still maturing.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Manages skills; doesn't affect code correctness |
| Speed | + | One-click install/sync beats manual per-tool copying |
| Maintainability | + | Single source of truth for skills across tools |
| Safety | neutral | Review installed skills (skill content is the risk, not the manager) |
| Cost Efficiency | + | Free/OSS; saves repetitive skill setup |

## Verdict

**CONDITIONAL**

Adopt if you maintain a sizable skill library across multiple coding agents and want one place to curate, tag, and sync it — the symlink-based "install once, sync everywhere" model fits multi-tool users. CLI-preferring users may want a scriptable alternative; verify cross-OS symlink behavior first. Note the manager doesn't vet skill *content* — audit skills you install (pairs with waza for quality, security-reviewer for safety).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [skills-hub](https://github.com/qufei1993/skills-hub) | tool | Cross-platform desktop app (Tauri/React) to manage Agent Skills in one place (MIT) — browse/search/install, organize with tags, and sync to multiple AI tools' global or project skills dirs (symlink, fallback copy); "install once, sync everywhere" | Skills are scattered and must be re-installed per tool; want one place to curate and sync across every coding agent | vercel-labs/skills, find-skills, ComposioHQ/awesome-claude-skills |
