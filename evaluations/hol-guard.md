# Evaluation: HOL Guard

**Repo:** [hashgraph-online/hol-guard](https://github.com/hashgraph-online/hol-guard)
**Stars:** 361 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Dev loop stage:** Review / Ship
**Layer:** Infrastructure

---

## What it does

AI antivirus for developer agents. HOL Guard intercepts tool actions before files change or network calls fire, deciding in milliseconds whether to allow or block. It ships as two PyPI packages: `hol-guard` (local harness protection) and `plugin-scanner` (CI/maintainer verification). Guard wraps 10+ harnesses (Claude Code, Codex, Copilot CLI, Cursor, Gemini, Grok, Kimi, OpenCode, ZCode, Hermes) via launcher shims that route launches through a detection pipeline before the harness executes.

The detection pipeline works in six steps: discover harness config → normalize artifacts into snapshots → diff against stored baselines → evaluate policy → record receipts → launch only if not blocked. Detectors include a Safe Decode sandbox that unwraps base64, hex, gzip, heredoc, Python `-c`, Node `-e`, and PowerShell `-EncodedCommand` without executing payloads. Four security levels (Gentle → Balanced → Strict → Paranoid) control sensitivity. A localhost dashboard (port 6174) shows pending approvals, receipts, and decision history.

Supply-chain scanning intercepts package managers (npm, pip) via shims to block known-malicious dependencies before install. The `supply-chain scan` and `explain` commands provide CVE context similar to `npm audit` but integrated into the agent workflow.

## How we tested it

Architecture review based on repo structure, docs, and README. Did not install locally — evaluation is based on documentation depth, detection architecture analysis, and comparison with existing catalog entries.

```
gh api repos/hashgraph-online/hol-guard --jq '.description, .stargazers_count'
# Read: README.md, docs/guard/architecture.md, docs/guard/remediation.md
# Checked: src/ structure, release cadence (v2.0.814, released today)
```

Assessed the detection pipeline by reading `docs/guard/architecture.md` — the six-step snapshot/diff/policy/receipt flow is well-documented with clear separation of concerns. The Safe Decode sandbox for encoded command detection is a genuinely novel approach not found in SkillSpector or agentlint.

## What worked

- **Real detection pipeline, not marketing.** The architecture doc reveals a genuine snapshot-diff-policy engine with per-harness adapter modules. This isn't a README wrapper — it's a structured security product.
- **10+ harness support** with per-harness approval strategies (Claude hooks, Codex thread binding, Copilot hook wiring). Broadest harness coverage of any security tool in the catalog.
- **Four graduated security levels** let teams start permissive and tighten. Paranoid mode blocks any unrecognized MCP server action — useful for high-security environments.
- **Supply-chain scanning** via package manager shims is a unique layer: intercepts `npm install` and `pip install` before dependencies land, not after.
- **Receipt system** creates an auditable trail of every allow/block decision with diff evidence. The approval center provides a local localhost dashboard for reviewing pending decisions.
- **Very active development** — v2.0.814 released today, 222+ merged PRs. The velocity is high.

## What didn't work or surprised us

- **No hands-on test.** Evaluation is architecture-review-only. The detection claims are well-documented but unverified in practice.
- **Python 3.10+ dependency** adds a runtime requirement. Go binary or npm package would be lighter for JS/TS-focused teams.
- **Wrapper-mode approach means startup friction.** Every harness launch routes through Guard, adding latency. The docs acknowledge this is the core execution strategy.
- **361 stars is modest** for the scope claimed. The project is young (most development is recent) but adoption is still early.
- **License shows as "NOASSERTION" on GitHub** despite the file being Apache-2.0. Minor metadata issue.
- **Unclear how it handles false positives at scale.** The remediation docs describe per-package exceptions but don't address systemic false positive rates.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Doesn't affect code output — focuses on tool trust |
| Speed | - | Adds launch interception overhead to every harness start |
| Maintainability | neutral | Receipts and audit trails help security posture but don't change code |
| Safety | ++ | Pre-execution blocking, supply-chain scanning, encoded command detection, 4 security levels |
| Cost Efficiency | neutral | No token impact — operates at the harness layer |

## Verdict

**CONDITIONAL**

Use when operating in security-sensitive environments where agent extensions (plugins, skills, MCP servers) come from untrusted sources. HOL Guard fills a genuine gap — SkillSpector scans skill files for malicious patterns statically, agentlint enforces runtime rules, but neither intercepts harness launches or package installs before execution. The four-level security model and receipt system are well-designed for team adoption. Skip for solo developers using only first-party extensions from Anthropic or well-known authors, where the launch overhead isn't justified. Re-evaluate once adoption grows and false positive data is available.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [hol-guard](https://github.com/hashgraph-online/hol-guard) | tool | AI antivirus for developer agents — scans plugins, skills, MCP servers before tools run | Downloaded agent extensions could be malicious; need pre-execution scanning | SkillSpector, agentlint |
