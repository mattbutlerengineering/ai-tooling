# Evaluation: obsidian-skills

**Repo:** [kepano/obsidian-skills](https://github.com/kepano/obsidian-skills)
**Stars:** 36,142 | **Last updated:** 2026-06-08 (pushed; created 2026-01-02) | **License:** MIT
**Dev loop stage:** Mostly *out of the code dev loop* — it teaches an agent to read/write a personal knowledge base (Obsidian vaults). The one stage-relevant member is `defuddle` (web → clean markdown), which touches Research/Discover and Plan by cutting ingestion token cost.
**Layer:** Process (five Agent-Skills-spec `SKILL.md` files plus reference docs; no runtime — the only executable dependency is the external Obsidian CLI / Defuddle CLI the skills shell out to)

---

## What it does

The catalog one-liner: "Agent skills for Obsidian — teaches agents to use Obsidian CLI and open formats." Built by **kepano (Steph Ango), Obsidian's CEO**, this is a small, curated, first-party skill pack that teaches a skills-compatible agent the Obsidian-specific dialects most models do not reliably know. As inspected, it ships exactly **five skills** under `skills/`:

- **obsidian-markdown** — Obsidian Flavored Markdown: wikilinks `[[Note]]`, embeds `![[...]]`, callouts `> [!type]`, properties/frontmatter; references split into `CALLOUTS.md`, `EMBEDS.md`, `PROPERTIES.md`.
- **obsidian-bases** — the `.base` database format (views, filters, formulas, summaries) with a `FUNCTIONS_REFERENCE.md`.
- **json-canvas** — the open [JSON Canvas](https://jsoncanvas.org/) `.canvas` spec (nodes, edges, groups) with an `EXAMPLES.md`.
- **obsidian-cli** — drive vaults, plugins, and themes via the Obsidian CLI.
- **defuddle** — shell out to the Defuddle CLI to extract clean markdown from web pages, "instead of WebFetch," to save tokens.

The mechanism is install-and-trigger, not orchestration. The repo is itself a Claude Code marketplace plugin (`.claude-plugin/marketplace.json` + `plugin.json`) and also installs via `npx skills add`, manual `/.claude` copy, or cloning into `~/.opencode/skills/`. Each `SKILL.md` carries clean Agent-Skills-spec frontmatter (`name`, `description`) with sharp trigger conditions — the `defuddle` description even encodes a negative rule ("Do NOT use for URLs ending in .md"). It is portable by design across Claude Code, Codex, and OpenCode.

## How we tested it

**Source-grounded inspection — not installed, not run.** No skill was installed, no plugin added, and neither the Obsidian CLI nor Defuddle CLI was executed. Every claim comes from the repository (GitHub metadata, README, full recursive file tree, two sampled `SKILL.md` frontmatters), not from observed agent behavior. The "saves tokens" framing for `defuddle` is the author's README claim, not a number I measured.

```bash
gh api repos/kepano/obsidian-skills --jq '{desc,stars:.stargazers_count,forks:.forks_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'
gh api repos/kepano/obsidian-skills/readme --jq '.content' | base64 -d
gh api 'repos/kepano/obsidian-skills/git/trees/main?recursive=1' --jq '.tree[].path'   # 5 skills, references/, .claude-plugin/
gh api repos/kepano/obsidian-skills/contents/skills/obsidian-markdown/SKILL.md --jq '.content' | base64 -d | head -25
gh api repos/kepano/obsidian-skills/contents/skills/defuddle/SKILL.md     --jq '.content' | base64 -d | head -15
gh api repos/kepano/obsidian-skills/commits --jq 'length'        # 30 (page-1 cap)
gh api repos/kepano/obsidian-skills/contributors --jq '[.[].login]'  # ~15, kepano dominant
```

## What worked

- **First-party authority and tight scope.** Written by Obsidian's CEO, covering exactly the formats Obsidian owns or co-defines (Obsidian Flavored Markdown, `.base`, JSON Canvas, the CLI). Five focused skills — the opposite of the 100-plus-file menus elsewhere in this catalog. Nothing speculative.
- **Textbook Agent-Skills hygiene.** Clean spec-compliant frontmatter, sharp `description` triggers (including a negative condition in `defuddle`), and references factored into separate `.md` files so the main `SKILL.md` stays lean — exactly the progressive-disclosure pattern this catalog favors. These are reference-quality examples of *how to write a skill*.
- **Genuinely portable.** One repo installs cleanly into Claude Code (marketplace plugin), Codex, and OpenCode, with documented per-tool paths. No lock-in.
- **`defuddle` is the one broadly useful, dev-loop-relevant member.** A clean-markdown web extractor that explicitly displaces WebFetch to cut ingestion tokens is useful to any agent doing Research/Discover or Plan, Obsidian user or not.
- **Trustworthy provenance.** 36K stars, 2.5K forks, MIT, first-party — about as low-risk a skill source as exists.

## What didn't work or surprised us

- **Four of five skills are out of the code dev loop.** obsidian-markdown, obsidian-bases, json-canvas, and obsidian-cli only matter if you keep an Obsidian vault and want an agent to author into it. For a team shipping software, that is a personal-knowledge-management concern, not a Plan→Ship concern. The catalog's "interact with Obsidian knowledge bases" is accurate — and that is precisely the limit.
- **Hard dependency on external CLIs not in the repo.** obsidian-cli and defuddle are thin wrappers that shell out to the Obsidian CLI and `defuddle` (`npm i -g defuddle`) respectively. The skill is instructions; the capability lives in tools you must install separately and which can break independently.
- **No releases / no versioning.** Despite the plugin manifest, there are 0 tagged releases — you install whatever `main` is, with no pinned bundle (a minor concern given the tiny, stable surface).
- **The format coverage overlaps a model's growing native knowledge.** Frontier models increasingly know wikilinks and callouts; the durable value is the long-tail specifics (`.base` formulas, JSON Canvas edges, CLI flags), not the basics.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (narrow) | Encodes Obsidian-specific syntax (wikilinks, `.base` formulas, JSON Canvas, callouts) the model may get subtly wrong, raising correctness *on those formats only*. |
| Speed | + | `defuddle` cuts web-ingestion tokens vs WebFetch; the format skills save round-trips fixing malformed Obsidian syntax — but only inside Obsidian work. |
| Maintainability | neutral | Pure instruction files; no effect on your codebase. The *repo* is well-kept and first-party, but adds nothing to your project's maintainability. |
| Safety | neutral / − | The markdown skills are inert. obsidian-cli and defuddle shell out to external CLIs — low risk, but capability and trust live in tools outside this repo. |
| Cost Efficiency | + (narrow) | `defuddle`'s clutter-stripping reduces token spend on web reads; otherwise neutral. |

## Verdict

**CONDITIONAL — install `defuddle` for any agent; install the rest only if you live in Obsidian.** This is a small, first-party, exemplary-quality skill pack with the best Agent-Skills hygiene in the catalog. But four of its five skills are personal-knowledge-management tooling that sits outside the software dev loop — they are excellent *if and only if* your workflow runs through an Obsidian vault. The portable, broadly-useful piece is `defuddle` (web → clean markdown, token-saving), which is worth lifting on its own. Treat the markdown/bases/canvas skills as best-in-class *reference examples* of skill authoring even if you never keep a vault.

Compared to neighbors: it is the spiritual companion to **tolaria** (an Obsidian-class local-first markdown KB app whose vaults double as agent context) — tolaria gives you the *vault*, obsidian-skills teaches the agent to *write* it. Against the catalog's documentation cluster (**documentation-writer**, **documentation-and-adrs**) it is narrower and format-specific rather than process-driven. Unlike the sprawling research-skill packs, its discipline is its strength: five skills, no theater, first-party. It earns CONDITIONAL purely on audience narrowness, not quality.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [obsidian-skills](https://github.com/kepano/obsidian-skills) | skill | First-party pack of 5 Agent-Skills teaching agents Obsidian formats (Flavored Markdown, `.base`, JSON Canvas, CLI) plus a `defuddle` web→clean-markdown extractor | Agents get Obsidian-specific syntax wrong and burn tokens on cluttered web pages when authoring into a vault | tolaria (vault app vs. skills that write it); documentation-writer (broader, process-driven docs) |
