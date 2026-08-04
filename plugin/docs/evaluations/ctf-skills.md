# Evaluation: ctf-skills

**Repo:** [ljagiello/ctf-skills](https://github.com/ljagiello/ctf-skills)
**Stars:** 2,666 | **Last updated:** 2026-07-01 (pushed) | **License:** MIT
**Dev loop stage:** Review (security, out of scope)
**Layer:** Tooling
**Last verified:** 2026-08-04
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->

---

## What it does

Agent skills for capture-the-flag categories — web exploitation, pwn, cryptography, reverse
engineering, forensics and OSINT — each with its own playbook and tooling.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this. Source-grounded only: GitHub metadata (fetched 2026-08-04)
plus the CATALOG one-liner and "Overlaps with" cell (`pentest-ai`, `Claude-BugHunter`,
`OpenOSINT`). Sufficient for a scope-based SKIP; not sufficient for a positive verdict, and none is
offered.

## Verdict

**SKIP** — off-scope. The Security & Safety category defines itself as *"Tools for scanning
agent-generated code and skills for vulnerabilities"*, and CTF play is a different activity
entirely: solving deliberately-planted puzzles in a competition, against binaries and services
someone built to be broken.

It is the sharpest case in the cluster this pass disposed (`pentest-ai`, `pentest-ai-agents`,
`Claude-BugHunter`, `cve-mcp-server`, `ida-pro-mcp`), because the others at least point at real
systems. Nothing here touches the loop between writing code and shipping it.

MIT and ★2.7K, so this is a scope call and not a quality one — competitive security is a real craft
with a real audience, and the row stays findable for anyone who wants it.

Re-open if this catalog widens past the dev loop, or for a security-training context where CTF
tooling is the point.
_Triaged 2026-08-04 by the P3 backlog band ([#268](https://github.com/mattbutlerengineering/ai-tooling/issues/268))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [ctf-skills](https://github.com/ljagiello/ctf-skills) | skill | Agent skills for CTF challenges — web, pwn, crypto, reverse engineering, forensics, OSINT | Solving each CTF category with an agent needs specialized per-domain tooling and playbooks | pentest-ai, Claude-BugHunter, OpenOSINT |
