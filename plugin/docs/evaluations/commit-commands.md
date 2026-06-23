# Evaluation: commit-commands

**Repo:** [anthropics/claude-plugins-official](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands)
**Stars:** 30,444 (monorepo) | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Ship
**Layer:** Process

---

## What it does

Catalog one-liner: "Git workflow shortcuts: clean_gone, commit, commit-push-pr." It is a tiny official Anthropic plugin distributed inside the `claude-plugins-official` marketplace monorepo. It contributes exactly three slash commands and no agents, hooks, or MCP servers:

- **`/commit`** — gathers `git status`, `git diff HEAD`, current branch, and `git log --oneline -10` via command-frontmatter context injection, then instructs Claude to stage relevant files and create one commit whose message matches the repo's existing style.
- **`/commit-push-pr`** — same context, then a 5-step task: branch off main if needed, commit, push to origin, and open a PR via `gh pr create`.
- **`/clean_gone`** — runs `git branch -v` / `git worktree list`, then a one-liner pipeline (`grep '\[gone\]' | sed | awk | while read`) that removes worktrees for and `git branch -D` deletes every branch whose upstream is `[gone]`.

Mechanically these are just markdown command files. The `commit` and `commit-push-pr` commands use the `allowed-tools` frontmatter to pre-scope Bash to specific git/gh subcommands, and use `!` backtick context blocks so the diff/status/log are embedded in the prompt before Claude acts. There is no enforcement layer — the commands are prompt scaffolding that front-loads the right git context and tells Claude to do the work in a single tool-batched response.

## How we tested it

**Evidence:** REVIEW

Source review of the plugin **as installed on this machine** — it is already present under `~/.claude/plugins/` (both the marketplace checkout and the cache), so this is the real shipped artifact, not a README paraphrase. I read the three command `.md` files and the plugin README/`plugin.json` directly, and confirmed the marketplace source and repo identity via the marketplace manifest and git remote. I did **not** execute `/commit`, `/commit-push-pr`, or `/clean_gone` against a working tree in this session (running them would mutate git state / open a PR), so behavioral claims rest on reading the command definitions, which are short and fully transparent.

```bash
# Repo identity confirmed (catalog entry was UNLINKED):
gh search repos commit-commands claude            # surfaced mirrors of anthropics-...-commit-commands
find ~/.claude/plugins -ipath '*commit-commands*' -name '*.md'   # plugin installed locally
git -C ~/.claude/plugins/repos/claude-plugins-official remote -v # -> anthropics/claude-plugins-official.git
gh api repos/anthropics/claude-plugins-official -q '{full_name,license,stars:.stargazers_count}'  # 30444, Apache-2.0
# Read the actual command files:
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/commit-commands/commands/{commit,commit-push-pr,clean_gone}.md
~/.claude/plugins/marketplaces/claude-plugins-official/plugins/commit-commands/{README.md,.claude-plugin/plugin.json}
```

Repo verification: confirmed. The plugin ships from `anthropics/claude-plugins-official` (the README homepage URL `claude-plugins-public` redirects to the same repo). It is the exact source of the three command names in the catalog entry.

## What worked

- **Official, trustworthy, and actively maintained.** Apache-2.0, authored by Anthropic, inside the 30k-star official marketplace pushed the same day as this evaluation. No bus-factor or supply-chain concern of the kind that dogs solo-author plugins.
- **Correctly scoped tool permissions.** `commit` and `commit-push-pr` declare narrow `allowed-tools` (`git add/status/commit/push`, `git checkout --branch`, `gh pr create`) rather than blanket Bash — a clean, least-privilege command design worth imitating.
- **Good context front-loading.** Injecting `git status` + `git diff HEAD` + branch + recent log into the prompt before asking for a commit is the right pattern; it matches commit messages to repo style and is exactly how a careful human would prime the model.
- **`/clean_gone` is the one genuinely additive piece.** Pruning `[gone]` branches *and their worktrees* is a fiddly, easy-to-get-wrong maintenance task that the user's own shorthand does not cover. This is the part with real marginal value.
- **Zero install footprint risk.** Three markdown files, no hooks, no SessionStart mutation, no external services — nothing to conflict with the user's existing `~/.claude` hook stack (OMEGA, etc.).

## What didn't work or surprised us

- **Largely redundant with the user's own CLAUDE.md shorthand.** The user already defines a "git add commit push" shorthand (review status+diff, stage specific paths not `git add -A`, Conventional Commits, push current branch, PR only on request, deploy only on request). `/commit` and `/commit-push-pr` cover the same ground with *less* nuance — they don't encode the user's "specific paths not `-A`" or "PR only when asked" rules.
- **Hard-codes attribution the user disables.** The README says `/commit` and `/commit-push-pr` "include Claude Code attribution in the commit message" — directly contradicting the user's global setting (attribution disabled via `~/.claude/settings.json`). Adopting these commands as-is would reintroduce unwanted attribution noise.
- **`/commit-push-pr` opens a PR unconditionally.** The user's shorthand only opens a PR on explicit "draft pr"/"open pr". This command always runs `gh pr create`, which is more aggressive than the user's workflow.
- **The PR description quality lives entirely in the prompt.** Unlike the user's git-workflow rule (analyze full commit history, `git diff base...HEAD`, test plan with TODOs), `/commit-push-pr` only injects `git diff HEAD` of the working tree, not the full branch range — so PR summaries can miss earlier commits on the branch.
- **No tests, no enforcement, nothing to verify.** It is prompt scaffolding; there is no deterministic guarantee, so it inherits all the model's commit-message variance.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Front-loaded diff/status/log helps message accuracy, but no enforcement; behavior == model behavior |
| Speed | + | One slash command replaces the manual status→diff→stage→commit→push→`gh pr create` sequence (the core value, for Ship-stage git ops) |
| Maintainability | + | `/clean_gone` reliably prunes stale `[gone]` branches + worktrees; consistent commit cadence |
| Safety | neutral | Narrow `allowed-tools` is good; but `/clean_gone` force-removes worktrees and `git branch -D` (hard delete) — fine for `[gone]` branches, but no confirmation step |
| Cost Efficiency | neutral | Trivial token cost; no measurable efficiency gain or loss |

## Verdict

**SKIP (KEEP existing setup)**

For this user specifically, the plugin is redundant rather than additive. The user's own CLAUDE.md already implements a more nuanced "git add commit push" shorthand (specific-path staging, Conventional Commits, PR-only-on-request, deploy-only-on-request) and globally disables Claude Code attribution — which `/commit` and `/commit-push-pr` would reintroduce. Installing them would *downgrade* the existing convention and conflict with two explicit user preferences. The honest recommendation is to keep the current shorthand and not install the plugin wholesale.

It earns SKIP rather than a hard reject only because the source is impeccable (official Anthropic, Apache-2.0, 30k-star monorepo, narrow tool scoping) and `/clean_gone` is the one piece with genuine marginal value the user's shorthand lacks — branch+worktree pruning. A reasonable middle path is to lift just the `clean_gone` command (or its sed/awk pipeline) into the user's own setup rather than adopt the plugin. Versus **claude-code-action** the relationship in the catalog holds and is complementary, not competing: commit-commands runs git ops locally and interactively at the Ship stage, whereas claude-code-action runs in CI/GitHub Actions; one does not substitute for the other.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [commit-commands](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/commit-commands) | plugin | Official Anthropic plugin: three git slash commands — `/commit`, `/commit-push-pr`, `/clean_gone` | Reduces context-switching for routine commit/push/PR and stale-branch cleanup at the Ship stage | claude-code-action (complementary: commit-commands = local, CCA = CI); overlaps a user's own commit shorthand |
