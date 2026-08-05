# Next evals — a banded promotion queue

The 367 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 97 distinct values across these 367 leads (142 have zero overlap pressure; largest tie: 22) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 108 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 234 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 54.8 | pressure 24, gap 4.8 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.3 | pressure 16, gap 6.3 | `/evaluate-tool cognee` |
| agent-browser | Verify | 37.2 | pressure 15, gap 5.2 | `/evaluate-tool agent-browser` |
| langfuse | Outer Loop | 36.4 | pressure 15, gap 6.4 | `/evaluate-tool langfuse` |
| ECC | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool ECC` |
| OpenHands | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 34.8 | pressure 14, gap 4.8 | `/evaluate-tool goose` |
| promptfoo | Outer Loop | 34.4 | pressure 13, gap 6.4 | `/evaluate-tool promptfoo` |
| supermemory | Memory & Context | 34.3 | pressure 13, gap 6.3 | `/evaluate-tool supermemory` |
| spec-kit | Plan | 33.1 | pressure 13, gap 5.1 | `/evaluate-tool spec-kit` |
| awesome-claude-code | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool vercel-labs/agent-skills` |
| MemOS | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| opik | Outer Loop | 28.4 | pressure 10, gap 6.4 | `/evaluate-tool opik` |
| OpenSpec | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool claude-hud` |
| sandcastle | Implement | 26.8 | pressure 10, gap 4.8 | `/evaluate-tool sandcastle` |
| browser-use | Verify | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool browser-use` |
| chrome-devtools-mcp | Verify | 25.2 | pressure 9, gap 5.2 | `/evaluate-tool chrome-devtools-mcp` |
| orca | Implement | 28.8 | pressure 11, gap 4.8 | `/evaluate-tool orca` |
| ghostsecurity/skills | Review | 25.1 | pressure 9, gap 5.1 | `/evaluate-tool ghostsecurity/skills` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 108 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 108 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| vet | Review | 25.1 | pressure 9, gap 5.1 | `/triage-lead vet` |
| aider | Implement | 24.8 | pressure 10, gap 4.8 | `/triage-lead aider` |
| gstack | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead gstack` |
| ruflo | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead ruflo` |
| agentmemory | Memory & Context | 24.3 | pressure 8, gap 6.3 | `/triage-lead agentmemory` |
| memU | Memory & Context | 24.3 | pressure 8, gap 6.3 | `/triage-lead memU` |
| claude-octopus | Review | 23.1 | pressure 8, gap 5.1 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.1 | pressure 8, gap 5.1 | `/triage-lead tdd-guard` |
| Understand-Anything | Plan | 23.1 | pressure 8, gap 5.1 | `/triage-lead Understand-Anything` |
| gastown | Implement | 22.8 | pressure 8, gap 4.8 | `/triage-lead gastown` |
| ACE (agentic-context-engine) | Memory & Context | 22.3 | pressure 8, gap 6.3 | `/triage-lead ACE (agentic-context-engine)` |
| compound-engineering | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead compound-engineering` |

## P3 backlog — 234 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 234 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 24.8 | pressure 9, gap 4.8 | `/triage-lead qwen-code` |
| ui-ux-pro-max | Skills & Plugins | 24.3 | pressure 8, gap 6.3 | `/triage-lead ui-ux-pro-max` |
| awesome-claude-skills (Composio) | Reference | 23.0 | pressure 7, gap 7.0 | `/triage-lead awesome-claude-skills (Composio)` |
| gemini-cli | Implement | 22.8 | pressure 8, gap 4.8 | `/triage-lead gemini-cli` |
| impeccable | Skills & Plugins | 22.3 | pressure 7, gap 6.3 | `/triage-lead impeccable` |
| slidev | Skills & Plugins | 22.3 | pressure 7, gap 6.3 | `/triage-lead slidev` |
| ag-ui | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead ag-ui` |
| buildwithclaude | Reference | 21.0 | pressure 6, gap 7.0 | `/triage-lead buildwithclaude` |
| CLIProxyAPI | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 20.8 | pressure 7, gap 4.8 | `/triage-lead fast-agent` |
| worktrunk | Ship | 20.7 | pressure 6, gap 6.7 | `/triage-lead worktrunk` |
| Helicone | Outer Loop | 20.4 | pressure 6, gap 6.4 | `/triage-lead Helicone` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
