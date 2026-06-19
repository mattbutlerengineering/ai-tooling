# Evaluation: CLI-Anything

**Repo:** [HKUDS/CLI-Anything](https://github.com/HKUDS/CLI-Anything)
**Stars:** 43,466 | **Last updated:** 2026-06-14 | **License:** Apache-2.0
**Dev loop stage:** Implement (occasionally Verify) — but primarily for *non-coding* software domains
**Layer:** Infrastructure (Claude Code plugin that generates tooling)

---

## What it does

Catalog one-liner: "Making all software agent-native via CLI wrappers." The mechanism has two halves.

**(1) A harness generator.** Installed as a Claude Code plugin (`/plugin marketplace add HKUDS/CLI-Anything` then `/plugin install cli-anything`), it exposes a `/cli-anything <software-path-or-repo>` command that runs a 7-phase pipeline against a target piece of software: Analyze (scan source, map GUI actions to APIs) → Design (command groups, state model, output formats) → Implement (build a Click-based CLI with REPL, JSON output, undo/redo) → Plan Tests → Write Tests → Document → Publish (`setup.py`, install to PATH). The output is a self-contained Python "agent-harness" directory plus a generated `SKILL.md` so the resulting CLI is itself agent-discoverable. A `/cli-anything:refine` command does incremental gap analysis to widen coverage. The plugin is multi-agent: the same harness/commands ship for Pi, OpenClaw, OpenCode, Codex, Hermes, Reasonix, Qodercli, and GitHub Copilot CLI.

**(2) CLI-Hub, a registry + package manager.** `pip install cli-anything-hub` gives `cli-hub list/search/install/launch <name>` over ~80 community-built CLIs already in the repo, plus a meta-skill (`npx skills add HKUDS/CLI-Anything --skill cli-hub-meta-skill`) that lets an agent autonomously discover and install the right CLI for a task.

The decisive fact for this catalog is *what the ~80 shipped CLIs are*: GIMP, Blender, Krita, Inkscape, MuseScore, FreeCAD, Audacity, OBS Studio, Kdenlive, Shotcut, QGIS, Live2D, draw.io, Mermaid, ComfyUI, Zoom, Calibre, Zotero, Obsidian, Slay the Spire II, Godot, etc. — overwhelmingly creative/desktop/end-user applications. A minority touch a developer's workflow (lldb, n8n, pm2, chromadb, ollama, exa, wiremock, eth2-quickstart). The project's stated thesis ("Today's software serves humans; tomorrow's users will be agents") is general agent-enablement, not coding-loop improvement.

## How we tested it

Inspected the repository via the GitHub API and read the full README; did not install the plugin or run `/cli-anything` against a target. This is an architecture/scope review of a Claude Code plugin whose surface area (which software it makes agent-native) is the load-bearing question for this catalog, and that surface is fully visible from the repo tree and registry.

```bash
gh api repos/HKUDS/CLI-Anything --jq '{stars,license,description,pushed_at,created_at,language}'
gh api repos/HKUDS/CLI-Anything/readme --jq '.content' | base64 -d        # full README
gh api "repos/HKUDS/CLI-Anything/git/trees/main" --jq '.tree[] | select(.type=="tree") | .path'  # ~80 CLI dirs
gh api "repos/HKUDS/CLI-Anything/git/trees/main?recursive=1" --jq '.tree[].path'  # harness layout (e.g. 3MF/, QGIS/)
gh api repos/HKUDS/CLI-Anything/releases --jq '.[] | {tag,published}'      # v0.3.0 (2026-04), v0.2.0 (2026-03)
# Catalog overlap scan:
grep -inE "agent-native|CLI wrapper|cli-anything|nanobot|skill generat" CATALOG.md
```

Reviewed: the 7-phase generator command set (`/cli-anything`, `:refine`, `:test`, `:validate`, `:list`), the Claude Code plugin install path (`.claude-plugin/marketplace.json`, `cli-anything-plugin/`), the CLI-Hub package manager, the meta-skill, and the per-CLI harness structure (each is a Click CLI under `<App>/agent-harness/cli_anything/<app>/` with `core/`, `tests/`, and `skills/SKILL.md`).

## What worked

- **Genuine, first-class Claude Code integration.** Unlike a generic library, this ships an actual Claude Code plugin marketplace, a real slash command, and per-CLI `SKILL.md` files. The output of the generator is itself agent-native. This is the strongest reason it is not a clean SKIP like aisuite.
- **The 7-phase pipeline encodes good practice.** It doesn't just wrap a binary — it forces a test plan, a written test suite, JSON output, and a published `setup.py`. The repo advertises 2,461 passing tests across harnesses, and per-CLI dirs do contain real `tests/` with unit + E2E coverage.
- **CLI-Hub solves real distribution friction.** One `pip install` + `cli-hub install <name>` to get a ready-made, agent-callable wrapper for desktop software is a clean pattern, and the meta-skill lets an agent self-serve.
- **Reputable authorship and strong momentum.** HKUDS (HKU Data Intelligence Lab, also behind nanobot/LightRAG) — 43K stars, daily merges through mid-June 2026, active security-hardening passes (path-traversal fixes, `defusedxml` routing of untrusted XML), an arXiv tech report, and a multi-agent (not Claude-only) design.
- **Security is being taken seriously per-harness** — visible CVE-style fixes (GIMP Script-Fu path injection, Sketch token path traversal, Zoom token permissions, DOM sanitization for the browser CLI).

## What didn't work or surprised us

- **The target domain is mostly *not* coding.** The catalog's lens is tools that move quality signals in a developer's dev loop. ~80% of the shipped CLIs are creative/desktop/consumer apps (image editors, DAWs, video editors, 3D/CAD, note-takers, a roguelike). Making Blender or MuseScore agent-callable is valuable, but it is a *content-production* loop, not a software-development one.
- **Scope is "make any software agent-native," which is broader than coding — the same tension that landed aisuite at SKIP.** The difference here is the real Claude Code plugin and the dev-adjacent subset (lldb, n8n, pm2, chromadb, ollama, exa, wiremock), which pull it up to CONDITIONAL rather than SKIP.
- **For the coding loop specifically, the value is narrow and situational.** If you're debugging native code (lldb), driving a self-hosted automation backend (n8n), or scripting a vector DB (chromadb), the relevant harness helps. For routine app/web development it adds nothing the agent's existing shell + MCP toolset doesn't already cover.
- **Each generated CLI is a maintenance surface.** A generated Click harness for a large app is itself code to keep working against the upstream software's API churn; the `refine` loop exists precisely because first-pass coverage is partial. Community CLIs vary in depth.
- **Heavyweight to adopt for one use.** You install a plugin and a package manager to get wrappers; worth it if you live in agent-driven creative/desktop automation, overkill if you wanted one CLI.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Generated harnesses ship tests, but they make non-coding software callable; they don't improve the correctness of *your* code |
| Speed | + (conditional) | If your task genuinely needs to drive GUI/desktop software (or a dev backend like n8n/lldb), a ready CLI is far faster than ad-hoc scripting — but only for those tasks |
| Maintainability | - (mild) | Each generated CLI is additional code to maintain against upstream API drift; the refine loop is needed because coverage is incremental |
| Safety | + | Structured JSON output and per-harness security hardening (path-traversal, defusedxml, token handling) beat hand-rolled shell-outs to the same software |
| Cost Efficiency | neutral | Self-describing CLIs with `--help` reduce agent exploration tokens vs. raw automation, but this applies to non-coding software domains |

## Verdict

**CONDITIONAL**

CLI-Anything is a well-built, actively-maintained, reputably-authored Claude Code plugin — and that real integration is what distinguishes it from aisuite (SKIP). But its purpose is general agent-enablement of *all* software, and the ~80 CLIs it ships are overwhelmingly creative/desktop/consumer apps rather than software-development tooling. It does not write, review, test, or ship your code; it makes other software agent-callable. **Adopt it when your agent work involves driving GUI/desktop or specialized software — image/audio/video editing, 3D/CAD, GIS, note-taking — or a dev-adjacent backend that already has a harness (lldb, n8n, pm2, chromadb, ollama, exa, wiremock).** For a standard code-centric dev loop it sits outside the workflow and is not part of the recommended stack. Re-evaluate if the coding-relevant subset of the registry grows substantially.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [CLI-Anything](https://github.com/HKUDS/CLI-Anything) | tool | Making all software agent-native via CLI wrappers | Existing tools don't expose interfaces that AI agents can use | — |
