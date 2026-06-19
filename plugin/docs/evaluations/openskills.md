# Evaluation: openskills

**Repo:** [numman-ali/openskills](https://github.com/numman-ali/openskills)
**Stars:** 10,446 | **Last updated:** 2026-01-18 (v1.5.0) | **License:** Apache-2.0
**Dev loop stage:** Implement (sits beside the inner loop — installs/distributes skills agents load while working; does not change how a skill behaves)
**Layer:** Infrastructure (skill installation + a load shim around the agent CLI)

---

## What it does

Catalog one-liner: "Universal skills loader — installs SKILL.md to any agent (Claude Code, Cursor, Codex, Aider)." OpenSkills is a single npm CLI (`npx openskills …`, Node 20.6+) that takes Anthropic's `SKILL.md` format — the exact `name`/`description` frontmatter + progressive-disclosure body that Claude Code ships — and makes it usable by any agent that can read an `AGENTS.md` file, not just Claude Code.

The mechanism has two halves. **Install/distribute:** `openskills install <source>` pulls skills from the Anthropic marketplace (`anthropics/skills`), any public/private GitHub repo, or a local path, into a skills directory — project-local `./.claude/skills/` by default, `~/.claude/skills/` with `--global`, or `./.agent/skills/` with `--universal` to avoid colliding with Claude Code's own plugin marketplace. `update`/`remove`/`manage`/`list` round out lifecycle management, and installs record their source so `update` can refresh from git. **Load shim:** `openskills sync` writes the *exact same* `<available_skills>` XML block that Claude Code injects into its system prompt, but into your `AGENTS.md` (between `SKILLS_TABLE_START/END` markers). The catch is the invocation contract: where Claude Code natively loads a skill via its built-in `Skill("name")` tool, OpenSkills tells the agent to shell out — `npx openskills read <name>` — which prints the skill body plus a base directory for bundled resources. So for non-Claude-Code agents, OpenSkills *is* the progressive-disclosure runtime; for Claude Code itself, the native skills system already does this, and OpenSkills is mainly an installer/source-manager that happens to also emit an AGENTS.md table.

Architecturally this is the **lightweight, headless, CLI counterpart** to the catalog's two skill-portability peers: skills-manage (a Tauri *desktop GUI* doing central-library symlink installs across 28 platforms) and capa (a `capabilities.yaml` package manager that fans out the *full* primitive set — skills + rules + sub-agents + hooks + MCP — into each editor's native format). OpenSkills is deliberately narrower than both: it moves **only skills**, via files and a CLI, with no server, no DB, no GUI, no MCP. Its FAQ explicitly argues against MCP for this ("skills are static instructions + resources → no server required").

## How we tested it

Method: inspected the repository, full README, and the published npm package metadata; pulled maturity/adoption signals via the GitHub and npm registry APIs; read the supported-source list, the `--universal` priority order, the command/flag surface, and the AGENTS.md XML format to determine the mechanism (file installer + `read`-shim load contract vs. a runtime agent client or MCP server). Compared directly against the two calibration evals already in this catalog (skills-manage = SKIP, capa = CONDITIONAL), both of which are skill/config portability tools. **Did not install or run the CLI** — this is a repo + README + registry review, not hands-on usage. No metrics were invented; all numbers below are quoted from the GitHub/npm APIs.

```bash
gh api repos/numman-ali/openskills --jq '{stars,license,description,pushed_at,created_at,open_issues,forks}'
# 10,446 stars, Apache-2.0 (API shows NOASSERTION; LICENSE file is Apache 2.0, "Copyright 2025 OpenSkills Contributors"),
# TypeScript, created 2025-10-26, pushed 2026-01-18, 43 open issues, 661 forks
gh api repos/numman-ali/openskills/readme --jq '.content' | base64 -d        # mechanism, AGENTS.md format, FAQ
gh api repos/numman-ali/openskills/releases --jq '.[].tag_name'              # v1.0.0 … v1.5.0 (post-1.0, 9 releases)
gh api repos/numman-ali/openskills/contributors --jq 'length'               # 2 contributors
npm view openskills version description license time.created time.modified  # v1.5.0, npm published 2025-10-26
curl -s https://api.npmjs.org/downloads/point/last-month/openskills          # 19,194 downloads (2026-05-20..06-18)
curl -s https://api.npmjs.org/downloads/point/last-week/openskills           # 4,616 downloads
grep -niE 'openskills|skills-manage|capa|refly|skill-creator' CATALOG.md     # overlap check
```

## What worked

- **Right primitive at the right weight.** A single `npx`-runnable CLI that installs SKILL.md from marketplace / GitHub / local / private-git into a versionable, project-local `.claude/skills/` (or `.agent/skills/`) folder is exactly the scriptable, CI-friendly, headless install path that skills-manage's desktop GUI lacks. `-y/--yes` for CI and `-o` for custom output show it's built for automation, not just interactive use.
- **Exact format fidelity to Anthropic's spec.** It reuses Claude Code's `SKILL.md` frontmatter and reproduces the literal `<available_skills>` XML, so a skill authored for Claude Code drops into any AGENTS.md-reading agent unchanged. No lowest-common-denominator translation layer.
- **Genuinely solves portability for the cross-editor case.** The `read`-shim is the clever bit: it gives Cursor/Windsurf/Aider/Codex real progressive disclosure (load the one-line description always, fetch the full body only on `openskills read`) — the context-hygiene benefit that makes skills worth using, delivered to agents that have no native skills system.
- **Strong adoption and honest scoping.** 10.4K stars, 661 forks, ~19K npm downloads/month and ~4.6K/week — by far the most-adopted of the three skill-portability tools (vs skills-manage 2K stars, capa 284). Apache-2.0, post-1.0 (v1.5.0), explicit "Not affiliated with Anthropic" disclaimer, and a clear FAQ rationale for *not* being an MCP server.
- **Low lock-in.** Skills land as plain files in standard directories the tools already read; stopping use leaves your `.claude/skills/` intact. No DB, no running server, no credentials at rest (private-repo installs use your existing git auth, not a stored PAT).

## What didn't work or surprised us

- **It is a distribution/load layer, not a dev-loop quality tool.** Like skills-manage, it changes *which skills are installed where* and *how an agent loads them* — it does not author, improve, test, review, or reason about skill content. The actual quality lever (what the SKILL.md says) lives elsewhere (skill-creator, write-a-skill). In this catalog's framework — tools that move quality signals *inside* the loop — its surface area is thin.
- **For a Claude-Code-primary user, most of the value evaporates.** Claude Code already installs skills (plugins/marketplace) and loads them natively via the `Skill` tool with the same `<available_skills>` block. Running `openskills` against Claude Code mainly buys you a git-sourced installer and an AGENTS.md table you may not need. The `read`-shim's whole reason to exist — giving non-CC agents progressive disclosure — is redundant where the native skills system runs. The portability payoff is real only if you *also* drive Cursor/Codex/Aider/Windsurf from the same skills.
- **The `read` invocation contract is a soft handshake, not enforcement.** Whether a non-CC agent actually shells out to `npx openskills read <name>` at the right moment depends on it obeying the AGENTS.md instructions — there's no tool-call guarantee like Claude Code's native `Skill`. Reliability across agents will vary; this is inherent to the "instructions in a markdown file" approach and not independently verified here.
- **Maintenance has gone quiet.** Created 2025-10-26, but **last pushed 2026-01-18 — ~5 months stale as of this evaluation**, with only 2 contributors and 43 open issues. Adoption is excellent and it's post-1.0, but the bus factor and the commit gap are real risks for something you'd standardize a skill pipeline on. (Contrast capa: 284 stars but ~weekly releases.)
- **API license metadata quirk.** GitHub's API returns `NOASSERTION`; the repo's `LICENSE` file and README both clearly state Apache-2.0. Cosmetic, but noted for accuracy.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Does not alter agent reasoning, prompts, or skill content — `openskills read` yields the same SKILL.md body the tool would load if installed by hand |
| Speed | + (situational) | One `npx` command to install + `sync` across agents, CI-friendly with `-y`; only pays off when managing skills across more than one editor |
| Maintainability | + (situational) | Project-local, versionable skill files + git-sourced `update` reduce skill drift across editors; for single-editor CC use it adds an AGENTS.md table you may not need |
| Safety | neutral / + | No stored credentials, no server, no DB; private installs reuse existing git auth — cleaner posture than skills-manage's plaintext PAT. The `read`-shim's load reliability is unenforced |
| Cost Efficiency | + (claimed by design) | Progressive disclosure (description always, body on demand) keeps context lean for non-CC agents; free, no token cost of its own. Not independently measured |

## Verdict

**CONDITIONAL**

OpenSkills is the best-built and most-adopted of the catalog's three skill-portability tools, and it earns a clearly better verdict than the GUI skills-manage (SKIP) for a structural reason: it is the lightweight, headless, scriptable, version-controlled CLI that skills-manage's desktop binary is not — no unsigned binary, no SQLite store, no plaintext PAT, just `npx` against plain files in directories the tools already read. The calibration eval for skills-manage explicitly named openskills as the peer that "delivers the cross-editor portability without a native binary," and that holds up. Its one real differentiator over capa is the `read`-shim that brings genuine progressive disclosure to non-Claude-Code agents.

It lands at CONDITIONAL rather than ADOPT for the same scope reason capa did: **the core pain it solves is multi-editor.** For a Claude-Code-primary user, Claude Code already installs and natively loads skills via the `Skill` tool with the identical `<available_skills>` block — so openskills mostly adds a git-sourced installer and an AGENTS.md table you don't strictly need, and the `read`-shim is redundant where the native skills runtime runs. **Adopt when** you drive two or more agents (Claude Code + Cursor/Codex/Aider/Windsurf) from one shared set of SKILL.md skills and want a single, versionable, CI-friendly installer + cross-agent load shim. **Skip if** you're single-editor Claude Code: the native skills system covers it, and openskills is an indirection over files the agent already consumes directly. Note the maturity caveat — strong adoption (10.4K stars, ~19K npm downloads/mo) but ~5 months since the last commit with only 2 contributors; re-check activity before standardizing a team pipeline on it.

Versus neighbors: **skills-manage** is the GUI install side (SKIP — desktop binary, weaker posture); **capa** is broader (skills + rules + sub-agents + hooks + MCP from one yaml, CONDITIONAL) but moves more machinery; **openskills** is the narrow, file-and-CLI, skills-only middle ground with the strongest adoption and the unique non-CC `read`-shim. For *authoring* skills (the actual quality lever it does not touch), pair with **skill-creator** / **write-a-skill**.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [openskills](https://github.com/numman-ali/openskills) | tool | Universal skills loader — one CLI installs Anthropic SKILL.md to any agent (Claude Code, Cursor, Codex, Aider) and emits the AGENTS.md `<available_skills>` block (10K stars) | Skills are editor-specific; need a universal, scriptable installer + load shim that works across all AI editors | refly, skill-creator, skills-manage (GUI install side), capa (broader config fan-out) |
