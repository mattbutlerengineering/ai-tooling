# Next evals — a banded promotion queue

The 384 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 101 distinct values across these 384 leads (153 have zero overlap pressure; largest tie: 22) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 111 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 236 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |
| **P5 ships-inside** | the row declares a `Ships inside` container (#343) | 12 | settle the container, or SKIP "ships inside `<container>`" — never an independent lead |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 54.9 | pressure 24, gap 4.9 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.2 | pressure 16, gap 6.2 | `/evaluate-tool cognee` |
| agent-browser | Verify | 36.8 | pressure 15, gap 4.8 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 36.5 | pressure 15, gap 6.5 | `/evaluate-tool langfuse` |
| ECC | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool ECC` |
| OpenHands | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool OpenHands` |
| goose | Implement | 34.9 | pressure 14, gap 4.9 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.5 | pressure 13, gap 6.5 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool supermemory` |
| claude-hud | Plan | 33.2 | pressure 13, gap 5.2 | `/evaluate-tool claude-hud` |
| spec-kit | Plan | 33.2 | pressure 13, gap 5.2 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 33.0 | pressure 12, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| mem0 | Memory & Context | 32.2 | pressure 12, gap 6.2 | `/evaluate-tool mem0` |
| MemOS | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool MemOS` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| sandcastle | Implement | 28.9 | pressure 11, gap 4.9 | `/evaluate-tool sandcastle` |
| opik | Outer Loop | 28.5 | pressure 10, gap 6.5 | `/evaluate-tool opik` |
| OpenSpec | Plan | 27.2 | pressure 10, gap 5.2 | `/evaluate-tool OpenSpec` |
| aider | Implement | 30.9 | pressure 13, gap 4.9 | `/evaluate-tool aider` |
| orca | Implement | 30.9 | pressure 12, gap 4.9 | `/evaluate-tool orca` |
| agentmemory | Memory & Context | 28.2 | pressure 10, gap 6.2 | `/evaluate-tool agentmemory` |
| ui-ux-pro-max | Skills & Plugins | 26.6 | pressure 9, gap 6.6 | `/evaluate-tool ui-ux-pro-max` |
| ghostsecurity/skills | Review | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool ghostsecurity/skills` |
| vet | Review | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool vet` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 111 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 111 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| tech-leads-club/agent-skills | Skills & Plugins | 8.6 | pressure 0, gap 6.6 | `/triage-lead tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 8.6 | pressure 0, gap 6.6 | `/triage-lead vercel-labs/agent-skills` |
| modelcontextprotocol/servers | MCP Servers | 6.7 | pressure 0, gap 6.7 | `/triage-lead modelcontextprotocol/servers` |
| getsentry/skills | Skills & Plugins | 6.6 | pressure 0, gap 6.6 | `/triage-lead getsentry/skills` |
| awesome-copilot | Reflect | 3.3 | pressure 0, gap 3.3 | `/triage-lead awesome-copilot` |
| gstack | Implement | 24.9 | pressure 9, gap 4.9 | `/triage-lead gstack` |
| ruflo | Implement | 24.9 | pressure 9, gap 4.9 | `/triage-lead ruflo` |
| browser-use | Verify | 24.8 | pressure 9, gap 4.8 | `/triage-lead browser-use` |
| memU | Memory & Context | 24.2 | pressure 8, gap 6.2 | `/triage-lead memU` |
| claude-octopus | Review | 23.2 | pressure 8, gap 5.2 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.2 | pressure 8, gap 5.2 | `/triage-lead tdd-guard` |
| Understand-Anything | Plan | 23.2 | pressure 8, gap 5.2 | `/triage-lead Understand-Anything` |

## P3 backlog — 236 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 236 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| mcp-atlassian | MCP Servers | 6.7 | pressure 0, gap 6.7 | `/triage-lead mcp-atlassian` |
| qwen-code | Implement | 24.9 | pressure 9, gap 4.9 | `/triage-lead qwen-code` |
| impeccable | Skills & Plugins | 24.6 | pressure 8, gap 6.6 | `/triage-lead impeccable` |
| ag-ui | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead ag-ui` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| gemini-cli | Implement | 22.9 | pressure 8, gap 4.9 | `/triage-lead gemini-cli` |
| slidev | Skills & Plugins | 22.6 | pressure 7, gap 6.6 | `/triage-lead slidev` |
| buildwithclaude | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 20.9 | pressure 7, gap 4.9 | `/triage-lead fast-agent` |
| worktrunk | Ship | 20.7 | pressure 6, gap 6.7 | `/triage-lead worktrunk` |
| google/skills | Skills & Plugins | 20.6 | pressure 6, gap 6.6 | `/triage-lead google/skills` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

## P5 ships-inside — 12 leads

_settle the container, or SKIP "ships inside `<container>`" — never an independent lead._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| frontend-design | Skills & Plugins | 12.6 | pressure 3, gap 6.6 | `/triage-lead frontend-design` |
| plugin-dev | Skills & Plugins | 12.6 | pressure 2, gap 6.6 | `/triage-lead plugin-dev` |
| prisma | MCP Servers | 10.7 | pressure 2, gap 6.7 | `/triage-lead prisma` |
| server-memory | Memory & Context | 10.2 | pressure 1, gap 6.2 | `/triage-lead server-memory` |
| codebase-design | Plan | 9.2 | pressure 1, gap 5.2 | `/triage-lead codebase-design` |
| domain-modeling | Plan | 9.2 | pressure 1, gap 5.2 | `/triage-lead domain-modeling` |
| confluence | MCP Servers | 8.7 | pressure 0, gap 6.7 | `/triage-lead confluence` |
| jira | MCP Servers | 8.7 | pressure 0, gap 6.7 | `/triage-lead jira` |
| typescript-mcp-server-generator | Skills & Plugins | 8.6 | pressure 0, gap 6.6 | `/triage-lead typescript-mcp-server-generator` |
| implement | Implement | 6.9 | pressure 0, gap 4.9 | `/triage-lead implement` |
| diagnosing-bugs | Verify | 6.8 | pressure 0, gap 4.8 | `/triage-lead diagnosing-bugs` |
| presentation-creator | Skills & Plugins | 6.6 | pressure 0, gap 6.6 | `/triage-lead presentation-creator` |

<!-- NEXT-EVALS:END -->
