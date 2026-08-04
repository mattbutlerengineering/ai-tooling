# Evaluation: strix

**Repo:** [usestrix/strix](https://github.com/usestrix/strix)
**Stars:** 39,682 | **Last updated:** 2026-07-10 (pushed) | **License:** Apache-2.0
**Dev loop stage:** Review (security)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

LLM agents that find and help fix application vulnerabilities in authorized security engagements.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`pentest-ai`, `pentest-ai-agents`,
`Claude-BugHunter`, `garak`). Enough to place it against the cluster this pass disposed; not enough
for a positive verdict, and none is offered.

## Triage note

Left at `discovery-log` — the one survivor of a cluster this pass otherwise SKIPped as off-scope.

Four of its five overlap neighbours were disposed here (`pentest-ai`, `pentest-ai-agents`,
`Claude-BugHunter`, plus `cve-mcp-server` and `ida-pro-mcp` nearby), all on the same ground: they
serve an offensive-security practice rather than the dev loop. strix reads differently. *"Find and
fix application vulnerabilities"* on **your** application is the question a developer actually has
after an agent writes code, which is exactly what the Security & Safety blurb scopes in.

Scale is the second reason not to bulk-dispose it. ★39.7K, Apache-2.0, pushed 2026-07-10 — this is
the largest security entry in the catalog by an order of magnitude, and the difference between "AI
pentesting product" and "vulnerability review for code you own" is not decidable from a one-liner.

The genuine question is whether it duplicates [`trailofbits/skills`](https://github.com/trailofbits/skills)
and the STACK `security-guidance` plugin, or reaches something they do not — running the app and
probing it, rather than reading its source. That is a with/without read against a codebase with
known-planted vulnerabilities, which is P0 measurement work and not a call this lane may make.

The catalog one-liner said ★30K; corrected to ★39.7K from live metadata in this pass.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [strix](https://github.com/usestrix/strix) | tool | AI penetration testing (Apache-2.0, ★30K) — LLM agents that find and help fix application vulnerabilities in authorized engagements | Security testing requires manual expertise; automates vulnerability discovery with AI-driven pentesting | pentest-ai, pentest-ai-agents, Claude-BugHunter, garak |
