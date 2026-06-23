# Evaluation: security-guidance

**Repo:** [anthropics/claude-plugins-official — plugins/security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance)
**Stars:** 30,444 (parent marketplace repo; the plugin is one of many in it) | **Last updated:** 2026-06-19 (marketplace `pushed_at`); plugin version `2.0.6` | **License:** Apache-2.0
**Dev loop stage:** Review (primary — LLM diff/commit review) and Implement (regex pattern warnings fire live on Edit/Write)
**Layer:** Tooling (a Claude Code plugin = hooks + LLM calls; no infra of its own)

> **Provenance note:** the catalog entry was **unlinked**. Verified via `gh search repos --owner anthropics plugins`: the canonical home is the **official Anthropic-managed marketplace** `anthropics/claude-plugins-official`, plugin path `plugins/security-guidance`, authored by David Dworken (dworken@anthropic.com). Numerous third-party "mirror" repos exist (costrict-plugins, blue119/security-guidance-demo, companion gates like XecureLogic/policy-gate and andreaslehnert/uc-codeguard) but are NOT the source. The README points bug reports at `anthropics/claude-code/issues`, confirming first-party ownership.

---

## What it does

A first-party Claude Code plugin that runs **security review on Claude-generated code in three layers**, wired entirely through Claude Code hooks (no slash commands, no agents of its own):

1. **Pattern warnings (Implement-time, layer 1).** A `PostToolUse` hook matching `Edit|Write|MultiEdit|NotebookEdit` runs `patterns.py`, a regex ruleset of ~25 known-dangerous patterns (`yaml.load`, `torch.load(weights_only=False)`, `pickle.load` on untrusted data, raw `innerHTML`, hardcoded secrets, `shell=True` string concatenation, Go-specific rules, etc.). Each rule has a stable numeric RuleId (an `assert` at import time fails loudly if a pattern is added without one — real engineering hygiene). Zero LLM cost; instant feedback as the agent writes.
2. **LLM diff review (Review-time, layer 2).** A `Stop` hook sends the turn's diff (changed paths, diff hunks, relevant file contents) to a fast LLM call — default `claude-opus-4-7` via `SECURITY_REVIEW_MODEL` — and feeds high-severity findings back to Claude via `asyncRewake` so the model can fix them *before the user sees the response*. An 8 KB prompt budget concatenates org policy files.
3. **Agentic commit/push review (Review/Ship-time, layer 3).** On `git commit` / `git push` (and Graphite `gt create/modify/submit`), an SDK-driven reviewer with `Read`/`Grep`/`Glob` traces data flow across files to catch multi-file vulns that pattern matching and single-diff review miss (IDOR, auth bypass, cross-file SSRF).

It is **purely defensive** — it reviews/flags, it never scans infrastructure or performs offensive actions. Configurable org rules drop into `claude-security-guidance.md` (user → project → project-local, concatenated). A `SECURITY_GUIDANCE_DISABLE=1` kill switch and per-layer enable flags exist. `SG_DUAL_OR=on` unions two parallel review calls for higher recall at ~2× cost.

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed or run.** I verified the canonical repo via `gh search`, then read the plugin's `README.md`, `.claude-plugin/plugin.json` (version 2.0.6), `hooks/hooks.json` (all four hook events + the git-command `if`-matchers), the `LICENSE` (Apache-2.0), and inspected `hooks/patterns.py` for the regex/RuleId structure. The hook wiring, layer behavior, env-var configuration, model defaults, privacy/data-flow statements, and the ~25-pattern / 25+-vulnerability-class claims are all read directly from the repo's own files. **No plugin was installed, no edits were made to trigger the hooks, and no LLM review was invoked**, so I have not independently measured detection precision/recall or false-positive rates — those would require live use. No metrics below are invented; the "few percentage points more" recall and "2× cost" figures are the README's own claims, cited as such.

```bash
# Provenance — the entry was unlinked; find the real owner
gh search repos security-guidance claude --json fullName,description,stargazersCount,url
gh search repos --owner anthropics plugins --json fullName,description,stargazersCount   # -> anthropics/claude-plugins-official
gh api repos/anthropics/claude-plugins-official --jq '{full_name,stars:.stargazers_count,license:.license.spdx_id,pushed_at}'
gh api 'repos/anthropics/claude-plugins-official/git/trees/HEAD?recursive=1' --jq '.tree[].path' | grep -i security-guidance
# Read the plugin
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/README.md       --jq '.content' | base64 -d
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/.claude-plugin/plugin.json --jq '.content' | base64 -d  # version 2.0.6
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/hooks/hooks.json --jq '.content' | base64 -d
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/hooks/patterns.py --jq '.content' | base64 -d
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/LICENSE          --jq '.content' | base64 -d  # Apache-2.0
# Catalog overlap check
grep -inE "ghostsecurity|trailofbits|security-reviewer|Anthropic-Cybersecurity" /Users/mbutler/github/ai-tooling/CATALOG.md
```

## What worked

- **First-party, defense-in-depth design.** Three layers hit three different points in the loop (write → turn-end → commit) with three different cost/fidelity tradeoffs: free regex at write time, a cheap diff LLM at turn end, and an expensive cross-file agentic reviewer only at commit/push. This is the right escalation ladder, and being authored by Anthropic with Apache-2.0 means it tracks Claude Code's hook API closely and is safe to depend on.
- **`asyncRewake` integration is the standout mechanism.** Findings are fed *back to Claude before the user sees the response*, so the agent self-corrects vulnerabilities inline rather than surfacing a wall of warnings to the human afterward. That is a genuinely better placement than a post-hoc reviewer — it closes the loop inside the agent's turn.
- **Operationally well-thought-out.** Kill switch (`SECURITY_GUIDANCE_DISABLE`), per-layer toggles, a dedicated `ENABLE_STOP_REVIEW=0` for multi-agent/shared-worktree setups (where another agent can move HEAD between turns), model selection across 1P/Bedrock/Vertex, a documented 8 KB prompt budget with defined truncation order, and a size-rotated local debug log. These are the details a tool gets right only after real production use.
- **Honest privacy + limitations disclosure.** The README states exactly what data leaves the machine per layer and where it goes per provider config, and explicitly frames the tool as best-effort assistive — "not a substitute for human review, SAST/DAST, dependency scanning, or pen-testing," with no warranty. Calibrates expectations correctly.
- **Engineering hygiene in the ruleset.** Stable numeric RuleIds with an import-time `assert` keeping the enum in sync, telemetry attribution per rule, and support for user-defined `user:` patterns. Inline justification comments are honored as exclusions — a pragmatic false-positive escape hatch.

## What didn't work or surprised us

- **Detection quality is unmeasured here and inherently nondeterministic.** Layers 2 and 3 are LLM calls; the README itself warns they "can miss vulnerabilities, produce false positives, and may behave differently across codebases, languages, and model versions." I did not run it, so I cannot vouch for precision/recall. This is a probabilistic assistant, not a deterministic gate (contrast the companion `policy-gate`/`uc-codeguard` third-party plugins, which exist precisely to add a hard fail-closed layer).
- **Real per-turn API cost.** The Stop-hook review fires on *every* turn that changed code, defaulting to Opus 4.7; `SG_DUAL_OR` doubles that. On a busy coding session this is a non-trivial recurring token cost on top of the main loop, and the commit reviewer additionally pulls in files via Read/Grep/Glob. Cost scales with activity, not with risk.
- **Latency / turn-blocking surface.** Three hook layers plus a `SessionStart` hook that ensures the Agent SDK (180 s timeout) add overhead to session start, edits, turn-end, and commits. Pattern warnings are instant, but the LLM layers add round-trips to the critical path of finishing a turn and committing.
- **Layer-3 doesn't read org policy.** The README notes the agentic commit reviewer does *not* currently load `claude-security-guidance.md`, so codebase-specific rules only influence the layer-2 diff review — an asymmetry worth knowing if you rely on custom org rules.
- **Coupled to the Claude Code harness.** Unlike the overlapping *skills* (ghostsecurity/skills, trailofbits/skills), this is hook-based and Claude-Code-specific (CLI ≥ v2.1.144, Python 3.8+). It can't be invoked as a portable skill in another harness, and it only reviews Claude-generated diffs in-session — not arbitrary existing code on demand.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (scoped to security) | Catches injection/XSS/SSRF/IDOR/auth-bypass/unsafe-deserialization/path-traversal classes in agent-written diffs and feeds fixes back before the user sees them; nondeterministic and unmeasured here. |
| Speed | − (mild) | Adds LLM round-trips on turn-end and commit, plus a SessionStart SDK check; layer-1 regex is instant but layers 2–3 sit on the critical path. |
| Maintainability | + | Inline self-correction keeps known-dangerous patterns out of the committed codebase; org-rule file lets teams encode codebase-specific invariants. |
| Safety | + (core value) | This is its entire purpose: defensive, automated security review wired into the agent loop at three escalating points, first-party and Apache-2.0. |
| Cost Efficiency | − | Default Opus 4.7 review on every code-changing turn (2× with `SG_DUAL_OR`) plus file-pulling commit reviews; cost scales with session activity. Mitigable via cheaper model / per-layer toggles. |

## Verdict

**ADOPT (with cost-tuning) — for projects already on the Claude Code harness.**

security-guidance is the official Anthropic, Apache-2.0 answer to "agent-generated code may introduce vulnerabilities," and its three-layer, defense-in-depth design (instant regex at write time → cheap diff LLM at turn end → cross-file agentic reviewer at commit) is the right shape for the problem. The killer feature is `asyncRewake`: findings go back to Claude to self-correct *before the user sees the response*, which is a materially better placement than any post-hoc reviewer. First-party ownership means it stays current with the hook API and is low-risk to depend on. It is **ADOPT rather than CONDITIONAL** for Claude Code users because it is on the official default-enabled marketplace, defensive-by-construction, fully toggleable, and addresses a near-universal risk in agentic coding — there is little reason *not* to run at least layers 1–2. The caveats are operational, not disqualifying: detection is probabilistic (treat as assistive, not a gate — pair with a deterministic CI check for must-not-ship rules), and the per-turn Opus review has real recurring cost, so drop `SECURITY_REVIEW_MODEL` to Sonnet or disable the Stop layer on high-frequency/multi-agent setups. **Not ADOPT-universally** only because it is harness-locked to Claude Code; teams in other harnesses should reach for the portable skills below.

**vs. overlaps:**
- **ghostsecurity/skills** — portable AppSec *skills* (OWASP, threat modeling, secure defaults) invoked on demand in any harness. Complementary: skills give the model security *knowledge*; this plugin gives *automated, hook-driven review of actual diffs*. Use both — skills to write securely, this to catch what slipped.
- **trailofbits/skills** — professional audit-firm methodology as skills; deeper/heavier and pull-based. Better for explicit audit passes; security-guidance is the always-on background layer.
- **security-reviewer (agent)** — an explicitly-invoked review agent; same review goal but manual and harness-agnostic-ish, versus this plugin's automatic, in-loop, three-layer wiring. security-guidance wins on automation and inline self-correction; a dedicated reviewer agent wins when you want a deliberate, scoped pass.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | plugin | Official Anthropic Claude Code plugin: three-layer security review (regex pattern warnings on edits, LLM diff review on Stop with self-correction, agentic cross-file commit/push reviewer) for injection, XSS, SSRF, secrets, IDOR, and 25+ vuln classes | Agent-generated code may introduce security vulnerabilities the human never notices; wires automated defensive review into the agent loop so Claude fixes findings before the user sees the turn | ghostsecurity/skills & trailofbits/skills (portable security *knowledge* skills, on-demand vs. this always-on hook-driven review); security-reviewer (manual review agent vs. this automatic in-loop plugin) |
