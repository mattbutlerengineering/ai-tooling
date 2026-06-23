# Evaluation: security-guidance

**Repo:** [anthropics/claude-plugins-official — plugins/security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance)
**Stars:** 30,644 (parent marketplace repo; the plugin is one of many in it) | **Last updated:** 2026-06-23 (marketplace `pushed_at`); plugin version `2.0.6` | **License:** Apache-2.0
**Last verified:** 2026-06-22
**Dev loop stage:** Review (primary — LLM diff/commit review) and Implement (regex pattern warnings fire live on Edit/Write)
**Layer:** Tooling (a Claude Code plugin = hooks + LLM calls; no infra of its own)

> **Provenance note:** the catalog entry was **unlinked**. Verified via `gh search repos --owner anthropics plugins`: the canonical home is the **official Anthropic-managed marketplace** `anthropics/claude-plugins-official`, plugin path `plugins/security-guidance`, authored by David Dworken (dworken@anthropic.com). Numerous third-party "mirror" repos exist (costrict-plugins, blue119/security-guidance-demo, companion gates like XecureLogic/policy-gate and andreaslehnert/uc-codeguard) but are NOT the source. The README points bug reports at `anthropics/claude-code/issues`, confirming first-party ownership.

---

## What it does

A first-party Claude Code plugin that runs **security review on Claude-generated code in three layers**, wired entirely through Claude Code hooks (no slash commands, no agents of its own):

1. **Pattern warnings (Implement-time, layer 1).** A `PostToolUse` hook matching `Edit|Write|MultiEdit|NotebookEdit` runs `patterns.py`, a regex ruleset of 25 known-dangerous patterns (`yaml.load`, `torch.load(weights_only=False)`, `pickle.load` on untrusted data, raw `innerHTML`, hardcoded secrets, `shell=True` string concatenation, Go-specific rules, etc.). Each rule has a stable numeric RuleId (an `assert` at import time fails loudly if a pattern is added without one — real engineering hygiene). Zero LLM cost; instant feedback as the agent writes.
2. **LLM diff review (Review-time, layer 2).** A `Stop` hook sends the turn's diff (changed paths, diff hunks, relevant file contents) to a fast LLM call — default `claude-opus-4-7` via `SECURITY_REVIEW_MODEL` — and feeds high-severity findings back to Claude via `asyncRewake` so the model can fix them *before the user sees the response*. An 8 KB prompt budget concatenates org policy files.
3. **Agentic commit/push review (Review/Ship-time, layer 3).** On `git commit` / `git push` (and Graphite `gt create/modify/submit`), an SDK-driven reviewer with `Read`/`Grep`/`Glob` traces data flow across files to catch multi-file vulns that pattern matching and single-diff review miss (IDOR, auth bypass, cross-file SSRF).

It is **purely defensive** — it reviews/flags, it never scans infrastructure or performs offensive actions. Configurable org rules drop into `claude-security-guidance.md` (user → project → project-local, concatenated). A `SECURITY_GUIDANCE_DISABLE=1` kill switch and per-layer enable flags exist. `SG_DUAL_OR=on` unions two parallel review calls for higher recall at ~2× cost.

## How we tested it

**Evidence:** MEASURED

**Ran layer 1 (`patterns.py`) hands-on** on 2026-06-22 (macOS arm64, Python 3). Layer 1 is the deterministic, LLM-free part of the plugin: a `PostToolUse` hook (`hooks/security_reminder_hook.py`) calls `check_patterns(file_path, content)`, which iterates the `SECURITY_PATTERNS` list defined in `hooks/patterns.py` and applies each rule's `substrings` / `regex` / `path_check` / `path_filter`. I fetched the plugin source into a `mktemp -d` temp dir via `gh api`, **imported the real `patterns.py` ruleset, drove it through the `check_patterns` matching logic copied verbatim from `security_reminder_hook.py` (L452, with `extensibility.user_patterns()` stubbed to `[]`)**, and ran it against 10 crafted *positive* samples (known-dangerous snippets that should fire) and 5 *negative* samples (safe variants that should not). I captured how many rules loaded, which RuleId each sample fired, and the no-fire on every negative. **The temp dir was deleted afterward.**

Observed (verbatim from the run):

```
[load] patterns.py imported OK -> 25 rules loaded
[load] RuleId enum members: 25; name->id map: 25
[load] import-time assert (enum <-> SECURITY_PATTERNS) holds
[load] desync guard verified: dropping a rule trips the assert
```

| Sample (path)                              | Fired rule (RuleId)            | Expected |
|--------------------------------------------|--------------------------------|----------|
| P1 `yaml.load(open(...))` (.py)            | `unsafe_yaml_load` (12)        | fire ✓   |
| P2 `torch.load(..., weights_only=False)`   | `torch_unsafe_load` (23)       | fire ✓   |
| P3 `pickle.loads(request.data)`            | `pickle_deserialization` (8)   | fire ✓   |
| P4 `el.innerHTML = userInput` (.js)        | `innerHTML_xss` (7)            | fire ✓   |
| P5 `subprocess.run(cmd, shell=True)`       | `python_subprocess_shell` (10) | fire ✓   |
| P6 `os.system('rm -rf ' + path)`           | `os_system_injection` (9)      | fire ✓   |
| P7 `eval(expr)` (.js)                       | `eval_injection` (4)           | fire ✓   |
| P8 `requests.get(url, verify=False)`       | `tls_verification_disabled` (15) | fire ✓ |
| P9 `np.load(f, allow_pickle=True)`         | `pickle_wrapper_load` (25)     | fire ✓   |
| P10 `.github/workflows/ci.yml` (path_check)| `github_actions_workflow` (1)  | fire ✓   |
| N1 `yaml.safe_load(...)`                    | — (none)                       | no-fire ✓|
| N2 `torch.load(..., weights_only=True)`    | — (none)                       | no-fire ✓|
| N3 `el.textContent = userInput`            | — (none)                       | no-fire ✓|
| N4 `subprocess.run(['ls','-l',path])`      | — (none)                       | no-fire ✓|
| N5 `def add(a,b): return a+b`              | — (none)                       | no-fire ✓|

**10/10 positives fired the correct RuleId; 5/5 negatives stayed silent.** The four discriminating true-negatives are the interesting ones: the ruleset distinguishes `yaml.load` from `yaml.safe_load`, `torch.load(weights_only=False)` from `weights_only=True` (via a same-line negative lookahead), `innerHTML` from `textContent`, and shell-string `subprocess` from arg-list `subprocess` — so it is not a naïve substring grep. The **RuleId-assert hygiene claim is confirmed**: importing `patterns.py` runs the module-level `assert set(_RULE_NAME_TO_ID) == {p["ruleName"] for p in SECURITY_PATTERNS}` (passed), and a deliberate desync (dropping one rule) trips it — so adding a pattern without a RuleId fails import (and CI) loudly.

```bash
# Fetch the real plugin source into a temp dir (deleted after the run)
TMP=$(mktemp -d)
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/hooks/patterns.py \
  --jq '.content' | base64 -d > "$TMP/patterns.py"
gh api repos/anthropics/claude-plugins-official/contents/plugins/security-guidance/hooks/security_reminder_hook.py \
  --jq '.content' | base64 -d > "$TMP/security_reminder_hook.py"   # source of check_patterns (L452)

# Harness imports the REAL ruleset and reuses check_patterns verbatim
#   from patterns import SECURITY_PATTERNS, RuleId, rule_names_to_mask, _RULE_NAME_TO_ID
#   check_patterns(path, content) -> [ruleName, ...]   (extensibility.user_patterns() stubbed [])
python3 "$TMP/run_eval.py"     # -> 25 rules; 10/10 positives, 5/5 negatives; assert verified
rm -rf "$TMP"
```

**What was NOT exercised (needs live Claude Code hooks — not headless-drivable):** Layers 2 and 3 are LLM calls wired through the Claude Code hook runtime — the `Stop`-hook diff review (default Opus 4.7, `asyncRewake` self-correction) and the SDK-driven agentic commit/push reviewer. Driving them requires a live Claude Code session emitting real `Stop`/`PostToolUse(Bash)` hook events with a git repo and model credentials; they cannot be invoked standalone. **I did not install the plugin, did not trigger any hook in a live session, and did not invoke any LLM review**, so detection precision/recall, false-positive rate, and cost of layers 2–3 remain unmeasured — those are the README's own probabilistic-assistant caveats, cited as such, not measured here. The "few percentage points more recall" and "2× cost" figures below are the README's claims.

## What worked

- **Layer 1 is a verifiable deterministic gate — measured.** 25 rules load, and on crafted samples 10/10 known-dangerous patterns fire their correct RuleId while 5/5 safe variants stay silent, including four non-trivial discriminations (`safe_load` vs `load`, `weights_only=True` vs `False`, `textContent` vs `innerHTML`, arg-list vs shell-string subprocess). This is a real, auditable detection property — the free, zero-LLM layer earns its place on its own.
- **RuleId hygiene is real, not a doc claim — measured.** Importing `patterns.py` runs an `assert` keeping the enum in sync with the ruleset; a deliberate desync trips it, so a pattern added without a RuleId fails import and CI. Confirmed live.
- **First-party, defense-in-depth design.** Three layers hit three different points in the loop (write → turn-end → commit) with three different cost/fidelity tradeoffs: free regex at write time, a cheap diff LLM at turn end, and an expensive cross-file agentic reviewer only at commit/push. This is the right escalation ladder, and being authored by Anthropic with Apache-2.0 means it tracks Claude Code's hook API closely and is safe to depend on.
- **`asyncRewake` integration is the standout mechanism.** Findings are fed *back to Claude before the user sees the response*, so the agent self-corrects vulnerabilities inline rather than surfacing a wall of warnings to the human afterward. That is a genuinely better placement than a post-hoc reviewer — it closes the loop inside the agent's turn.
- **Operationally well-thought-out.** Kill switch (`SECURITY_GUIDANCE_DISABLE`), per-layer toggles, a dedicated `ENABLE_STOP_REVIEW=0` for multi-agent/shared-worktree setups (where another agent can move HEAD between turns), model selection across 1P/Bedrock/Vertex, a documented 8 KB prompt budget with defined truncation order, and a size-rotated local debug log. These are the details a tool gets right only after real production use.
- **Honest privacy + limitations disclosure.** The README states exactly what data leaves the machine per layer and where it goes per provider config, and explicitly frames the tool as best-effort assistive — "not a substitute for human review, SAST/DAST, dependency scanning, or pen-testing," with no warranty. Calibrates expectations correctly.

## What didn't work or surprised us

- **Layer 1's `patterns.py` is pure data + one helper — the matching lives in the hook.** `patterns.py` itself exposes only `SECURITY_PATTERNS`, the `RuleId` enum, and `rule_names_to_mask`; the actual `check_patterns` loop is in `security_reminder_hook.py`. To exercise detections standalone I had to replicate that loop verbatim (it is small and side-effect-free). A worthwhile note for anyone reusing the ruleset: import the data from `patterns.py`, but the matching contract (substrings → regex → path_check, with `path_filter` as a gate) is defined by the hook.
- **Regex rules have documented multi-line blind spots.** The source itself notes `torch_unsafe_load` and `unsafe_yaml_load` "false-positive [on] multi-line calls" — the same-line lookaheads that suppress safe variants only see one line, so a call split across lines can mis-fire or mis-suppress. Layer 1 is a line-oriented heuristic, by design.
- **Detection quality of layers 2–3 is unmeasured here and inherently nondeterministic.** Layers 2 and 3 are LLM calls; the README itself warns they "can miss vulnerabilities, produce false positives, and may behave differently across codebases, languages, and model versions." I did not run them (they need live hooks), so I cannot vouch for their precision/recall. They are probabilistic assistants, not deterministic gates (contrast the companion `policy-gate`/`uc-codeguard` third-party plugins, which exist precisely to add a hard fail-closed layer).
- **Real per-turn API cost (layers 2–3).** The Stop-hook review fires on *every* turn that changed code, defaulting to Opus 4.7; `SG_DUAL_OR` doubles that. On a busy coding session this is a non-trivial recurring token cost on top of the main loop, and the commit reviewer additionally pulls in files via Read/Grep/Glob. Cost scales with activity, not with risk.
- **Layer-3 doesn't read org policy.** The README notes the agentic commit reviewer does *not* currently load `claude-security-guidance.md`, so codebase-specific rules only influence the layer-2 diff review — an asymmetry worth knowing if you rely on custom org rules.
- **Coupled to the Claude Code harness.** Unlike the overlapping *skills* (ghostsecurity/skills, trailofbits/skills), this is hook-based and Claude-Code-specific (CLI ≥ v2.1.144, Python 3.8+). It can't be invoked as a portable skill in another harness, and it only reviews Claude-generated diffs in-session — not arbitrary existing code on demand.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + (scoped to security) | Layer 1 measured: 10/10 crafted known-dangerous patterns fire the correct RuleId, 5/5 safe variants stay silent (incl. `safe_load`/`weights_only=True`/`textContent`/arg-list subprocess discriminations). Layers 2–3 catch injection/XSS/SSRF/IDOR/auth-bypass/deserialization classes and feed fixes back before the user sees them; nondeterministic and unmeasured here. |
| Speed | − (mild) | Layer-1 regex is instant (measured: pure in-process match, no I/O); layers 2–3 add LLM round-trips on turn-end and commit plus a SessionStart SDK check, sitting on the critical path. |
| Maintainability | + | Inline self-correction keeps known-dangerous patterns out of the committed codebase; org-rule file lets teams encode codebase-specific invariants; RuleId-assert hygiene (measured) keeps the ruleset internally consistent. |
| Safety | + (core value) | This is its entire purpose: defensive, automated security review wired into the agent loop at three escalating points, first-party and Apache-2.0; the deterministic layer-1 gate is verifiably accurate on the samples tested. |
| Cost Efficiency | − | Layer-1 is free (no LLM). Default Opus 4.7 review on every code-changing turn (2× with `SG_DUAL_OR`) plus file-pulling commit reviews make layers 2–3 cost scale with session activity. Mitigable via cheaper model / per-layer toggles. |

## Verdict

**ADOPT (with cost-tuning) — for projects already on the Claude Code harness.**

security-guidance is the official Anthropic, Apache-2.0 answer to "agent-generated code may introduce vulnerabilities," and its three-layer, defense-in-depth design (instant regex at write time → cheap diff LLM at turn end → cross-file agentic reviewer at commit) is the right shape for the problem. **The deterministic layer-1 ruleset is now measured**: 25 rules, 10/10 correct firings and 5/5 clean true-negatives on crafted samples, with verified RuleId-assert hygiene — a real auditable detection property, not a doc claim. The killer feature is `asyncRewake`: findings go back to Claude to self-correct *before the user sees the response*, which is a materially better placement than any post-hoc reviewer. First-party ownership means it stays current with the hook API and is low-risk to depend on. It is **ADOPT rather than CONDITIONAL** for Claude Code users because it is on the official default-enabled marketplace, defensive-by-construction, fully toggleable, and addresses a near-universal risk in agentic coding — there is little reason *not* to run at least layers 1–2. The caveats are operational, not disqualifying: the LLM layers' detection is probabilistic and unmeasured here (treat as assistive, not a gate — pair with a deterministic CI check for must-not-ship rules), and the per-turn Opus review has real recurring cost, so drop `SECURITY_REVIEW_MODEL` to Sonnet or disable the Stop layer on high-frequency/multi-agent setups. **Not ADOPT-universally** only because it is harness-locked to Claude Code; teams in other harnesses should reach for the portable skills below.

**vs. overlaps:**
- **ghostsecurity/skills** — portable AppSec *skills* (OWASP, threat modeling, secure defaults) invoked on demand in any harness. Complementary: skills give the model security *knowledge*; this plugin gives *automated, hook-driven review of actual diffs*. Use both — skills to write securely, this to catch what slipped.
- **trailofbits/skills** — professional audit-firm methodology as skills; deeper/heavier and pull-based. Better for explicit audit passes; security-guidance is the always-on background layer.
- **security-reviewer (agent)** — an explicitly-invoked review agent; same review goal but manual and harness-agnostic-ish, versus this plugin's automatic, in-loop, three-layer wiring. security-guidance wins on automation and inline self-correction; a dedicated reviewer agent wins when you want a deliberate, scoped pass.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [security-guidance](https://github.com/anthropics/claude-plugins-official/tree/main/plugins/security-guidance) | plugin | Official Anthropic Claude Code plugin: three-layer security review (regex pattern warnings on edits, LLM diff review on Stop with self-correction, agentic cross-file commit/push reviewer) for injection, XSS, SSRF, secrets, IDOR, and 25+ vuln classes | Agent-generated code may introduce security vulnerabilities the human never notices; wires automated defensive review into the agent loop so Claude fixes findings before the user sees the turn | ghostsecurity/skills & trailofbits/skills (portable security *knowledge* skills, on-demand vs. this always-on hook-driven review); security-reviewer (manual review agent vs. this automatic in-loop plugin) |
