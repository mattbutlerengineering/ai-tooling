# Evaluation: vercel-labs-skills (`npx skills`)

**Repo:** [vercel-labs/skills](https://github.com/vercel-labs/skills)
**Stars:** 28,034 | **Last updated:** 2026-08-04 (pushed; created 2026-01-14) | **License:** MIT <!-- was `none declared` at eval time; MIT LICENSE added upstream, re-checked 2026-08-04 -->
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Pre-loop / cross-cutting — it is the *acquisition* mechanism that gets skills into whatever tool you run for every stage. It does not itself participate in Plan/Implement/Verify; it provisions the skills that do.
**Layer:** Tooling (an npm CLI that resolves a source, parses `SKILL.md` files, and symlinks or copies them into each agent's skills directory; plus a telemetry/registry backend)

---

## What it does

`npx skills` is the reference CLI for the "open agent skills ecosystem" — a cross-tool installer and lifecycle manager for `SKILL.md`-format skills. The package is literally named `skills` (v1.5.12) and ships a second bin alias, **`add-skill`**, confirming it is the rebranded successor to the `npx add-skill` installer the catalog already references via skills.sh. It claims support for **OpenCode, Claude Code, Codex, Cursor and "68 more"** agents (72 total), each with its own skills directory layout that the CLI knows how to target.

The command surface is broad for an installer: `add` (install from GitHub shorthand, full URL, direct skill path, GitLab, any git URL, or local path), `use` (run one skill without installing — writes to a temp dir and pipes a generated prompt to `claude`/etc.), `list`/`ls`, `find` (interactive or keyword search against the registry), `remove`, `update`, and `init` (scaffold a new `SKILL.md`). Install can be project-scoped (`./<agent>/skills/`, committed with the repo) or global (`-g`, `~/<agent>/skills/`), and defaults to **symlinking** all agents to one canonical copy (with `--copy` as the fallback when symlinks aren't supported). Flags cover multi-agent fan-out (`-a claude-code -a opencode`), skill selection (`-s`, `'*'`), and full non-interactive CI use (`-y`, `--all`). The `src/` tree shows real engineering: a `providers/` registry (`wellknown.ts`, GitHub/GitLab/Mintlify/HuggingFace source types), `source-parser`, `frontmatter`, `skill-lock`/`local-lock` lockfiles, `detect-agent`, and a Vitest suite alongside most modules.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No `npx skills` command was executed; nothing was installed, symlinked, or piped to an agent. Every claim comes from the repository (GitHub metadata, README, `package.json`, recursive file tree, and `src/telemetry.ts`), not from observed CLI behavior. The "72 agents" and command behaviors are the README's and source's own descriptions, not anything I exercised.

```bash
gh api repos/vercel-labs/skills --jq '{desc,stars:.stargazers_count,pushed:.pushed_at[0:10],created:.created_at[0:10],license:.license.spdx_id}'  # 22,937; license null
gh api repos/vercel-labs/skills/readme --jq '.content' | base64 -d | head -120
gh api "repos/vercel-labs/skills/git/trees/HEAD?recursive=1" --jq '.tree[].path'        # bin/cli.mjs, src/*, providers/
gh api repos/vercel-labs/skills/contents/package.json --jq '.content' | base64 -d        # name "skills", bin: skills + add-skill, v1.5.12
gh api repos/vercel-labs/skills/contents/src/telemetry.ts --jq '.content' | base64 -d    # phones add-skill.vercel.sh on every op
gh api repos/vercel-labs/skills/releases --jq 'length'  # 30 (page cap); forks 1848; open issues 743
```

## What worked

- **Genuinely cross-tool, genuinely git-native.** Resolves GitHub shorthand, full URLs, a direct path to one skill in a repo, GitLab, arbitrary git URLs, and local paths — and targets 70+ agents from one command. This is the most general skills installer I have inspected; it makes the `SKILL.md` format portable in practice, not just in theory.
- **Real lifecycle, not just install.** `update`, `remove`, lockfiles (`skill-lock`/`local-lock`), and `--list` mean skills can be maintained over time rather than copied once and forgotten. `init` scaffolds new skills. `use` lets you try a skill without polluting any directory.
- **Symlink-by-default is the right call.** A single canonical copy with symlinks into each agent's directory avoids the N-copies drift that plagues per-tool installs (e.g. openskills' copy approach), with `--copy` as an honest fallback.
- **Vercel-grade engineering and traction.** 22.9K stars in ~5 months, ~1.8K forks, a providers/registry abstraction, and Vitest coverage across most `src/` modules. CI/husky/prettier in place. This is a maintained tool, not a weekend script.
- **CI-friendly.** `-y`/`--all`/`-g` and explicit agent/skill selection make it scriptable for repo bootstrap and team onboarding.

## What didn't work or surprised us

- **It phones home on every operation.** `src/telemetry.ts` posts to `https://add-skill.vercel.sh/t` (and an `/audit` endpoint) on `install`, `remove`, `update`, and `find`, sending the source, skill names, agent names, scope, and even a JSON map of skill→path. **Update (verified in source):** an opt-out *does* exist — `isEnabled()` returns false when `DO_NOT_TRACK` or `DISABLE_TELEMETRY` is set, and telemetry auto-disables under CI (`CI`, `GITHUB_ACTIONS`, `GITLAB_CI`, `CIRCLECI`, …). So the flow is real and undisclosed in the README, but it honors the standard `DO_NOT_TRACK=1` convention and is already off in CI — the remaining issue is documentation, not the absence of a control.
- **~~No license file.~~ Resolved 2026-08-04.** At eval time `license` was `null` in the GitHub metadata — a 22.9K-star tool you were asked to pipe into `claude` with no declared license terms, a real adoption blocker for any org with license hygiene. Upstream has since added an **MIT** LICENSE (re-checked against `gh api` 2026-08-04, ★28.0K). The blocker is gone; the telemetry reservation below is not.
- **`skills use ... | claude` is arbitrary remote prompt execution.** `use` fetches a third-party skill to a temp dir and pipes its generated prompt straight into your agent. The convenience is real; so is the supply-chain surface — you are trusting whatever `owner/repo` resolves to, with no validation step. (Contrast tech-leads-club/agent-skills, which sells *validated* skills.)
- **743 open issues.** High traction brings a large, partly-unresolved backlog; "72 agents" support is breadth that is hard to keep all working.
- **It is plumbing, not value.** `skills` moves files; it produces zero quality improvement on its own. Its worth is entirely downstream — only as good as the collections you point it at (e.g. its sibling vercel-labs/agent-skills).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Installs skills; does not change code quality itself. Any correctness gain comes from the skills it delivers, not the installer. |
| Speed | + | One command to add/update/remove skills across 70+ tools, project- or global-scoped, scriptable in CI — far faster than manual copy-into-each-tool. |
| Maintainability | + | Lockfiles + `update`/`remove` + symlink-to-canonical-copy keep installed skills maintainable and drift-free across tools. |
| Safety | − / neutral | Telemetry to `add-skill.vercel.sh` on every op (undocumented in README, but opt-out via `DO_NOT_TRACK`/`DISABLE_TELEMETRY` and auto-off in CI); ~~no license declared~~ (MIT as of 2026-08-04); `use`/`add` execute/install arbitrary remote skill content with no validation gate. |
| Cost Efficiency | neutral | The CLI itself adds no token cost; downstream skill quality determines token spend. |

## Verdict

**discovery-log — tentative read: the best general-purpose skills installer here, but vet the telemetry and license before scripting it into CI.** `npx skills` (a.k.a. `add-skill`) is the most capable cross-tool skill installer in the catalog: git-native source resolution, 70+ agents, real lifecycle commands, lockfiles, and symlink-by-default, all Vercel-engineered and heavily starred. The reservations are governance, not capability — telemetry on every install/remove/update/find to a Vercel endpoint (undocumented in README, but suppressible with `DO_NOT_TRACK=1`/`DISABLE_TELEMETRY=1` and already off in CI), and — at eval time — no declared license. **The license half of that reservation is now resolved:** upstream added an MIT LICENSE, re-checked 2026-08-04. Use it for ad-hoc `add`/`use` against sources you already trust and set `DO_NOT_TRACK=1`; the remaining pre-CI question is telemetry, not licensing.

Compared to neighbors: **openskills** is a simpler universal loader (copy-based, fewer agents, no registry/telemetry) — lighter and quieter but less capable. **buildwithclaude** is a discovery *hub* (find skills), not an installer; `skills` is the install/lifecycle layer that pairs with it (buildwithclaude already lists skills.sh, the registry this CLI fronts). **claude-code-templates** is a component installer/marketplace with an analytics dashboard but is Claude-Code-centric; `skills` wins on cross-tool breadth and git-native sourcing. **tech-leads-club/agent-skills** sells *validated* skills — the safety property `skills` conspicuously lacks at the installer layer.

## Triage note

Left at `discovery-log` — **and this lead was queued for elimination until the license was
re-checked.** `repo-metadata.json` recorded `license_spdx: NONE`, and a no-license entry is a
disposal under this repo's adoption bar. A fresh `gh api repos/vercel-labs/skills` on 2026-08-04
returns **MIT**: upstream added a LICENSE file after the eval was written. The metadata record, this
eval's header, its "What didn't work" bullet, its Safety row, and its verdict have all been corrected.

That makes this the pass's headline finding: **a cached license value is a snapshot, and acting on a
stale `NONE` produces a false SKIP with a real justification attached to it.** `--metadata-staleness`
ages the whole snapshot but cannot flag one record that flipped, and this record was well inside the
120-day threshold. The general lesson is to re-fetch before disposing *on* a license, not to distrust
the cache for banding.

The eval's remaining reservation is telemetry (`add-skill.vercel.sh` on every operation, opt-out via
`DO_NOT_TRACK=1`, auto-off in CI), which is a condition to satisfy rather than a ground to eliminate.

_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [vercel-labs/skills](https://github.com/vercel-labs/skills) | tool | `npx skills` — cross-tool installer/lifecycle CLI for SKILL.md skills (add/use/update/remove across 70+ agents, git-native sources, symlink-by-default); the `add-skill` successor behind skills.sh | Installing and maintaining agent skills is per-tool, manual, and drift-prone; need one git-native command across every editor | openskills, claude-code-templates, buildwithclaude (skills.sh registry), antigravity-awesome-skills (CLI installer) |
