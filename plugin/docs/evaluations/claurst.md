# Evaluation: claurst

**Repo:** [Kuberwastaken/claurst](https://github.com/Kuberwastaken/claurst)
**Stars:** 9,830 (7,780 forks) | **Last updated:** 2026-06-17 | **License:** GPL-3.0
**Dev loop stage:** Plan + Implement + Verify (a full inner-loop terminal agent — but a *replacement* front-end, not a Claude Code add-on)
**Layer:** Tooling (an alternative agent harness / standalone CLI)

---

## What it does

Catalog one-liner: "Agentic coding for builders who ship." That is the marketing tag from the README header; it does not describe the mechanism. Ground truth: **claurst is a standalone, multi-provider terminal coding agent written from scratch in Rust — a clean-room reimplementation of Claude Code, not a Claude Code plugin, skill, or MCP.** It is its own binary (`claurst`) that you install and run *instead of* `claude`, not something you bolt onto an existing Claude Code session.

The project's origin is unusual and worth stating plainly: per the README and the author's blog, Claude Code's TypeScript source was exposed via a sourcemap in an npm publish; the author (Kuber Mehta) ran a two-phase clean-room process — one AI agent read the leaked source and produced behavioral specs (the committed `spec/` directory, 13 documents), and a *separate* AI agent implemented idiomatic Rust from the spec alone, never touching the original TypeScript. The README cites Phoenix Technologies v. IBM (1984) and Baker v. Selden (1879) as the clean-room legal precedent. So claurst is a behavior-compatible re-implementation: it reproduces Claude Code's behavior (tools, commands, hooks, permission flow) in a different language and runtime.

Mechanically, what you get is a Rust TUI pair-programmer with: multi-provider routing (Anthropic, plus a "Free Mode" and others via `/connect`), a rich terminal UI, a plugin system, an MCP client, hooks, slash commands (`/goal` for multi-turn objective persistence, `/share` to export sessions to GitHub Gists, `/connect`, `/goal`), a companion mascot named Rustle, chat forking, and memory consolidation. It speaks the **Agent Client Protocol (ACP)** so ACP-aware editors (Zed, Neovim, JetBrains) can drive it as a subprocess (`claurst acp`). It runs interactively, headless one-shot (`claurst -p "..."`), or as an ACP server. Config lives in `~/.claurst/settings.json`. No telemetry. The Rust workspace (`src-rust/crates/`) is cleanly split: `acp`, `api`, `bridge`, `buddy`, `cli`, `commands`, `core`, `mcp`, `plugins`, `query`, `tools`, `tui`.

Note the naming/relationship trap: it *consumes* Claude Code's config conventions (it ships and asks contributors to include an `AGENTS.md`, has `docs/hooks.md`, `docs/mcp.md`, `docs/plugins.md` mirroring Claude Code's feature set) — but "Claude Code compatible behavior" means it behaves *like* Claude Code, not that it plugs *into* Claude Code. This is the same category distinction as oh-my-openagent: a different front-end, not an extension of this catalog's loop.

## How we tested it

**Method: inspected the repo, README, full recursive file tree, license, docs index, and maturity signals via the GitHub API and npm registry API. Did NOT install or run it.** This is a deliberate non-install evaluation. claurst is an *alternative harness* — installing it (`curl ... | bash` dropping a binary into `~/.claurst/bin`, or `npm i -g claurst` which postinstall-downloads a platform binary) gives you a separate coding agent that replaces the front-end of this catalog's standardized Claude Code dev loop rather than extending it. Running it would not exercise the harness (Claude Code) this catalog standardizes on, and it wants its own provider/API-key config. So the verdict rests on the repo, the clean-room provenance, the documented mechanics, the license, and the maturity signals below. No metrics are invented; star/fork/release/contributor/commit counts are from live API calls and npm download numbers are from the npm registry API.

```bash
gh api repos/Kuberwastaken/claurst --jq '{stars:.stargazers_count,forks:.forks_count,license:.license.spdx_id,description,created_at,pushed_at,language}'
# 9,830 stars; 7,780 forks; GPL-3.0; Rust; created 2026-03-31; pushed 2026-06-17
gh api repos/Kuberwastaken/claurst/readme --jq '.content' | base64 -d            # full README
gh api "repos/Kuberwastaken/claurst/git/trees/HEAD?recursive=1" --jq '.tree[].path'  # spec/ (13 docs), src-rust/crates/{acp,api,bridge,buddy,cli,commands,core,mcp,plugins,query,tools,tui}, docs/
gh api repos/Kuberwastaken/claurst/contents/src-rust/crates --jq '.[].name'        # 12 crates
gh api repos/Kuberwastaken/claurst/releases --paginate --jq '.[].tag_name' | wc -l  # 8
gh api repos/Kuberwastaken/claurst/contributors --paginate --jq '.[].login' | wc -l # 19
gh api repos/Kuberwastaken/claurst/commits --paginate --jq '.[].sha' | wc -l        # 272
gh api repos/Kuberwastaken/claurst/releases/latest --jq '{tag,published_at}'        # v0.1.5, 2026-06-11
curl -s https://api.npmjs.org/downloads/point/last-month/claurst                    # 626/mo
```

Reviewed: README (English), the recursive file tree, the `spec/` clean-room specification index, the `docs/` set (advanced, agents, auth, commands, configuration, hooks, keybindings, mcp, plugins, providers, tools), the crate layout, the ACP integration section, and the maturity signals above.

## What worked

- **Genuinely interesting engineering and clean provenance.** A from-scratch Rust reimplementation of a Claude Code-class agent, built two-phase clean-room with the specs committed in `spec/`, is a real contribution — and the `spec/` directory is a useful reference artifact in its own right (it is an exhaustive behavioral spec of a coding agent's tools/hooks/permission model). The crate split (`acp`, `core`, `tools`, `tui`, `mcp`, `plugins`, …) is idiomatic and legible.
- **ACP-native and editor-driveable.** First-class Agent Client Protocol support (`claurst acp`, JSON-RPC over stdio, `session/request_permission` routed to the editor's native approval dialog) means it slots into Zed/Neovim/JetBrains cleanly — a real differentiator vs. the many CLI-only alternatives.
- **No telemetry, multi-provider, fast/memory-efficient Rust binary.** For users who want an open, self-hosted, privacy-respecting coding agent that is not tied to a single provider, the value proposition is coherent. "Free Mode" lowers the barrier to trying agentic coding without a paid key.
- **Reasonable early traction.** 9.8k stars and (notably) 7.8k forks in under three months, 8 releases, 19 contributors, an MIT-style community posture (issues/PRs welcome, AGENTS.md, devcontainer, CI/release/npm-publish/pages workflows). The very high fork-to-star ratio is unusual — partly a viral "Claude Code got leaked, I rebuilt it in Rust" story — but it is real attention with active CI and a docs site.

## What didn't work or surprised us

- **It is NOT a Claude Code tool — this is the central caveat and the basis for the verdict.** claurst is a standalone agent you run *instead of* Claude Code. There is no plugin, skill, or MCP to adopt into an existing Claude Code session. For a catalog standardized on the Claude Code dev loop, adopting claurst means *switching harnesses* (and switching the agent's runtime, config, and provider setup), which is a large commitment, not an enhancement. This is the same disqualifier that made oh-my-openagent a SKIP.
- **Early beta, thin maturity for daily-driving.** v0.1.5, explicitly self-labeled Beta, with multiple headline features flagged `[EXPERIMENTAL]` (`/share`, Free Mode, `/goal`). 8 releases, 19 contributors, 272 commits, and **only ~626 npm downloads/month** — orders of magnitude below the established harnesses in the catalog (oh-my-claudecode ~31k/mo, oh-my-openagent ~267k/mo). The stars/forks are driven by a viral leak narrative more than by production adoption.
- **GPL-3.0 is a strong copyleft license.** Stronger than the MIT/Apache norm in this catalog and meaningfully different from a commercial-integration standpoint — modifying and redistributing claurst (or linking it into a distributed product) triggers GPL obligations. A real legal-review item for any company, and stricter than oh-my-claudecode's MIT.
- **Provenance, while defensible, is legally untested.** The clean-room story and the Phoenix v. IBM / Baker v. Selden citations are a thoughtful good-faith posture, but it is a reimplementation derived (via specs) from leaked proprietary source. Anyone adopting it commercially should be aware the legal status is the author's argued position, not settled law for this specific case.
- **No independent quality evidence.** There is no benchmark or hands-on data showing claurst matches Claude Code on real coding tasks; "stable enough for daily driving" is the author's self-assessment of a v0.1.x beta.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral / unknown | Reimplements Claude Code's tool/permission behavior, but no benchmark or hands-on data shows it matches Claude Code on real tasks; v0.1.x beta with experimental features |
| Speed | + (potential) | Rust binary, "fast and memory-efficient" by design; headless `-p` and ACP modes — but unverified here, and small tasks gain nothing from switching harness |
| Maintainability | - (for *this* loop) | Adopting it replaces the Claude Code front-end rather than integrating into the loop; you maintain a separate agent runtime, config, and provider setup |
| Safety | +/- | No telemetry and editor-native per-tool permission prompts (via ACP `session/request_permission`) are positives; offset by early-beta maturity and the `curl | bash` install path |
| Cost Efficiency | + (potential) | Multi-provider routing and "Free Mode" can lower spend / avoid single-provider lock-in — relevant for users not on a Claude subscription, not for this catalog's Claude Code loop |

## Verdict

**SKIP** (for *this* catalog's Claude Code dev loop) — interesting project, wrong category; re-evaluate only if the user's stack moves off Claude Code.

claurst is a legitimately interesting standalone Rust reimplementation of Claude Code with a clean provenance story, ACP-native editor integration, no telemetry, and multi-provider support. But for a catalog standardized on the Claude Code harness, it is a SKIP as an *installable artifact*: it is an **alternative agent you run instead of Claude Code**, not a plugin/skill/MCP that extends the existing dev loop. Adopting it means switching front-ends, which is exactly the disqualifier that placed oh-my-openagent at SKIP. On top of the category mismatch, the maturity is early (v0.1.5 beta, ~626 npm downloads/month, headline features `[EXPERIMENTAL]`), the GPL-3.0 license is a stronger commercial constraint than the catalog norm, and the leak-derived provenance — while argued in good faith — is legally untested. None of this is "thin/abandoned" (it has active CI, a docs site, and real attention), so the SKIP is on category fit, not quality.

**Differentiation from the harness cluster:**
- vs. **opencode / qwen-code / oh-my-pi / goose** (the standalone-alternative-agent cluster, all `platform`-type): claurst is the same *kind* of thing — a Claude Code alternative you switch to. Its distinguishing angle is the Rust clean-room-reimplementation provenance and ACP-native design; on maturity/adoption it trails opencode and oh-my-pi.
- vs. **oh-my-openagent** (SKIP, alternative harness on OpenCode/Codex): same verdict and same reasoning — both are front-ends you switch *to*, not Claude Code add-ons. OmO is far more mature (~267k npm downloads/mo) and its transferable value is harness-engineering ideas; claurst's transferable value is its committed `spec/` (a clean-room behavioral spec of a coding agent).
- vs. **oh-my-claudecode** (CONDITIONAL): the contrast is sharp — oh-my-claudecode is a *real Claude Code plugin* you install via the marketplace and that lives inside the loop; claurst replaces the loop. If you must pick one for a Claude Code stack, oh-my-claudecode is the integrated choice; claurst is not in that comparison at all.
- The current catalog "Overlaps with" (`superpowers, compound-engineering`) is mis-targeted — those are in-loop Claude Code skill/process tools, whereas claurst is a standalone harness. Better overlap neighbors are `opencode, qwen-code, oh-my-pi, goose` (and `oh-my-openagent` as the closest SKIP precedent).

Re-evaluate to CONDITIONAL if the user's stack moves off Claude Code (claurst would then compete on its own terms with opencode/qwen-code/oh-my-pi, where its ACP-native design and Rust footprint are genuine pluses), and the GPL-3.0 / clean-room-provenance posture fits their commercial constraints — and after it exits beta with real adoption.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claurst](https://github.com/Kuberwastaken/claurst) | harness | Rust clean-room reimplementation of Claude Code — standalone multi-provider terminal coding agent (ACP-native, no telemetry); not a Claude Code plugin | Want an open, self-hosted, provider-agnostic terminal coding agent as an alternative to Claude Code | opencode, qwen-code, oh-my-pi, goose, oh-my-openagent |
