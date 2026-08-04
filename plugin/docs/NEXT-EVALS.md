# Next evals — a banded promotion queue

The 402 `discovery-log` leads, **derived** (not hand-maintained) from data already in the repo plus `repo-metadata.json`. Regenerate with `python3 triage.py`; do not edit between the markers.

Leads are grouped into **bands**, not a single ranked list. Within a band the order is `2*overlap_pressure + stage_gap_weight + evidence_bonus` (see `next-evals.py`), but that score has only 96 distinct values across these 402 leads (159 have zero overlap pressure; largest tie: 33) — enough to pick a head, not to rank a tail. Leads already stamped `**Last triaged:**` sink within their band so each pass surfaces un-examined ones.

**Eliminate-only.** Outside `P0 measure`, an unattended agent may SKIP a lead or leave it at `discovery-log`; it may never write ADOPT/KEEP/CONDITIONAL. A false SKIP is cheap and reversible; a false ADOPT poisons STACK. Detector Q gates this.

| Band | Definition | Leads | An agent may conclude |
|------|------------|-------|-----------------------|
| **P0 measure** | score-ranked head | 25 | human or `eval-runner` only — the one band that may reach ADOPT |
| **P1 successor-check** | `archived == true` | 0 | repoint the link to a successor, or SKIP "archived, no successor" |
| **P2 challenger** | overlaps a tool already in STACK | 107 | SKIP "redundant with `<incumbent>`", or leave at discovery-log |
| **P3 backlog** | everything else | 270 | leave; stamp `**Last triaged:**` only |
| **P4 mechanical-skip** | vendored Type under a disqualifying license | 0 | SKIP — zero judgement |

<!-- NEXT-EVALS:START -->

## P0 measure — 25 leads

_human or `eval-runner` only — the one band that may reach ADOPT._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| opencode | Implement | 56.8 | pressure 24, gap 6.8 | `/evaluate-tool opencode` |
| cognee | Memory & Context | 40.2 | pressure 16, gap 6.2 | `/evaluate-tool cognee` |
| agent-browser | Verify | 37.5 | pressure 15, gap 5.5 | `/evaluate-tool agent-browser` |
| ECC | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool ECC` |
| OpenHands | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool OpenHands` |
| goose | Implement | 36.8 | pressure 14, gap 6.8 | `/evaluate-tool goose` |
| langfuse | Outer Loop | 36.2 | pressure 15, gap 6.2 | `/evaluate-tool langfuse` |
| supermemory | Memory & Context | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool supermemory` |
| promptfoo | Outer Loop | 34.2 | pressure 13, gap 6.2 | `/evaluate-tool promptfoo` |
| spec-kit | Plan | 33.1 | pressure 13, gap 5.1 | `/evaluate-tool spec-kit` |
| pydantic-ai | Implement | 32.8 | pressure 12, gap 6.8 | `/evaluate-tool pydantic-ai` |
| awesome-claude-code | Reference | 31.0 | pressure 11, gap 7.0 | `/evaluate-tool awesome-claude-code` |
| tech-leads-club/agent-skills | Skills & Plugins | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool tech-leads-club/agent-skills` |
| vercel-labs/agent-skills | Skills & Plugins | 30.3 | pressure 11, gap 6.3 | `/evaluate-tool vercel-labs/agent-skills` |
| MemOS | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool MemOS` |
| mem0 | Memory & Context | 30.2 | pressure 11, gap 6.2 | `/evaluate-tool mem0` |
| awesome-agent-skills | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills` |
| awesome-agent-skills (libukai) | Reference | 29.0 | pressure 10, gap 7.0 | `/evaluate-tool awesome-agent-skills (libukai)` |
| sandcastle | Implement | 28.8 | pressure 10, gap 6.8 | `/evaluate-tool sandcastle` |
| opik | Outer Loop | 28.2 | pressure 10, gap 6.2 | `/evaluate-tool opik` |
| OpenSpec | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool OpenSpec` |
| claude-hud | Plan | 27.1 | pressure 10, gap 5.1 | `/evaluate-tool claude-hud` |
| agent-kit | Implement | 26.8 | pressure 9, gap 6.8 | `/evaluate-tool agent-kit` |
| aider | Implement | 26.8 | pressure 10, gap 6.8 | `/evaluate-tool aider` |
| gstack | Implement | 26.8 | pressure 9, gap 6.8 | `/evaluate-tool gstack` |

## P1 successor-check — 0 leads

_repoint the link to a successor, or SKIP "archived, no successor"._

_(none)_

## P2 challenger — 107 leads

_SKIP "redundant with `<incumbent>`", or leave at discovery-log._

_Listing 12 of 107 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| browser-use | Verify | 25.5 | pressure 9, gap 5.5 | `/triage-lead browser-use` |
| chrome-devtools-mcp | Verify | 25.5 | pressure 9, gap 5.5 | `/triage-lead chrome-devtools-mcp` |
| orca | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead orca` |
| ruflo | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead ruflo` |
| ghostsecurity/skills | Review | 25.0 | pressure 9, gap 5.0 | `/triage-lead ghostsecurity/skills` |
| vet | Review | 25.0 | pressure 9, gap 5.0 | `/triage-lead vet` |
| gastown | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead gastown` |
| agentmemory | Memory & Context | 24.2 | pressure 8, gap 6.2 | `/triage-lead agentmemory` |
| memU | Memory & Context | 24.2 | pressure 8, gap 6.2 | `/triage-lead memU` |
| Understand-Anything | Plan | 23.1 | pressure 8, gap 5.1 | `/triage-lead Understand-Anything` |
| claude-octopus | Review | 23.0 | pressure 8, gap 5.0 | `/triage-lead claude-octopus` |
| tdd-guard | Review | 23.0 | pressure 8, gap 5.0 | `/triage-lead tdd-guard` |

## P3 backlog — 270 leads

_leave; stamp `**Last triaged:**` only._

_Listing 12 of 270 — rerun `python3 triage.py` and read the source for the tail (no silent cap)._

| Tool | Stage | Score | Why (pressure/gap) | Command |
|------|-------|-------|--------------------|---------|
| qwen-code | Implement | 26.8 | pressure 9, gap 6.8 | `/triage-lead qwen-code` |
| CopilotKit | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead CopilotKit` |
| daytona | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead daytona` |
| gemini-cli | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead gemini-cli` |
| voltagent | Implement | 24.8 | pressure 8, gap 6.8 | `/triage-lead voltagent` |
| CLIProxyAPI | Implement | 22.8 | pressure 7, gap 6.8 | `/triage-lead CLIProxyAPI` |
| fast-agent | Implement | 22.8 | pressure 7, gap 6.8 | `/triage-lead fast-agent` |
| bifrost | Implement | 20.8 | pressure 6, gap 6.8 | `/triage-lead bifrost` |
| gptme | Implement | 20.8 | pressure 6, gap 6.8 | `/triage-lead gptme` |
| haystack | Implement | 20.8 | pressure 6, gap 6.8 | `/triage-lead haystack` |
| kilocode | Implement | 20.8 | pressure 6, gap 6.8 | `/triage-lead kilocode` |
| google/skills | Skills & Plugins | 20.3 | pressure 6, gap 6.3 | `/triage-lead google/skills` |

## P4 mechanical-skip — 0 leads

_SKIP — zero judgement._

_(none)_

<!-- NEXT-EVALS:END -->
