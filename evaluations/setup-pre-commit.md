# Evaluation: setup-pre-commit

**Repo:** [mattpocock/skills](https://github.com/mattpocock/skills/tree/main/skills/misc/setup-pre-commit)
**Stars:** 274,584 (the container, `mattpocock/skills`; the skill has no count of its own) | **Last updated:** 2026-09-29 | **License:** MIT
**Last verified:** 2026-10-02
**Dev loop stage:** Verify
**Layer:** Infrastructure

---

## What it does

Sets up Husky pre-commit hooks with lint-staged (Prettier), type checking and tests in the current repo. It is one skill inside `mattpocock/skills` (`skills/misc/setup-pre-commit/SKILL.md`, plus an `agents/openai.yaml` that only supplies a display name for Codex). skills.sh listed **411K installs** on 2026-10-02, the most-installed verification-adjacent skill in this scan.

The mechanism is an eight-step recipe, not a discipline: detect the package manager from the lockfile (npm default), install `husky lint-staged prettier` as devDependencies, `npx husky init`, write `.husky/pre-commit` as three lines (`npx lint-staged`, `npm run typecheck`, `npm run test`, with the package manager swapped in and missing scripts dropped *and reported to the user*), write `.lintstagedrc` as `{"*": "prettier --ignore-unknown --write"}`, write a `.prettierrc` only if no Prettier config exists, run a four-item verify checklist ending in `npx lint-staged`, and commit, so the first commit goes through the new hook as a smoke test.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — not run hands-on. I read the whole `SKILL.md` and its `agents/openai.yaml` through the GitHub API and compared it against the container's existing eval ([mattpocock-skills.md](mattpocock-skills.md)) and this repo's own commit gate (`make check-data`, called from both commit hooks). Nothing was installed, and no repo was set up with the hooks. The skill is a deterministic recipe, so its output can be read straight from the source. What a read cannot settle is how often an agent skips the "omit and tell the user" branch.

```bash
gh api repos/mattpocock/skills --jq '{stars:.stargazers_count, license:.license.spdx_id, pushed:.pushed_at}'
gh api repos/mattpocock/skills/contents/skills/misc/setup-pre-commit --jq '.[].path'
gh api repos/mattpocock/skills/contents/skills/misc/setup-pre-commit/SKILL.md --jq .content | base64 -d
gh api repos/mattpocock/skills/contents/skills/misc/setup-pre-commit/agents/openai.yaml --jq .content | base64 -d
```

## Test design — skills

- **Triggering:** not measured — no should-fire / shouldn't-fire prompt set was built.
- **Output A/B:** not measured — no with-skill vs baseline A/B; every finding below is from reading the source.
- **Not run?** Yes — see the disclaimer above.

## What worked

- **It turns a Verify-stage intention into a deterministic gate.** The other skills in this scan ask the agent to *behave* (test first, verify before claiming). This one installs something that keeps firing when nobody remembers to ask, which makes the gate easy to check: `.husky/pre-commit` is a three-line file.
- **Staged-only formatting comes first and the slow checks come after.** lint-staged plus `prettier --ignore-unknown` only touches staged files and skips binaries. Typecheck and tests run after, a sensible order for cost.
- **Honest about missing scripts.** If `package.json` has no `typecheck` or `test` script, the line is dropped and the user is told. It does not invent a script.
- **It doesn't overwrite your config.** `.prettierrc` is written only when no Prettier config exists.

## What didn't work or surprised us

- **JavaScript/TypeScript only.** Husky, lint-staged and Prettier assume a `package.json`. A Python, Go or Rust repo gets nothing, and the description doesn't say so.
- **Full test suite on every commit.** `npm run test` in a pre-commit hook gets expensive on a big repo, and the usual response is `--no-verify`, which defeats the gate. The skill offers no "fast subset" option.
- **It commits for you.** Step 8 stages "all changed/created files" and commits with a fixed message. In a dirty working tree that can sweep unrelated changes into the setup commit.
- **Its own "verify" step only checks that the hook is set up.** The checklist confirms the files exist and that `npx lint-staged` runs. It never confirms that typecheck or tests pass on the current tree, so the first real commit can be where you find out.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Typecheck and tests become a commit-time gate instead of a step the agent may skip |
| Speed | - | Full typecheck + full test suite per commit adds latency that grows with the repo |
| Maintainability | + | Consistent formatting via lint-staged; config files are small and conventional |
| Safety | neutral | Installs three well-known npm devDependencies; the auto-commit step can over-stage a dirty tree |
| Cost Efficiency | + | Cheap local gate catches type/test failures before CI or an agent turn spends tokens on them |
| Verifiability | + | The gate is a three-line file plus a JSON config; anyone can read exactly what runs |

## Verdict

**SKIP** — ships inside `mattpocock/skills`. Installing the container settles it, since it is a component of that artifact and not a competitor to it.

The review above is kept as color. As a skill it is a solid, narrow recipe for JS/TS repos. Commit-time gating is the right instinct, and it is the same one this repo applies with `make check-data` in both commit hooks. Its limits (JS-only, full suite per commit, an auto-commit that can over-stage) are things a human should know before letting an agent run it. None of them is a reason to install it separately from the pack.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [setup-pre-commit](https://github.com/mattpocock/skills/tree/main/skills/misc/setup-pre-commit) | skill | Sets up Husky + lint-staged pre-commit hooks running Prettier, typecheck and tests | Agents and humans commit unformatted, type-broken or test-failing code because nothing gates the commit | husky (ext.), lint-staged (ext.), tdd-guard |
