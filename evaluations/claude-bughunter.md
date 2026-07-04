# Evaluation: Claude-BugHunter

**Repo:** [elementalsouls/Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter)
**Stars:** 2,556 | **Last updated:** 2026-06-18 | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Review (external security testing)
**Layer:** Tooling

---

## What it does

A self-contained Claude Code skill bundle (plugin + 71 skills + 15 slash commands) for external bug bounty hunting and red-team engagements. Skills auto-load by topic — describe your target in plain English and the relevant hunt skill activates. Built from 681 disclosed HackerOne/Bugcrowd reports curated across 24 vulnerability classes.

Four layers stack: **Think** (methodology + red-team mindset), **Hunt webapps** (48 `hunt-*` skills covering OWASP-mapped bug classes), **Hit the perimeter** (enterprise platform attack chains for M365/Entra, Okta, vCenter, SSL VPN appliances, SharePoint), and **Ship it** (triage validation, VRT-aware severity, evidence hygiene, reporting). Also includes a Burp MCP integration for live HTTP interception.

Explicitly scoped to external attack surface only — internal AD attacks, C2 frameworks, post-exploit/persistence, and evasion are deliberately out of scope with clear documentation about what is and isn't covered.

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation: read the full README, examined the repo structure (71 skill directories, 14 command files, plugin.json manifest, eval harness), and read 4 representative SKILL.md files in full (hunt-xss, hunt-idor, bb-methodology, triage-validation) to assess depth, accuracy, and practical quality.

```bash
gh api repos/elementalsouls/Claude-BugHunter --jq '.description, .stargazers_count'
gh api repos/elementalsouls/Claude-BugHunter/contents/skills/hunt-xss/SKILL.md --jq '.content' | base64 -d
gh api repos/elementalsouls/Claude-BugHunter/contents/skills/bb-methodology/SKILL.md --jq '.content' | base64 -d
gh api repos/elementalsouls/Claude-BugHunter/contents/skills/triage-validation/SKILL.md --jq '.content' | base64 -d
gh api repos/elementalsouls/Claude-BugHunter/contents/skills/hunt-idor/SKILL.md --jq '.content' | base64 -d
```

Did not install or run against live targets — this is an architecture/content review, not a hands-on pentest evaluation.

## What worked

- **Report-derived, not theory-derived.** Each `hunt-*` skill cites the number of public reports it was built from (e.g., hunt-xss: 174 reports, hunt-idor: 26 reports). Attack patterns, bypass tables, and chain templates come from real disclosed findings, not generic OWASP checklists.
- **The 7-Question Gate in triage-validation is excellent.** It forces validation before reporting: "Can an attacker use this RIGHT NOW, step by step?" with a template requiring exact HTTP request, response, and impact. One wrong answer = kill the finding. This discipline prevents the flood of informational findings that plague automated security scanning.
- **OOB-or-it-didn't-happen verification.** The hunt-xss skill explicitly distinguishes what IS and what IS NOT confirmation of blind/stored XSS, with concrete examples of false signals (encoded output, WAF rejection) vs. real confirmation (Collaborator callback with browser User-Agent). This level of precision is rare.
- **Clear scope boundaries.** The README explicitly states what the bundle does NOT cover (internal AD, C2, persistence, evasion) with rationale — not gaps, design decisions. This prevents misuse and sets correct expectations.
- **Proper plugin packaging.** Ships as a Claude Code plugin (plugin.json v2.1.0) with namespaced commands, not just loose skill files. Multi-harness install script supports Claude Code, OpenCode, Codex CLI, and Hermes Agent.
- **Built-in eval harness with ablation.** The eval/ directory runs the skills against OWASP Juice Shop and PortSwigger Academy labs with a skills-on/skills-off comparison to measure actual skill delta. This is the only security skill bundle we've seen that includes empirical validation.

## What didn't work or surprised us

- **Offensive-only scope.** This is a bug hunting and external red-team tool, not a defensive code review tool. It does NOT help you find vulnerabilities in code you're writing — it helps you find vulnerabilities in running applications you're testing. For defensive code review, trailofbits/skills and ghostsecurity/skills remain the right tools.
- **No hands-on verification.** We reviewed skill content quality but did not run the skills against live targets. The eval harness exists but requires Docker + Burp MCP setup — not feasible for a quick catalog evaluation.
- **Requires Burp Suite for full capability.** The Burp MCP integration is a key part of the workflow (HTTP interception, request replay). Without it, the skills provide knowledge but lose the "hands" for live testing.
- **Large context footprint.** 71 skills loading by topic description means multiple skills could activate simultaneously. Each SKILL.md is dense (the ones we read were 200-400 lines). Cost implications for long engagements.
- **License listed as NOASSERTION on GitHub API** despite README/plugin.json claiming MIT. Minor concern — the plugin.json explicitly says MIT.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | This is an external testing tool, not a code correctness tool |
| Speed | + | Structured methodology and auto-loaded vulnerability-class skills accelerate manual pentest/bug-bounty workflows |
| Maintainability | neutral | Does not affect codebase maintainability |
| Safety | + | The triage-validation gates, scope discipline, and evidence-hygiene rules prevent low-quality findings and ensure responsible disclosure |
| Cost Efficiency | - | Large skill bundle means higher context usage per session; Burp Suite Pro is a paid dependency for full capability |

## Verdict

**CONDITIONAL**

Use when conducting authorized external security testing — bug bounty programs, penetration tests, or red-team engagements. The report-derived hunt skills and the 7-Question Gate triage methodology are significantly more rigorous than generic security scanning prompts. Not a replacement for trailofbits/skills (defensive code review) or ghostsecurity/skills (AppSec during development) — those operate at the Review stage on code you're writing, while Claude-BugHunter operates at the external testing stage against running applications you're authorized to test.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Claude-BugHunter](https://github.com/elementalsouls/Claude-BugHunter) | skill | Bug hunting and red-team skill bundle — 71 skills, 15 slash commands, 681 disclosed-report patterns | External security testing lacks structure; provides vulnerability-class-organized hunting patterns | ghostsecurity/skills, Anthropic-Cybersecurity-Skills, pentest-ai |
