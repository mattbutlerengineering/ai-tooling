# Evaluation: Anthropic-Cybersecurity-Skills

**Repo:** [mukul975/Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills)
**Stars:** 16,444 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

The largest open-source cybersecurity skills library for AI agents: 754 structured skills across 26 security domains, each following the agentskills.io standard. Every skill is mapped to five industry frameworks (MITRE ATT&CK v19.1, NIST CSF 2.0, MITRE ATLAS, MITRE D3FEND, NIST AI RMF) — no other open-source skills library provides unified cross-framework coverage. Skills range from forensic disk imaging to Kubernetes RBAC to ransomware response.

Each skill has a consistent structure: YAML frontmatter with framework mappings, a SKILL.md with "When to Use" / "Prerequisites" / multi-step "Workflow" sections, a `references/api-reference.md` with tool-specific API cheatsheets, and a `scripts/agent.py` with runnable Python for the skill's core logic (e.g., Shannon entropy calculation for C2 traffic). Progressive disclosure lets agents scan all 754 frontmatters (~30 tokens each) and fully load only the relevant skill (500–2,000 tokens).

Ships as a Claude Code plugin (`.claude-plugin/plugin.json`) and installs with `npx skills add`. Same author as `cve-mcp-server` (1,030 stars) — consistent security-domain quality.

## How we tested it

**Evidence:** REVIEW

Architecture-review evaluation: read the README, examined repo structure, checked the index.json, and read 2 complete SKILL.md files plus their companion `references/` and `scripts/` directories.

```bash
gh api repos/mukul975/Anthropic-Cybersecurity-Skills --jq '.description, .stargazers_count, .updated_at'
gh api 'repos/mukul975/Anthropic-Cybersecurity-Skills/contents/skills/analyzing-network-traffic-of-malware/SKILL.md' --jq '.content' | base64 -d
gh api 'repos/mukul975/Anthropic-Cybersecurity-Skills/contents/skills/acquiring-disk-image-with-dd-and-dcfldd/SKILL.md' --jq '.content' | base64 -d
gh api 'repos/mukul975/Anthropic-Cybersecurity-Skills/contents/skills/analyzing-network-traffic-of-malware/scripts/agent.py' --jq '.content' | base64 -d
gh api 'repos/mukul975/Anthropic-Cybersecurity-Skills/contents/skills/analyzing-network-traffic-of-malware/references/api-reference.md' --jq '.content' | base64 -d
```

Did not install the full 754-skill collection — this is a content/architecture review.

## What worked

- **Genuine depth per skill.** The two sampled skills (`analyzing-network-traffic-of-malware` at 340 lines, `acquiring-disk-image-with-dd-and-dcfldd` at 247 lines) are full practitioner workflows with tool-specific commands (tshark, Zeek, Suricata, dd, dcfldd), decision trees, and concrete examples — not generic OWASP checklists.
- **Companion artifacts add real value.** Each skill ships with `references/api-reference.md` (tool API cheatsheets the agent can consult mid-workflow) and `scripts/agent.py` (runnable Python implementing the skill's core logic). The malware traffic skill's agent.py includes a Shannon entropy calculator for detecting encrypted C2 channels — that's tool-specific, not generated filler.
- **Five-framework mapping is unique.** A single skill like `analyzing-network-traffic-of-malware` maps to ATT&CK T1071.001, NIST CSF DE.CM-01, ATLAS AML.T0047, D3FEND D3-NTA, and AI RMF MEASURE-2.6. This matters for compliance teams that need coverage evidence across frameworks simultaneously.
- **Progressive disclosure is well-designed.** ~30 token frontmatter scan per skill means searching all 754 in one pass is feasible (~22K tokens). Full load is 500–2,000 tokens per skill — targeted and efficient.
- **26 domains cover the full security landscape.** From cloud security (60 skills) and threat hunting (55) to niche areas like OT/ICS security (28) and deception technology (2). Coverage extends far beyond web-app security.

## What didn't work or surprised us

- **754 skills installed at once is impractical.** No selective install — `npx skills add` pulls the entire collection. For Claude Code, this means all 754 skills compete for activation, creating noise when working on non-security tasks. Selective domain install (e.g., `npx skills add mukul975/Anthropic-Cybersecurity-Skills@web-application-security`) is not available.
- **Not tested hands-on against real targets.** The quality assessment is architectural — the skills read well, but we haven't verified that an agent following the `analyzing-network-traffic-of-malware` workflow on a real PCAP produces better results than the agent's baseline knowledge.
- **Overlap with existing security catalog entries is significant but complementary.** trailofbits/skills (ADOPT) covers code-review-oriented security with audit methodology; Claude-BugHunter (CONDITIONAL) covers external bug bounty with report patterns. This collection covers the full SOC/DFIR/threat-hunting spectrum — different audience, different use case.
- **"Anthropic" in the name is misleading.** The repo header warns "Not affiliated with Anthropic PBC" but the name implies official endorsement. This may confuse users.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Skills encode correct tool usage but we didn't verify against real targets |
| Speed | + | Framework mappings eliminate manual compliance cross-referencing |
| Maintainability | neutral | Skills are self-contained but the 754-skill collection is all-or-nothing |
| Safety | + | 26 domains cover defensive, offensive, and compliance workflows comprehensively |
| Cost Efficiency | + | Progressive disclosure (~30 tokens/scan) keeps context costs manageable |

## Verdict

**CONDITIONAL**

Use when doing dedicated security work — incident response, threat hunting, forensics, penetration testing, or compliance mapping. The five-framework coverage and practitioner-level depth per skill set this apart from both trailofbits/skills (code-review security, ADOPT) and Claude-BugHunter (external bug bounty, CONDITIONAL). Not recommended for general development where only the occasional security review is needed — the 754-skill collection adds weight without benefit outside security contexts, and trailofbits/skills covers that use case better.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Anthropic-Cybersecurity-Skills](https://github.com/mukul975/Anthropic-Cybersecurity-Skills) | skill | 754 cybersecurity skills mapped to MITRE ATT&CK, NIST CSF, D3FEND, and ATLAS frameworks | Need comprehensive security skills aligned with industry frameworks | trailofbits/skills, ghostsecurity/skills |
