# Evaluation: trailofbits/skills

**Repo:** [trailofbits/skills](https://github.com/trailofbits/skills)
**Stars:** 5,748 | **Last updated:** 2026-06-17 | **License:** CC-BY-SA-4.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-07-09  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

Claude Code plugin marketplace from Trail of Bits with 10+ security skills covering smart contract security, C/C++ review, GitHub Actions auditing, differential review, Burp Suite integration, and dimensional analysis for formula bugs. Each skill encodes real audit methodology from one of the most respected security firms in the industry — structured approaches to finding vulnerabilities rather than generic "scan for common issues" prompting.

## How we tested it

**Evidence:** REVIEW

**Marketplace/inventory review — full audit not run.** Inspected the actual plugin set via the GitHub API (`repos/trailofbits/skills/contents/plugins`) and read the skill structure, rather than recording a live audit of a target codebase (a meaningful audit run is interactive and codebase-specific, not a scriptable one-shot). The repo ships as a Claude Code plugin marketplace:

```
/plugin marketplace add trailofbits/skills
```

The inventory is **~39 plugins**, broader than "10+ security skills." Security/audit methodology skills include `building-secure-contracts` (smart contracts), `c-review` (C/C++), `agentic-actions-auditor` (GitHub Actions), `differential-review`, `burpsuite-project-parser`, `dimensional-analysis` (formula/unit bugs), `constant-time-analysis`, `variant-analysis`, `static-analysis`, `semgrep-rule-creator`, `yara-authoring`, `supply-chain-risk-auditor`, `insecure-defaults`, and `property-based-testing` / `mutation-testing`. Notably, several plugins are **not** security-specific (`modern-python`, `gh-cli`, `git-cleanup`, `devcontainer-setup`, `let-fate-decide`, `culture-index`) — so the "security skills" framing oversells a general-purpose toolbox.

## What worked (from the inventory review)

- **The methodology framing is the real differentiator.** Skills like `differential-review` (review only what changed) and `audit-context-building` encode *how to audit systematically* — a structured pass over categories — rather than a generic "find security bugs" prompt that returns a wall of maybe-issues.
- **`differential-review` is a strong fit for a pre-merge security gate** in the Review stage — it scopes to the diff instead of re-auditing the whole tree.
- **Backed by Trail of Bits**, a respected audit firm, so the encoded approach plausibly reflects real-world practice (reputation, not a claim we verified by running an audit here).

## What didn't work or surprised us

- **The "security skills" label undersells/over-frames the set** — it's ~39 plugins, many general-purpose (Python tooling, git hygiene). Treat it as a grab-bag marketplace, not a focused security suite.
- **Smart-contract and binary skills (`building-secure-contracts`, `dwarf-expert`, `constant-time-analysis`) are dead weight for typical web development** unless you're in those domains.
- **Several skills assume Trail of Bits / specialist tooling** (Semgrep, YARA, property-based/mutation testing harnesses) that most teams won't have installed.
- **CC-BY-SA-4.0** means derivatives must use the same license — fine for usage, notable for modification.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Targets security review, not business-logic correctness. |
| Speed | neutral | Adds review time; `differential-review` limits scope to the diff. |
| Maintainability | neutral | No impact on code structure. |
| Safety | + (by design) | Encodes structured, evidence-first audit methodology — not yet confirmed by a run here. |
| Cost Efficiency | + (claimed) | Structured methodology should mean fewer noisy passes than generic prompting. |

## Verdict

**SKIP** — CC-BY-SA-4.0 ShareAlike. A skill/plugin is *vendored* into the consuming repo, so ShareAlike would attach to the repo that copies the skill text in.

_Superseded the review-based read below on 2026-07-09 (bulk license triage, P4 mechanical-skip). The read was never wrong about the tool's quality — the licence, not the craft, is disqualifying._

**CONDITIONAL** (review-based)

The structured methodology is the genuine differentiator versus generic "find security bugs" prompting, and `differential-review` is a sensible pre-merge security gate. Held at CONDITIONAL rather than ADOPT for two reasons: this evaluation is an inventory review, not a recorded audit run; and the package is a broad ~39-plugin marketplace where only a subset is security methodology — install selectively rather than wholesale. Best paired with the first-party `security-guidance` plugin (in-loop diff review) and used as a deliberate Review-stage pass.

**Comparison with ghostsecurity/skills:** Trail of Bits is methodology-focused (how to audit systematically), ghostsecurity is tool-focused (what to scan for in specific frameworks). They're complementary, not redundant — use Trail of Bits for the audit structure and ghostsecurity for framework-specific checklists.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [trailofbits/skills](https://github.com/trailofbits/skills) | plugin | Professional security audit methodology from Trail of Bits | Generic security prompts produce noise; structured methodology produces evidence-based findings | ghostsecurity/skills, SkillSpector |
