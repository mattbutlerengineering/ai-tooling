# Evaluation: cc-safety-net

**Repo:** [kenryu42/cc-safety-net](https://github.com/kenryu42/cc-safety-net)
**Stars:** 1,405 | **Last updated:** 2026-06-19 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Implement / Ship (runtime guardrail, not post-hoc Review)
**Layer:** Infrastructure

---

## What it does

A coding-agent CLI hook that catches destructive git and filesystem commands before they execute. It registers a single `PreToolUse` hook on the `Bash` tool that runs `node dist/bin/cc-safety-net.js hook --claude-code`, semantically parses the command, and returns `{"hookSpecificOutput": {"permissionDecision": "deny", "permissionDecisionReason": "..."}}` to block the action before it runs. It targets one threat narrowly and deeply: irreversible data-loss commands (`git reset --hard`, `git checkout -- file`, `git push --force`, `git stash clear`, `git branch -D`, `rm -rf` of dangerous targets, `find -delete`, `xargs rm -rf`, `dd`/`mkfs` on block devices, `shred`). It ships for seven agents (Claude Code, Codex, Gemini CLI, Copilot CLI, Kimi Code, OpenCode, Pi).

The mechanism that distinguishes it from a permission deny rule is **semantic command analysis** rather than wildcard string matching. The source (`src/core/git/rules.ts`) actually parses git option grammar — it knows `git checkout -b feature` creates a branch (allow), `git checkout --orphan` is safe (allow), but `git checkout -- file` and `git checkout <ref> <path>` discard/overwrite the working tree (block). It unbundles short flags (`rm -r -f` == `rm -rf`), normalizes whitespace and command basename (`/usr/bin/git` → `git`), recursively unwraps shell wrappers up to 10 levels (`sh -lc 'rm -rf /'`), and (in paranoid mode) inspects interpreter one-liners (`python -c 'os.system("rm -rf /")'`). For `rm -rf` it is path-aware: it allows ephemeral/cwd targets (`/tmp`, `$TMPDIR`, `./build`) and blocks root/home/parent/absolute targets — so it is not a blanket `rm -rf` block. Custom rules (rulebook JSON) let teams add their own command blocks; failures fail closed.

## How we tested it

**Evidence:** REVIEW

Source-grounded review — **not installed or run hands-on**. No command was actually blocked live, so no block output, timing, or false-positive rate below is observed; all behavior is read from the documented spec plus the TypeScript source, not measured. I confirmed the decisive catalog question (does it move Safety, and is its net-new value meaningful over Claude Code's built-in permission classifier and over agentlint / hol-guard?) from the integration mechanism and the rule logic in source, which is sufficient to settle the verdict.

```bash
gh api repos/kenryu42/cc-safety-net --jq '{stars,license:.license.spdx_id,description,pushed_at,created_at}'
gh api "repos/kenryu42/cc-safety-net/git/trees/main?recursive=1" --jq '.tree[].path'
gh api repos/kenryu42/cc-safety-net/contents/README.md --jq '.content' | base64 -d
gh api repos/kenryu42/cc-safety-net/contents/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/kenryu42/cc-safety-net/contents/.claude-plugin/plugin.json --jq '.content' | base64 -d
gh api repos/kenryu42/cc-safety-net/contents/src/bin/hook/claude-code.ts --jq '.content' | base64 -d
gh api repos/kenryu42/cc-safety-net/contents/src/core/git/rules.ts --jq '.content' | base64 -d
gh api repos/kenryu42/cc-safety-net/contributors --jq '.[] | {login,contributions}'
gh api repos/kenryu42/cc-safety-net/releases --jq '.[0:3]'
```

Confirmed mechanism: `hooks/hooks.json` registers exactly one `PreToolUse` hook with matcher `Bash`. `src/bin/hook/claude-code.ts` builds a deny output with `permissionDecision: 'deny'` and a `permissionDecisionReason` — genuine pre-execution prevention via Claude Code's hook permission decision, identical in shape to agentlint's blocking mechanism. `src/core/git/rules.ts` confirms real option-grammar parsing (distinct `CHECKOUT_OPTS_WITH_VALUE` / `CHECKOUT_KNOWN_OPTS_NO_VALUE` sets, per-form reason strings), not regex/wildcard — this is the load-bearing differentiator from permission deny rules.

Maturity signals: 1.4K stars, MIT, created 2025-12-25, pushed same day as evaluation. v1.0.6 plugin / 24 tags. CI + codecov badges and ~50 test files under `tests/` (e.g. `tests/core/rules-rm.test.ts`, `tests/core/analyze/fail-closed-repair.test.ts`, `tests/bin/hooks/claude-code-hook.test.ts`). Contributor graph is effectively solo: kenryu42 (619 commits) with one external human contributor (4 commits) — high bus-factor risk despite the high star count.

## What worked

- **Semantic parsing is the real differentiator, and it's in the source, not just the README.** `git checkout -b` (allow) vs `git checkout --` (block), flag-order normalization (`rm -r -f` == `rm -rf`), basename normalization, and recursive shell-wrapper unwrapping all defeat the documented bypass vectors of wildcard `Bash(...)` deny rules. This is a concrete, verifiable improvement over Claude Code's pattern-based permission matching.
- **Path-aware `rm -rf`** allows `/tmp`, `$TMPDIR`, and within-cwd targets while blocking root/home/parent/absolute — meaningfully lower false-positive rate than a blanket `rm -rf` deny rule that would block routine `rm -rf ./build`.
- **Runs before the permission system.** PreToolUse hooks fire ahead of permission evaluation, so it is a genuine fallback even when deny rules are misconfigured — defense-in-depth, not a substitute.
- **Honest, well-reasoned positioning.** The README's "vs permission deny rules" and "vs sandboxing" tables are unusually candid (it states its own weakness: "analyzes command strings only," no network protection) and explicitly recommends running it *alongside* sandboxing and deny rules rather than replacing them.
- **Fail-closed defaults + audit logging + secret redaction.** Malformed hook input fails closed; blocked commands are logged to `~/.cc-safety-net/logs/`; block reasons redact secrets. Engineering discipline (CI, codecov, ~50 test files) is high for the category.
- **Custom rulebooks** with a test-fixture requirement (every rule needs a blocked fixture) make team-specific blocks (`terraform destroy`, `npm install -g`, `docker system prune`) verifiable.

## What didn't work or surprised us

- **Heavy overlap with Claude Code's built-in permission classifier.** Claude Code already prompts on `rm -rf`, force-push, and similar destructive Bash commands. cc-safety-net's net-new value is *not* "blocks dangerous commands" (the built-in does that) but "blocks them via semantic analysis that resists the bypass vectors wildcard/heuristic matching misses" and "blocks git footguns the sandbox considers safe-within-cwd." That is a narrower, but real, increment.
- **Narrow scope vs agentlint.** This is git/filesystem data-loss only — no secrets, no exfiltration, no malicious-URL, no supply-chain, no subagent auditing, no code-quality rules. agentlint's 77 rules cover far more ground; cc-safety-net does one thing.
- **Solo-maintainer bus factor.** 1.4K stars but one human author with 619 of ~640 commits. Adoption signal is strong; sustainability signal is weak. (Contrast: stars overstate resilience here.)
- **No network or exfiltration protection** (author states this) — so it does nothing for prompt-injection data theft, which is the higher-severity agent risk; sandboxing or agentlint's security pack is needed for that.
- **String-analysis ceiling.** It inspects command strings; a sufficiently obfuscated command (beyond 10 wrapper levels, dynamic eval, base64-decoded payloads) can still slip past. The author flags this as "lower bypass resistance" than OS sandboxing.
- **Node 18+ runtime dependency** invoked on every Bash tool call; per-call overhead is unmeasured here but is a Node process spawn per command.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Prevents accidental loss of uncommitted work, but doesn't make the agent's code more correct |
| Speed | neutral | Spawns a Node process per Bash call; overhead unmeasured but small; saves large time when it prevents a destructive mistake |
| Maintainability | neutral | No effect on code structure; custom rulebooks can enforce team git hygiene |
| Safety | + | Blocks irreversible git/filesystem data-loss commands pre-execution with bypass-resistant semantic parsing; narrow scope (no network/secrets/supply-chain) keeps it a "+" not "++" |
| Cost Efficiency | + | Preventing one `rm -rf ~/` or `git reset --hard` that wipes hours of work pays for itself; audit log aids incident review |

## Verdict

**CONDITIONAL**

Adopt when you want bypass-resistant, semantic protection against destructive git/filesystem commands specifically — and you understand it is a *complement to*, not a replacement for, Claude Code's built-in permission system and sandboxing. Its genuine net-new value over the built-in classifier is the semantic option-grammar parsing (defeats flag-reordering, shell-wrapper, and interpreter-one-liner bypasses that string/wildcard matching misses) and its awareness of git footguns the sandbox treats as "safe within cwd" (`git reset --hard`, `git stash clear`). That increment is real but narrow, so it does not clear the ADOPT bar of "use everywhere by default" — the built-in permission prompts already cover the common case for most users.

**Differentiation from overlaps.** Three distinct points in the agent-safety stack. **cc-safety-net** is the *focused, deep* git/filesystem data-loss guard: one PreToolUse Bash hook, deny via semantic command analysis, seven-agent support. **agentlint** (CONDITIONAL, 25 stars) is the *broad* runtime guardrail: 77 rules across 8 packs covering secrets, exfiltration, supply chain, code quality, subagent auditing — far wider, but its universal pack only heuristically matches the same destructive commands cc-safety-net parses semantically. **hol-guard** (CONDITIONAL, ~361 stars) sits one layer lower as "AV": it snapshot/diffs extensions and package installs at harness launch — provenance of what *runs*, not what the agent *does* mid-session. So they are complementary: hol-guard vets the launcher, cc-safety-net deep-guards a narrow set of catastrophic Bash commands, agentlint broadly constrains agent actions. If your single concern is "never let the agent nuke my working tree or home directory," cc-safety-net is the most precise and best-tested tool for exactly that; if you want broad action control, agentlint covers more. The closest substitute is Claude Code's own permission classifier — cc-safety-net's justification over it is bypass-resistance and git-footgun awareness, which is meaningful but not universal.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [cc-safety-net](https://github.com/kenryu42/cc-safety-net) | tool | Coding-agent CLI hook that catches destructive git and filesystem commands before they run (1.4K stars) | Agents can run destructive git/filesystem commands; need a pre-execution safety net | agentlint, hol-guard |
