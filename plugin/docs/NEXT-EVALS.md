# Next evals — a banded promotion queue

The 393 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 103 distinct values across these 393 leads (158 have zero overlap pressure; largest tie: 22) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 118 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 240 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 10 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| opencode | Implement | 54.9 | pressure 24, gap 4.9 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 42.2 | pressure 17, gap 6.2 | `/evaluate-tool cognee` |
| agent-browser | Verify | 39.0 | pressure 16, gap 5.0 | `/evaluate-tool agent-browser` |
| ECC | Implement | 36.9 | pressure 15, gap 4.9 | `/evaluate-tool ECC` |
| langfuse | Outer Loop | 36.5 | pressure 15, gap 6.5 | `/evaluate-tool langfuse` |
| spec-kit | Plan | 35.2 | pressure 14, gap 5.2 | `/evaluate-tool spec-kit` |
| OpenHands | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool OpenHands` |
| goose | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool supermemory` |
| claude-hud | Plan | 33.2 | pressure 13, gap 5.2 | `/evaluate-tool claude-hud` |
| awesome-claude-code | Reference | 33.0 | pressure 12, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| mem0 | Memory & Context | 32.2 | pressure 12, gap 6.2 | `/evaluate-tool mem0` |
| sandcastle | Implement | 30.9 | pressure 12, gap 4.9 | `/evaluate-tool sandcastle` |
| MemOS | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool MemOS` |
| OpenSpec | Plan | 29.2 | pressure 11, gap 5.2 | `/evaluate-tool OpenSpec` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool opik` |
| orca | Implement | 32.9 | pressure 13, gap 4.9 | `/evaluate-tool orca` |
| aider | Implement | 30.9 | pressure 13, gap 4.9 | `/evaluate-tool aider` |
| agentmemory | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool agentmemory` |
| ghostsecurity/skills | Review | 27.3 | pressure 10, gap 5.3 | `/evaluate-tool ghostsecurity/skills` |
| browser-use | Verify | 27.0 | pressure 10, gap 5.0 | `/evaluate-tool browser-use` |
| ui-ux-pro-max | Skills & Plugins | 26.5 | pressure 9, gap 6.5 | `/evaluate-tool ui-ux-pro-max` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 118 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 118 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| vet | Review | 25.3 | challenges code-review, pr-review-toolkit · pressure 9, gap 5.3 | `/triage-lead vet` |
| gstack | Implement | 24.9 | challenges GSD · pressure 9, gap 4.9 | `/triage-lead gstack` |
| ruflo | Implement | 24.9 | challenges GSD · pressure 9, gap 4.9 | `/triage-lead ruflo` |
| ACE (agentic-context-engine) | Memory & Context | 24.2 | challenges claude-reflect · pressure 8, gap 6.2 | `/triage-lead ACE (agentic-context-engine)` |
| memU | Memory & Context | 24.2 | challenges claude-mem · pressure 8, gap 6.2 | `/triage-lead memU` |
| claude-octopus | Review | 23.3 | challenges code-review · pressure 8, gap 5.3 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.3 | challenges GSD, pr-review-toolkit, stryker-js · pressure 8, gap 5.3 | `/triage-lead tdd-guard` |
| Understand-Anything | Plan | 23.2 | challenges codegraph · pressure 8, gap 5.2 | `/triage-lead Understand-Anything` |
| gastown | Implement | 22.9 | challenges claude-squad · pressure 8, gap 4.9 | `/triage-lead gastown` |
| ralph-claude-code | Implement | 22.9 | challenges GSD · pressure 8, gap 4.9 | `/triage-lead ralph-claude-code` |
| compound-engineering | Implement | 20.9 | challenges GSD · pressure 7, gap 4.9 | `/triage-lead compound-engineering` |
| andrej-karpathy-skills | Skills & Plugins | 20.5 | challenges agent-skills, documentation-and-adrs, mattpocock/skills · pressure 6, gap 6.5 | `/triage-lead andrej-karpathy-skills` |

## P3 backlog — 240 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 240 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| qwen-code | Implement | 24.9 | pressure 9, gap 4.9 | `/triage-lead qwen-code` |
| impeccable | Skills & Plugins | 24.5 | pressure 8, gap 6.5 | `/triage-lead impeccable` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| gemini-cli | Implement | 22.9 | pressure 8, gap 4.9 | `/triage-lead gemini-cli` |
| slidev | Skills & Plugins | 22.5 | pressure 7, gap 6.5 | `/triage-lead slidev` |
| ccpm | Plan | 21.2 | pressure 7, gap 5.2 | `/triage-lead ccpm` |
| buildwithclaude | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead fast-agent` |
| worktrunk | Ship | 20.7 | pressure 6, gap 6.7 | `/triage-lead worktrunk` |
| Helicone | Outer Loop | 20.5 | pressure 6, gap 6.5 | `/triage-lead Helicone` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 10 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why | Command |
|------|-------|-------|-----|---------|
| prisma | MCP Servers | 14.7 | ships inside `prisma/prisma` · pressure 3, gap 6.7 | `/triage-lead prisma` |
| plugin-dev | Skills & Plugins | 12.5 | ships inside `anthropics/claude-plugins-official` · pressure 2, gap 6.5 | `/triage-lead plugin-dev` |
| codebase-design | Plan | 9.2 | ships inside `mattpocock/skills` · pressure 1, gap 5.2 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.2 | ships inside `mattpocock/skills` · pressure 1, gap 5.2 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead confluence` |
| jira | MCP Servers | 8.7 | ships inside `sooperset/mcp-atlassian` · pressure 0, gap 6.7 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.5 | ships inside `github/awesome-copilot` · pressure 0, gap 6.5 | `/triage-lead typescript-mcp-server-generator` |
| diagnosing-bugs | Verify | 7.0 | ships inside `mattpocock/skills` · pressure 0, gap 5.0 | `/triage-lead diagnosing-bugs` |
| implement | Implement | 6.9 | ships inside `mattpocock/skills` · pressure 0, gap 4.9 | `/triage-lead implement` |
| presentation-creator | Skills & Plugins | 6.5 | ships inside `getsentry/skills` · pressure 0, gap 6.5 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
