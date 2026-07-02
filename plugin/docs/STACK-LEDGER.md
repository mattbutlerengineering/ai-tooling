# Stack Exclusion Ledger

Machine-readable record of **why each ADOPT/KEEP-verdict tool is or is not in [STACK.md](STACK.md)**.
Verdict data lives in [COMPARISON.md](COMPARISON.md) (what we concluded); STACK.md is the curated
install list (what we actually recommend). This ledger is the bridge: every ADOPT/KEEP tool maps to
either *in STACK*, *conditional*, or *excluded with a recorded reason* — so the reasoning is auditable
as data instead of buried in prose. It is the data foundation the stack-derivation drift gate (issue
\#70) consumes.

Covers all ADOPT- and KEEP-verdict tools in COMPARISON.md (DEFER/CONDITIONAL/SKIP rows are out of
scope). `In STACK?` values: `yes` (in a stage table) · `conditional` (in STACK's "Conditional"
section) · `no` (excluded — a reason is required). Exclusion reasons are grounded in each tool's
`## Verdict` in `evaluations/`.

## ADOPT / KEEP tools

| Tool | Verdict | Stage | In STACK? | Exclusion reason (required when `no`) |
|------|---------|-------|-----------|----------------------------------------|
| codegraph | ADOPT | Plan | yes | |
| context7 | KEEP | Plan | yes | |
| feature-dev | KEEP | Plan | yes | |
| GSD (Get Shit Done) | KEEP | Plan | yes | |
| markitdown | ADOPT | Plan | yes | |
| serena | ADOPT | Plan | conditional | |
| beads | KEEP | Implement | yes | |
| caveman | ADOPT | Implement | yes | |
| superpowers | ADOPT | Implement | yes | (install source for GSD — STACK installs `obra/superpowers`) |
| resolving-merge-conflicts | ADOPT | Implement | yes | (listed under STACK's Ship table) |
| playwright | ADOPT | Verify | yes | |
| code-review | KEEP | Review | yes | |
| pr-review-toolkit | KEEP | Review | yes | |
| security-guidance | ADOPT | Review | yes | |
| claude-code-action | ADOPT | Ship | yes | |
| claude-reflect | KEEP | Reflect | yes | |
| documentation-and-adrs | ADOPT | Reflect | yes | |
| documentation-writer | ADOPT | Reflect | no | Overlaps documentation-and-adrs (installed, the chosen Diátaxis/ADR pick); redundant standalone writer |
| ccusage | ADOPT | Outer Loop | yes | |
| codeburn | ADOPT | Outer Loop | no | Retrospective cross-tool cost analysis; abtop (live TUI) is the default outer-loop pick — pull in for multi-tool bills |
| agent-skills | ADOPT | Skills & Plugins | yes | |
| mattpocock/skills | ADOPT | Skills & Plugins | yes | |
| skill-creator | ADOPT | Skills & Plugins | conditional | |
| web-quality-skills | ADOPT | Verify | conditional | |
| cc-skills-golang | ADOPT | Skills & Plugins | no | Language-specific (Go only); verdict explicitly scoped, irrelevant outside Go projects |
| claude-mem | ADOPT | Memory & Context | yes | |
| OMEGA | KEEP | Memory & Context | no | Retained incumbent, not independently verified; claude-mem is the open, benchmarkable memory pick that holds the slot |
| fastmcp | ADOPT | MCP Servers | conditional | |
| github-mcp-server | ADOPT | MCP Servers | yes | |
| last30days-skill | ADOPT | Research & Discovery | yes | |
| agentskills | ADOPT | Reference | no | Canonical `SKILL.md` specification — a reference, not an installable tool |
| claude-plugins-official | KEEP | Reference | no | First-party marketplace/install channel (umbrella entry); member plugins are installed individually |
| dictionary-of-ai-coding | ADOPT | Reference | no | AI-coding terminology glossary — a reference to keep open, not an installable tool |
| mcp-for-beginners | ADOPT | Reference | no | MCP-learning curriculum — teaches the protocol, nothing to install |

## Batch exclusions

Group decisions that excluded a whole discovery batch from STACK, recorded as data rather than only
prose. (These batches are mostly CONDITIONAL/SKIP, so individual rows live in `evaluations/`, not the
ADOPT/KEEP table above.)

| Batch | Date | Tools | STACK decision | Rationale | Flagged for hands-on before any promotion |
|-------|------|-------|----------------|-----------|--------------------------------------------|
| 2026-06-19 discovery (#37) | 2026-06-19 | 19 | all excluded | All evaluated source-grounded, not run hands-on; none moved a quality signal in real testing. Rest are niche, overlapping, or methodology-not-tool. | code-on-incus (per-agent isolation + active defense; Security/Safety), brooks-lint (design-decay reviewer; Review) |
