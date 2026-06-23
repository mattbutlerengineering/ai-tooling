# Evaluation: opensrc

**Repo:** [vercel-labs/opensrc](https://github.com/vercel-labs/opensrc)
**Stars:** 2,590 | **Last updated:** 2026-05-01 (latest release v0.7.2, 2026-04-18) | **License:** Apache-2.0
**Dev loop stage:** Implement (reading dependency internals while writing code) — touches Plan when modeling against a library's API and Review when verifying agent-written usage against real source
**Layer:** Tooling (a CLI the agent composes with `rg`/`cat`/`find`; not infrastructure, not a hosted service)

---

## What it does

Fetch source code for npm packages (and PyPI, crates.io, GitHub, GitLab, Bitbucket) to give AI coding agents deeper dependency context. The mechanism is a small native **Rust CLI** distributed over npm. The load-bearing command is `opensrc path <package>`: it resolves the package to its source repository, shallow-clones it at the correct version tag, caches it globally under `~/.opensrc/`, and prints the absolute path to stdout. Because the path goes to stdout and progress to stderr, you compose it inside any shell tool:

```bash
rg "parse" $(opensrc path zod)
cat $(opensrc path zod)/src/types.ts
find $(opensrc path pypi:requests) -name "*.py"
```

The resolution pipeline (from the docs "How It Works"): registry lookup → extract the `repository` field from `package.json` → map the version to a git tag → `git clone --depth 1 --branch <tag>` → cache at `~/.opensrc/repos/<host>/<owner>/<repo>/<version>/`, tracked in `sources.json`. The differentiator is **version detection**: for npm it reads `node_modules/<pkg>/package.json`, then `package-lock.json`, `pnpm-lock.yaml`, `yarn.lock`, falling back to the registry `latest`. So the cached source matches the version the project actually resolves, not whatever the model memorized or whatever the library's docs site currently shows.

It is **not** an MCP server and has no hosted endpoint. Claude Code integration is by convention: the repo ships an agent skill (moved to a top-level `skills/` directory in v0.7.2, #46) plus an `AGENTS.md` snippet — wrapped in `<!-- opensrc:start -->` markers — that tells the agent the cache location and how to invoke `opensrc fetch` / `opensrc path`. Other commands: `fetch` (pre-warm the cache, no path output, for CI/scripts), `list`, `remove`, `clean`. Private repos authenticate via `GITHUB_TOKEN` / `GITLAB_TOKEN` / `BITBUCKET_TOKEN` read from the environment per run; nothing is persisted to disk.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I examined the GitHub repo metadata, the root README, the CLI README (`packages/opensrc/README.md`), `AGENTS.md`, `CHANGELOG.md`, and the docs MDX pages for commands, how-it-works, and authentication. I read the CLI source tree layout (`packages/opensrc/cli/src/` — `commands/{fetch,path,list,remove,clean}.rs`, `core/{cache,fetcher,git,version}.rs`, `core/registries/{npm,pypi,crates,repo}.rs`) to confirm the registries, lockfile parsers, and resolution flow described in the docs are actually implemented, not aspirational. I did not install the binary, run `opensrc path`, or measure cache or clone timings — no performance numbers below are invented.

```bash
gh api repos/vercel-labs/opensrc --jq '{stars,license,description,pushed_at,created_at}'
gh api repos/vercel-labs/opensrc/readme --jq '.content' | base64 -d
gh api repos/vercel-labs/opensrc/contents/packages/opensrc/README.md --jq '.content' | base64 -d
gh api repos/vercel-labs/opensrc/contents/AGENTS.md --jq '.content' | base64 -d
gh api repos/vercel-labs/opensrc/contents/CHANGELOG.md --jq '.content' | base64 -d
gh api "repos/vercel-labs/opensrc/contents/apps/docs/src/app/how-it-works/page.mdx" --jq '.content' | base64 -d
gh api "repos/vercel-labs/opensrc/contents/apps/docs/src/app/auth/page.mdx" --jq '.content' | base64 -d
gh api "repos/vercel-labs/opensrc/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/vercel-labs/opensrc/releases --jq '.[] | {tag,published:.published_at}'
# Catalog overlap scan:
grep -inE "opensrc|git-mcp|context7|deepwiki|npm.*source" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **Reading actual installed source is a genuine anti-hallucination win, and the strongest form of grounding available.** Docs (context7) and repo browsing (git-mcp) tell the agent what an API *should* do; opensrc lets the agent read what the dependency *actually does* — the real implementation, including undocumented behavior, edge cases, and the exact version's quirks. For "why is this dependency throwing / behaving like this," nothing beats grepping its source. This is the failure mode the catalog names: agents guessing dependency internals from training data instead of reading the code.
- **Version-pinned to the project's resolved tree.** Detecting the version from lockfiles / `node_modules` and cloning that exact tag is the real differentiator. Training data and docs sites drift; a `git clone --branch v3.24.1` does not. This directly attacks the "agent assumes a newer/older API than is installed" class of bug.
- **Composes with the tools the agent already uses.** Output is just a path on stdout, so `rg`/`cat`/`find`/`grep` work unchanged. No MCP server to register, no new tool protocol, no token-heavy resource listing — the agent searches a real directory the same way it searches the repo. This is a clean, low-ceremony design.
- **Genuinely multi-registry, despite the npm-centric framing.** npm, PyPI, crates.io, plus direct GitHub/GitLab/Bitbucket `owner/repo`. The catalog one-liner ("npm package source") undersells it — the value extends to Python and Rust projects too. (Version *detection from lockfiles* is npm-only; other registries fall back to latest or an explicit `@version`.)
- **Strong authorship and engineering signals.** Vercel Labs, Apache-2.0, rewritten in Rust in v0.7.0 (~10x faster startup per the changelog), 7 cross-platform binaries, CI with clippy/fmt/test, a real docs site, and a steady release cadence through April 2026. Credible maintenance, not a weekend script. The shallow global cache (`~/.opensrc/`, shared across projects, `git clone --depth 1`) is a sensible performance design.
- **Safe by construction for the read path.** It only clones and reads source; it never executes dependency code, runs migrations, or touches a live system. Tokens are env-only and never written to disk.

## What didn't work or surprised us

- **It is `vercel-labs` (a Labs/experimental org), and pre-1.0.** v0.7.2 with 22 open issues. The core flow is well-built, but it carries normal early-stage risk: APIs and cache layout still shift (the v0.7.0 release moved from per-project `opensrc/` to a global `~/.opensrc/` and renamed the token env vars from `OPENSRC_GITHUB_TOKEN` to `GITHUB_TOKEN`). Pin expectations to a version.
- **Integration is by convention, not a one-command install.** There is no `opensrc init` that wires up Claude Code; you paste the `AGENTS.md` block (or install the bundled skill) yourself so the agent knows the tool and cache exist. Without that prompt scaffolding, the agent won't reach for it. Lower-friction than an MCP server in some ways, higher-friction in that nothing is auto-discovered.
- **Resolution depends on each package publishing a usable `repository` field and matching git tags.** Packages with a missing/wrong `repository`, monorepo packages whose tag scheme doesn't match the published version, or builds that differ from the source repo (transpiled/bundled dist vs. `src/`) can resolve to the wrong place or fetch source that doesn't correspond to the installed artifact. The docs don't claim to read the actual `node_modules` tarball — they re-clone the upstream repo at a tag, which is *usually* but not *always* identical to what npm installed.
- **Disk and clone cost on cache miss.** Shallow clones are fast, but a large repo (e.g. cloning `vercel/next.js` to read one package) pulls the whole monorepo at that tag. Heavy dependency trees can accumulate real disk under `~/.opensrc/`. Mitigated by the global shared cache and `clean`, but worth noting versus a docs lookup that fetches kilobytes.
- **The agent still has to read efficiently.** Pointing an agent at a dependency's full source is a token-hungry invitation if it `cat`s whole files instead of `rg`-ing for the symbol it needs. The value depends on disciplined, targeted searching — the same skill that makes repo navigation cheap.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (strong) | Lets the agent read the real, version-pinned implementation of a dependency instead of guessing from training data or drifting docs — the most direct grounding against dependency-behavior hallucination. |
| Speed | neutral / + | Saves the human round-trip of "no, that's not how that library works" and the agent's trial-and-error against an unread API; offset by clone-on-miss latency and the need to search rather than read whole files. |
| Maintainability | neutral | Improves the *agent's* code (usage matches actual library behavior) but adds no project-level maintainability artifact; it's a read-time aid, not something that lives in the codebase beyond an AGENTS.md note. |
| Safety | + | Read-only: clones and reads source, never executes dependency code or touches a live system. Tokens are env-only, never persisted. |
| Cost Efficiency | neutral | Avoids wasted iteration on wrong-API assumptions, but pointing an agent at full dependency source can spend tokens if it reads broadly instead of grepping; net roughly even and usage-dependent. |

## Verdict

**CONDITIONAL**

opensrc targets a real, high-value failure mode — agents inventing dependency behavior from stale training data — and addresses it with the strongest grounding there is: reading the dependency's actual source, pinned to the version the project resolves. That is categorically deeper than docs lookup (context7) or generic repo browsing (git-mcp), and the version-from-lockfile detection is the feature that makes it more than `git clone` in a wrapper. It is well-engineered (Rust, multi-registry, sane global cache), Vercel-authored, and Apache-2.0. **Adopt it when you work in a dependency-heavy npm/PyPI/crates project and routinely hit "the agent doesn't actually know how this library works,"** wiring the `AGENTS.md` block or bundled skill so the agent reaches for it. It is **CONDITIONAL rather than ADOPT** because (1) it's a pre-1.0 `vercel-labs` project with a still-moving cache/API surface, (2) integration is manual prompt-scaffolding rather than a one-command setup, and (3) the value only lands when the agent searches source efficiently and the package's repo/tag metadata resolves cleanly. Not SKIP — for the right project this is a meaningfully better grounding lever than the doc-based alternatives.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [opensrc](https://github.com/vercel-labs/opensrc) | tool | CLI that fetches version-pinned dependency source (npm/PyPI/crates/GitHub) so agents read the real implementation, not training-data guesses | Agents guess at dependency behavior from training data instead of reading the actual installed source | Complementary: context7 = library docs, git-mcp = live repo source, opensrc = version-pinned source matching the project's lockfile |
