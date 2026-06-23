# Evaluation: hol-guard

**Repo:** [hashgraph-online/hol-guard](https://github.com/hashgraph-online/hol-guard)
**Stars:** 362 | **Last updated:** 2026-06-19 | **License:** Apache-2.0
**Dev loop stage:** Implement (runtime tool-call gating) + Ship (CI plugin gate via `plugin-scanner`)
**Layer:** Infrastructure

---

## What it does

"AI antivirus for developer agents — scans plugins, skills, MCP servers before tools run." HOL Guard ships as two PyPI packages from the same repo: `hol-guard` (the local runtime guard) and `plugin-scanner` (a CI/maintainer linter). Despite the package names, the source lives under `src/codex_plugin_scanner/`.

The **runtime guard** is the load-bearing piece. You install it with `pipx install hol-guard` and run `hol-guard init`, which discovers your local AI harness config (Claude Code, Codex, Copilot CLI, Cursor, Gemini, OpenCode, Kimi, Grok, ZCode, Hermes) and installs itself *in front of* every tool action. For Claude Code specifically, Guard "prefers Claude hooks first" — it wires managed `PreToolUse`-style hooks — and falls back to a localhost "approval center" (dashboard at `http://localhost:6174`) when the shell cannot prompt inline. When the agent tries to act, Guard intercepts, runs its detectors, and (per the README) "decides in milliseconds whether to allow or block." Blocked actions are queued for human approval and every decision is written to a local "receipt" log.

The detection is **static rule/pattern matching, not LLM-based** — confirmed by the detector modules under `src/codex_plugin_scanner/guard/runtime/`: `secret_sources.py`, `secret_file_requests.py`, `secret_sensitivity.py`, `prompt_injection.py`, `persistence_rules.py`, `data_flow_rules.py`, `composition_rules.py`, plus a dedicated `false_positive_rules.py` and an `advisory_matchers.py` that checks against an optional signed advisory database synced from `advisories.hol.org`. It also bundles Cisco AI Defense's `cisco-ai-skill-scanner` (and, in CI/Docker, the MCP scanner) for static skill/MCP analysis. Sensitivity is tunable across four levels — Gentle, Balanced (default), Strict, Paranoid — controlling whether it blocks only high-confidence secrets/exfil or escalates to low-confidence signals and any unrecognized MCP action.

The **`plugin-scanner`** package is a separate, CI-oriented quality gate: `plugin-scanner verify .` / `scan` produces a 0–100 score across Manifest Validation, Security, Operational Security, Best Practices, Marketplace, Skill Security, and Code Quality, emits SARIF, and runs as a GitHub Action (`fail_on_severity`, `min_score`). That is a publisher/maintainer tool, not the pre-execution guard the catalog entry describes.

## How we tested it

**Evidence:** REVIEW

Source-grounded evaluation. I did **not** install or run hol-guard. The method was: read the full README, enumerate the repo file tree, inspect the runtime detector module layout and the `.factory` Claude/Codex SKILL.md, and check release cadence, license, and the user's actual local environment for fit. No scan was executed, so no detection rates, false-positive rates, or timing numbers in this document come from observed runs — the "milliseconds" latency and the protection-level behavior are the project's own claims, labeled as such.

This revises an earlier (Jun 18) architecture-review eval of the same tool. That version asserted a "Safe Decode sandbox" and a documented "six-step pipeline" from `docs/guard/architecture.md`; I could not verify those specific claims against the current source tree, so per the integrity rule they are not carried forward — this version is grounded only in what the README and the `src/.../guard/runtime/` module layout actually show.

**Correction to the task brief:** the brief stated the user already has hol-guard installed. That is not the case. `command -v hol-guard` returns nothing, `pipx list` has no hol-guard, there is no `~/.hol-guard` / `~/.config/hol-guard` state directory, and `~/.claude/settings.json` hooks reference only GSD and OMEGA — no Guard wiring. The grep hits under `~/.claude/projects/...` were transcripts of *this evaluation session*, not an install. Real-world fit is therefore assessed against the user's existing hook stack rather than observed Guard behavior.

```bash
gh api repos/hashgraph-online/hol-guard --jq '{stars,license,description,pushed_at}'
gh api repos/hashgraph-online/hol-guard/readme --jq '.content' | base64 -d
gh api "repos/hashgraph-online/hol-guard/git/trees/HEAD?recursive=1" --jq '.tree[].path'
gh api repos/hashgraph-online/hol-guard/contents/LICENSE --jq '.content' | base64 -d | head -5
gh api repos/hashgraph-online/hol-guard/releases --jq '.[0:3]'
gh api "repos/hashgraph-online/hol-guard/commits?since=2026-03-20T00:00:00Z&per_page=100" --jq 'length'
# local-fit checks
command -v hol-guard; pipx list; ls ~/.hol-guard ~/.config/hol-guard
python3 -c "import json;print(json.load(open('~/.claude/settings.json'))['hooks'])"  # only GSD + OMEGA
```

## What worked

- **Targets the right gap with the right mechanism.** Pre-execution interception of agent tool calls is exactly the supply-chain failure mode the catalog entry names (downloaded skills/plugins/MCP servers executing malicious code). Static detectors deciding in-line, before file writes or network calls, is the correct architecture for a guard — it does not put an LLM judgment call in the hot path.
- **Real harness breadth and Claude-native wiring.** Documented, per-harness approval strategies for 10+ agents. For Claude Code it uses native hooks first (the right integration point) and only falls back to its localhost approval center when the shell can't prompt — a thoughtful design that respects the harness rather than wrapping it blindly.
- **Tunable sensitivity with an explicit false-positive layer.** Four protection levels plus a dedicated `false_positive_rules.py` module shows the maintainers treat false positives as a first-class problem — critical for a tool that gates *every* action, where over-blocking is the fastest path to uninstall.
- **Strong security-engineering signals for an infra/security tool.** OpenSSF Scorecard badge, CodeQL, ClusterFuzzLite fuzzing, SHA-pinned-actions checks, a dedicated `security-gates.yml` workflow, SECURITY.md, and reuse of Cisco AI Defense's open-source scanners. For a tool you grant interception privileges, this provenance matters more than raw star count.
- **Local-first and privacy-conscious.** Receipts, baselines, and advisory DB are local; advisory sync is pull-only and explicitly does not transmit file paths, harness configs, or workspace identifiers. An optional password/TOTP approval gate guards saved allow-decisions. No cloud dependency for core blocking.
- **`plugin-scanner` is a genuinely useful, separable CI artifact** with SARIF output and a published GitHub Action — directly relevant for anyone publishing skills/plugins to a marketplace.

## What didn't work or surprised us

- **Very young, single-org, fast-churning.** Created 2026-03-28 (under 3 months old), 362 stars, 7 forks, and ~100 commits in the last ~90 days, with releases at `v2.0.829` *on the eval date* (three releases within ~18 minutes). High velocity is good for fixes but means the runtime gate, the API, and the detector set are all moving targets; pinning a version is advisable.
- **It claims `PreToolUse` hook slots — direct conflict risk with the user's stack.** The user's `~/.claude/settings.json` already runs OMEGA's `fast_hook.py` on PostToolUse (matcher `Edit|Write|NotebookEdit|Bash|Read`), SessionStart, and Stop, plus GSD hooks. Guard installing "managed" hooks into the same config is exactly the multi-hook collision risk flagged in the agentmemory eval. There is no documented conflict-resolution contract for coexisting third-party hooks.
- **Performance tax on every tool call.** By design Guard runs detectors before each action. Even at the claimed millisecond budget, that is non-zero latency multiplied across thousands of tool calls per session, and a hook crash/timeout fails *open* on some harnesses (Kimi/Grok are documented to fail open) — meaning the guarantee silently degrades under load exactly when you'd want it most.
- **Naming/packaging is confusing.** Two packages (`hol-guard`, `plugin-scanner`), a third source name (`codex_plugin_scanner`), an optional Cisco extra with Python-version-dependent availability (no Cisco MCP scanner on 3.14+), and a `[cisco]` extra vs. a repo-controlled `cisco-mcp` uv group. The install matrix is heavier than "pipx install" implies.
- **Cloud account required for advisory freshness.** The runtime detectors work offline, but `advisories sync` (the up-to-date threat feed) requires a HOL Guard Cloud account. Without it you run on the bundled, aging advisory DB — a soft push toward their hosted service.
- **GitHub reports the license as `NOASSERTION`** even though the LICENSE file and README are unambiguously Apache-2.0. Cosmetic, but worth noting since it can trip automated license scanners.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't make the agent's *code* more correct; it gates risky actions, which is orthogonal to code correctness |
| Speed | - | Adds per-tool-call detector latency to every action; net slowdown, partly mitigated by an approval queue that avoids stop-the-world prompts |
| Maintainability | neutral | No effect on the codebase under development; receipts add an auditable decision trail |
| Safety | ++ | Core value: pre-execution interception of secrets exfil, prompt injection, supply-chain hooks, and untrusted MCP actions across 10+ harnesses, with tunable strictness and a false-positive layer |
| Cost Efficiency | neutral | Free/local for core use; no token cost (static detectors, not LLM); advisory freshness nudges toward a Cloud account |

## Verdict

**CONDITIONAL**

Adopt when supply-chain risk from untrusted agent extensions is a real concern — installing community skills/plugins/MCP servers, running agents with broad file/network access, or operating in a team/regulated setting that wants an auditable allow/block trail. The mechanism (static, in-line, pre-execution interception with native Claude hooks and tunable sensitivity) is the correct design for the Safety signal it targets, and the security-engineering provenance (OpenSSF Scorecard, CodeQL, fuzzing, Cisco scanners) is unusually strong for a 362-star project.

Hold off for the default solo-dev-on-trusted-extensions case, and specifically in *this* environment: the user's `~/.claude/settings.json` already carries OMEGA + GSD hooks, and Guard claiming managed `PreToolUse` slots introduces real hook-collision risk with no documented coexistence contract. The tool is also under 3 months old and releasing many times per day, so pin a version and re-test the hook wiring before trusting it on the hot path. If you only publish plugins/skills, prefer the lighter `plugin-scanner` CI gate alone and skip the runtime guard.

**vs. overlaps:** SkillSpector and agentlint are *static, on-demand* scanners you point at an artifact — they audit a skill/config before you install it. hol-guard's distinct niche is the **runtime gate**: it sits in the live tool-call path and blocks actions as they happen across many harnesses. Use a static scanner (SkillSpector/agentlint, or hol-guard's own `plugin-scanner`) at install/CI time; reach for hol-guard's runtime guard only when you want continuous, in-session enforcement and can absorb the hook + latency cost.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hol-guard](https://github.com/hashgraph-online/hol-guard) | tool | AI antivirus for developer agents — scans plugins, skills, MCP servers before tools run | Downloaded agent extensions could be malicious; need pre-execution scanning | SkillSpector, agentlint |
