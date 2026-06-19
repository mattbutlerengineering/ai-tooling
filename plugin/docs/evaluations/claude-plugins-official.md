# Evaluation: claude-plugins-official

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official)
**Stars:** 30,445 | **Last updated:** 2026-06-19 (`pushed_at`) | **License:** Apache-2.0 (per-plugin LICENSE; marketplace itself Apache-2.0)
**Dev loop stage:** Reflect / cross-cutting — it is the *distribution channel* for tools that act across every stage (Implement, Verify, Review, Ship)
**Layer:** Infrastructure (a marketplace/registry — the delivery substrate, not a single tool)

> **Scope note:** This is the **umbrella entry** for the official marketplace monorepo. It is *not* a single tool — it is the canonical first-party registry that **houses** plugins already evaluated individually in this catalog: `security-guidance` (ADOPT), `skill-creator` (ADOPT/KEEP), `plugin-dev`, `code-review`, `pr-review-toolkit`, `commit-commands`, `feature-dev`. Those member evaluations stand on their own; this entry assesses the marketplace as the source and trust anchor.

---

## What it does

Catalog framing: Anthropic's official, Anthropic-managed directory of high-quality Claude Code plugins. The repo's own description: *"Official, Anthropic-managed directory of high quality Claude Code Plugins."*

Mechanically it is a **Claude Code plugin marketplace** — a git repo with a `.claude-plugin/marketplace.json` manifest that Claude Code reads to enumerate installable plugins. Two trees:

- **`/plugins`** — internal plugins developed and maintained by Anthropic (37 directories at HEAD), including the catalog's already-evaluated `security-guidance`, `skill-creator`, `plugin-dev`, `code-review`, `pr-review-toolkit`, `commit-commands`, `feature-dev`, plus many more: `code-simplifier`, `code-modernization`, `frontend-design`, `claude-code-setup`, `claude-md-management`, `mcp-server-dev`, `agent-sdk-dev`, `hookify`, `ralph-loop`, `session-report`, a family of language-server plugins (`pyright-lsp`, `typescript-lsp`, `rust-analyzer-lsp`, `gopls-lsp`, `clangd-lsp`, `jdtls-lsp`, `kotlin-lsp`, `swift-lsp`, `ruby-lsp`, `php-lsp`, `lua-lsp`, `csharp-lsp`, `clangd-lsp`), output-style plugins, and an `example-plugin` reference implementation.
- **`/external_plugins`** — third-party plugins from partners/community (15 directories at HEAD) that pass a submission + quality/security review (via the [plugin directory submission form](https://clau.de/plugin-directory-submission)).

**Install model:** `/plugin install {plugin-name}@claude-plugins-official`, or browse `/plugin > Discover`. Each plugin follows the standard layout (`.claude-plugin/plugin.json`, optional `.mcp.json`, `commands/`, `agents/`, `skills/`, `README.md`). The marketplace also supports **skill-bundle entries** (`strict: false` + explicit `skills` array sourced from a `git-subdir`) so a third-party repo that ships bare `SKILL.md` files without a plugin manifest can still be curated in. Each bundled skill registers as `<plugin-name>:<skill-name>`.

## How we tested it

**Source-grounded inspection via the GitHub API — not installed, no plugins installed from it in this session.** I fetched repo metadata (`gh api repos/anthropics/claude-plugins-official`), read the full marketplace `README.md`, enumerated the plugin trees, and counted the internal/external split. I did **not** run `/plugin install` or exercise any member plugin in this session. The individual member plugins (`security-guidance`, `skill-creator`) were assessed in their own evaluations (the latter against the locally-installed artifact); this entry relies on those and on the marketplace repo's own files. No detection rates, install success rates, or other metrics are invented.

```bash
gh api repos/anthropics/claude-plugins-official  # stars 30445, Apache-2.0, pushed 2026-06-19, topics: claude-code, mcp, skills
gh api repos/anthropics/claude-plugins-official/contents/README.md --jq '.content' | base64 -d
gh api 'repos/anthropics/claude-plugins-official/git/trees/HEAD?recursive=1' --jq '.tree[].path' | grep -E '^plugins/[^/]+/?$'        # 37 internal plugins
gh api 'repos/anthropics/claude-plugins-official/git/trees/HEAD?recursive=1' --jq '.tree[].path' | grep -cE '^external_plugins/[^/]+/?$' # 15 external plugins
gh api 'repos/anthropics/claude-plugins-official/git/trees/HEAD?recursive=1' --jq '.tree[].path' | grep -i marketplace.json            # .claude-plugin/marketplace.json
```

## What worked

- **Canonical first-party trust anchor.** This is *the* official source for `security-guidance`, `skill-creator`, `plugin-dev`, `code-review`, `pr-review-toolkit`, `commit-commands`, and `feature-dev` — several of which this catalog already rates ADOPT/KEEP. Installing from here is the lowest-supply-chain-risk path to those tools versus third-party mirrors (the `security-guidance` evaluation found numerous lookalike mirror repos; this repo is the genuine origin).
- **Curation + active maintenance.** 30k+ stars, pushed the same day as this evaluation, Apache-2.0, owned by the `anthropics` org. Internal plugins are maintained by Anthropic; external plugins pass a submission and quality/security review gate. That curation is the marketplace's core value — it raises the floor versus an open free-for-all registry.
- **Broad, loop-spanning catalog.** 37 internal + 15 external plugins cover Implement (`feature-dev`, `frontend-design`, the LSP family), Verify/Review (`code-review`, `pr-review-toolkit`, `code-simplifier`, `security-guidance`), Ship (`commit-commands`), and Reflect/meta (`skill-creator`, `plugin-dev`, `mcp-server-dev`, `agent-sdk-dev`, `hookify`). It is a one-stop discovery surface for the Claude Code ecosystem.
- **Honest, explicit trust disclaimer.** The README leads with a warning that users must trust a plugin before installing, that Anthropic does not control bundled MCP servers/files and cannot verify behavior or that it won't change. Correct expectation-setting for a registry that includes third-party code.
- **Flexible curation schema.** The skill-bundle (`strict: false`) mechanism lets the marketplace surface high-quality skills from repos that never adopted the plugin manifest format — pragmatic reach without forcing upstream restructuring.

## What didn't work or surprised us

- **It's a registry, not a tool — verdict applies to the channel, not its contents.** Adopting the marketplace says nothing about whether any *given* plugin is worth running. Each member tool needs its own evaluation (which is exactly why `security-guidance`, `skill-creator`, etc. have separate entries). The umbrella entry must not be read as a blanket endorsement of all 52 plugins.
- **External plugins carry real third-party risk.** The README's own warning is the tell: `/external_plugins` and skill-bundle entries can ship MCP servers and code Anthropic does not control and that may change after review. The curation gate reduces but does not eliminate supply-chain risk; treat external entries with the same scrutiny as any third-party dependency.
- **Harness-locked.** This is the Claude Code plugin system specifically (`/plugin install ...@claude-plugins-official`). The skills/plugins here are not portable to other agent harnesses without repackaging; teams off Claude Code get no benefit.
- **Quality is heterogeneous and version-fluid.** "High quality" is the stated bar, but 37 internal plugins range from production-grade (`security-guidance`, `skill-creator`) to references (`example-plugin`, `playground`). Plugins update independently; an install pins to whatever the source resolves to, so behavior can drift.
- **750 open issues.** A large issue backlog on the monorepo (expected at this scale/popularity) means individual plugin bugs may sit unaddressed; not a defect of the marketplace concept but worth noting for reliance planning.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (indirect) | Curated channel to correctness-improving plugins (`code-review`, `security-guidance`, `pr-review-toolkit`); the marketplace itself does nothing to code, its contents do. |
| Speed | + (indirect) | One-command discovery + install (`/plugin install`) is faster than hunting/vetting individual repos; member tools (`feature-dev`, LSP plugins) speed the loop. |
| Maintainability | + | First-party source means installs track the official API and stay current; reduces drift versus pinning random third-party mirrors. |
| Safety | mixed | First-party internal plugins are low-risk and Apache-2.0; external plugins carry third-party supply-chain risk the README explicitly disclaims. Curation helps, trust-verification still on the user. |
| Cost Efficiency | neutral | The marketplace is free; cost is whatever member plugins incur (e.g. `security-guidance`'s per-turn LLM review). The channel adds none. |

## Verdict

**KEEP (as the catalog's umbrella entry) — ADOPT as the install source for first-party plugins.**

claude-plugins-official is the canonical, Anthropic-managed marketplace and the genuine origin of multiple plugins this catalog already rates ADOPT/KEEP (`security-guidance`, `skill-creator`, plus `plugin-dev`, `code-review`, `pr-review-toolkit`, `commit-commands`, `feature-dev`). As a *trust anchor and distribution channel* it is the right place to get those tools: first-party, Apache-2.0, actively maintained, with an honest disclaimer and a curation gate that raises the baseline. It earns **KEEP** because it belongs in the catalog as the umbrella source rather than a tool to "try," and **ADOPT for installing internal plugins** because that is the lowest-supply-chain-risk path to the first-party tools already endorsed here.

The verdict is deliberately scoped to the *channel*, not its contents: the marketplace is not itself a tool, so it cannot be ADOPT-as-a-tool. Each member plugin must be evaluated on its own merits — which this catalog does. Treat `/external_plugins` and skill-bundle entries with normal third-party-dependency scrutiny (the README says as much: Anthropic does not control or verify them). Off-Claude-Code teams get nothing from it.

**vs. overlaps:**
- **Member plugins evaluated individually** (`security-guidance`, `skill-creator`, `plugin-dev`, `code-review`, `pr-review-toolkit`, `commit-commands`, `feature-dev`) — this entry is their *parent/source*, not a competitor. Cross-reference: install them from here.
- **Third-party / community plugin registries** (skills.sh, community marketplaces) — this is the *first-party* equivalent; prefer it for the official tools, use community registries for breadth this one deliberately doesn't curate.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-plugins-official](https://github.com/anthropics/claude-plugins-official) | platform | Anthropic's official, curated Claude Code plugin marketplace (37 internal + 15 external plugins) — the canonical first-party source installed via `/plugin install {name}@claude-plugins-official` | Where to discover and trustably install official Claude Code plugins without supply-chain risk from third-party mirrors | Houses individually-evaluated members (security-guidance, skill-creator, plugin-dev, code-review, pr-review-toolkit, commit-commands, feature-dev); first-party counterpart to community plugin registries (skills.sh) |
