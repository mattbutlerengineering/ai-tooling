# Watchlist — what to revisit, and when

Everything worth re-evaluating or watching, **derived** (not hand-maintained) from data already in the repo: DEFER verdicts and their triggers, the STACK prose flags, the staleness sweep, and the unverified-claim / skill-measurement backlogs. Regenerate with `python3 watchlist.py`; do not edit between the markers. For *first-time* evaluation priorities see [NEXT-EVALS.md](NEXT-EVALS.md); this page is for *revisiting* work already started.

<!-- WATCHLIST:START -->

## 1. Deferred — re-evaluate when trigger fires (6)

Every `DEFER` verdict in the repo: promising but blocked, each with the re-evaluate trigger from its eval's `## Verdict` (per TEMPLATE.md's DEFER definition). A missing trigger is itself an action item. Most are [COMPARISON.md](COMPARISON.md) rows; an _eval-only_ entry is a DEFER carried by an eval with no catalog row — a bake-off or comparison document, whose subjects have their own rows — so it is linked to the eval instead.

| Tool | Stage | Re-evaluate when |
|------|-------|------------------|
| 8090 Software Factory | Plan | a hands-on budget is authorized, or when the "Try for Free" entry point is confirmed to be a durable free tier rather than a time-limited trial |
| [agentmemory-vs-claude-mem-bakeoff](evaluations/agentmemory-vs-claude-mem-bakeoff.md) _(eval-only)_ | Reflect | the three arms are actually run and the per-signal results recorded |
| Apache DevLake | Outer Loop | working in a team context or when managing multiple repos with CI/CD pipelines |
| letta | Memory & Context | your goal shifts from *augmenting a coding harness* to *building stateful agents into an application* |
| openwiki | Reflect | running `openwiki --init` + one `--update` cycle with a real key on a mid-size repo (grade the wiki for hallucinations and the update for churn), or when the package passes ~v0.1 with tests |
| SkillOpt | Skills & Plugins | a turnkey path from real dev sessions to a reward signal exists |

## 2. Flagged for hands-on before promotion (3)

Candidates the [STACK.md](STACK.md) prose flags for a hands-on eval before any promotion — surfaced by scanning STACK for its flag phrases (fragile by design; the durable fix is a machine-readable column in STACK-LEDGER.md).

| Tool | Flagged as |
|------|------------|
| worktrunk | pending a hands-on eval |
| [code-on-incus](https://github.com/mensfeld/code-on-incus) | flagged for a hands-on eval |
| [brooks-lint](https://github.com/hyhmrright/brooks-lint) | flagged for a hands-on eval |

<!-- WATCHLIST:STALE:START -->
## 3. Stale / undated evals (165 stale)

A point-in-time eval rots. The staleness sweep flags evals whose `**Last verified:**` date is older than its category threshold. This section is a **report**, refreshed by `make fix` — it is the one part of this page derived from today's date rather than from file content, so `watchlist.py --check` does not gate on it. Ages are not printed; only the crossing matters.

| Eval | Type | Last verified | Threshold (days) |
|------|------|---------------|------------------|
| Claude-Code-Game-Studios | harness | 2026-06-22 | 120 |
| CowAgent | harness | 2026-06-22 | 120 |
| OMEGA | MCP server | 2026-06-22 | 120 |
| OpenOSINT | MCP server | 2026-06-22 | 120 |
| agency-agents | harness | 2026-06-22 | 120 |
| agent-governance-toolkit | framework | 2026-06-22 | 120 |
| agent-kit | framework | 2026-06-22 | 120 |
| agentic-context-engine | framework | 2026-06-22 | 120 |
| agentrecall-mcp | MCP server | 2026-06-22 | 120 |
| agentscope | framework | 2026-06-22 | 120 |
| agentsmesh | platform | 2026-06-22 | 120 |
| aichat | harness | 2026-06-22 | 120 |
| aidlc-workflows | framework | 2026-06-22 | 120 |
| aisuite | framework | 2026-06-22 | 120 |
| antigravity-sdk-python | framework | 2026-06-22 | 120 |
| apache-devlake | platform | 2026-06-22 | 120 |
| archon | platform | 2026-06-22 | 120 |
| arrow-js | framework | 2026-06-22 | 120 |
| autoresearchclaw | harness | 2026-06-22 | 120 |
| autosci | harness | 2026-06-22 | 120 |
| awslabs-mcp | MCP server | 2026-06-22 | 120 |
| baml | framework | 2026-06-22 | 120 |
| beta9 | platform | 2026-06-22 | 120 |
| blender-mcp | MCP server | 2026-06-22 | 120 |
| bmad-method | framework | 2026-06-22 | 120 |
| cherry-studio | platform | 2026-06-22 | 120 |
| claude-code-harness | harness | 2026-06-22 | 120 |
| claude-code-staff-engineer | harness | 2026-06-22 | 120 |
| claude-modular | framework | 2026-06-22 | 120 |
| claude-plugins-official | platform | 2026-06-22 | 120 |
| claurst | harness | 2026-06-22 | 120 |
| clawcodex | harness | 2026-06-22 | 120 |
| cloudflare-mcp | MCP server | 2026-06-22 | 120 |
| codebase-memory-mcp | MCP server | 2026-06-22 | 120 |
| confluence | MCP server | 2026-06-22 | 120 |
| context7 | MCP server | 2026-06-22 | 120 |
| continuous-claude-v3 | harness | 2026-06-22 | 120 |
| copilotkit | framework | 2026-06-22 | 120 |
| crewai | framework | 2026-06-22 | 120 |
| cua | harness | 2026-06-22 | 120 |
| cve-mcp-server | MCP server | 2026-06-22 | 120 |
| daytona | platform | 2026-06-22 | 120 |
| debugmcp | MCP server | 2026-06-22 | 120 |
| deepeval | framework | 2026-06-22 | 120 |
| deepseek-reasonix | platform | 2026-06-22 | 120 |
| deer-flow | harness | 2026-06-22 | 120 |
| desktopcommandermcp | MCP server | 2026-06-22 | 120 |
| devfleet | MCP server | 2026-06-22 | 120 |
| dify | platform | 2026-06-22 | 120 |
| eigent | platform | 2026-06-22 | 120 |
| eino | framework | 2026-06-22 | 120 |
| evalview | MCP server | 2026-06-22 | 120 |
| exa-mcp-server | MCP server | 2026-06-22 | 120 |
| fabric | framework | 2026-06-22 | 120 |
| fal-ai-mcp-server | MCP server | 2026-06-22 | 120 |
| fast-agent | framework | 2026-06-22 | 120 |
| fastapi-mcp | framework | 2026-06-22 | 120 |
| fastmcp | framework | 2026-06-22 | 120 |
| figma-context-mcp | MCP server | 2026-06-22 | 120 |
| firecrawl-mcp | MCP server | 2026-06-22 | 120 |
| forgecode | harness | 2026-06-22 | 120 |
| formkit | framework | 2026-06-22 | 120 |
| gemini-cli | platform | 2026-06-22 | 120 |
| genericagent | harness | 2026-06-22 | 120 |
| gentle-ai | harness | 2026-06-22 | 120 |
| gentleman-book-mcp | MCP server | 2026-06-22 | 120 |
| git-mcp | MCP server | 2026-06-22 | 120 |
| github-mcp-server | MCP server | 2026-06-22 | 120 |
| google-workspace-mcp | MCP server | 2026-06-22 | 120 |
| gptme | harness | 2026-06-22 | 120 |
| grok-cli | platform | 2026-06-22 | 120 |
| gsd | framework | 2026-06-22 | 120 |
| gstack | harness | 2026-06-22 | 120 |
| happy | platform | 2026-06-22 | 120 |
| harbor | framework | 2026-06-22 | 120 |
| haystack | framework | 2026-06-22 | 120 |
| helicone | platform | 2026-06-22 | 120 |
| hermes-agent | harness | 2026-06-22 | 120 |
| hive | harness | 2026-06-22 | 120 |
| holyclaude | platform | 2026-06-22 | 120 |
| honcho | platform | 2026-06-22 | 120 |
| humanlayer | harness | 2026-06-22 | 120 |
| ida-pro-mcp | MCP server | 2026-06-22 | 120 |
| jcode | harness | 2026-06-22 | 120 |
| jira | MCP server | 2026-06-22 | 120 |
| kilocode | platform | 2026-06-22 | 120 |
| kimi-code | platform | 2026-06-22 | 120 |
| kodus-ai | platform | 2026-06-22 | 120 |
| langchain | framework | 2026-06-22 | 120 |
| langchainjs | framework | 2026-06-22 | 120 |
| langgraph | framework | 2026-06-22 | 120 |
| langgraphjs | framework | 2026-06-22 | 120 |
| lazycodex | harness | 2026-06-22 | 120 |
| letta-code | harness | 2026-06-22 | 120 |
| letta | platform | 2026-06-22 | 120 |
| lobehub | platform | 2026-06-22 | 120 |
| logfire | platform | 2026-06-22 | 120 |
| longhand | MCP server | 2026-06-22 | 120 |
| mastra | framework | 2026-06-22 | 120 |
| mcp-context-forge | MCP server | 2026-06-22 | 120 |
| mcp-toolbox | MCP server | 2026-06-22 | 120 |
| mcp-use | framework | 2026-06-22 | 120 |
| memind | platform | 2026-06-22 | 120 |
| memori | platform | 2026-06-22 | 120 |
| memu | platform | 2026-06-22 | 120 |
| microsoft-agent-framework | framework | 2026-06-22 | 120 |
| mimo-code | platform | 2026-06-22 | 120 |
| minecontext | platform | 2026-06-22 | 120 |
| nanobot | harness | 2026-06-22 | 120 |
| nanoclaw | platform | 2026-06-22 | 120 |
| nimbalyst | platform | 2026-06-22 | 120 |
| oh-my-claudecode | harness | 2026-06-22 | 120 |
| oh-my-openagent | harness | 2026-06-22 | 120 |
| oh-my-pi | platform | 2026-06-22 | 120 |
| omnigent | framework | 2026-06-22 | 120 |
| open-design | platform | 2026-06-22 | 120 |
| open-interpreter | harness | 2026-06-22 | 120 |
| open-multi-agent | framework | 2026-06-22 | 120 |
| opendocswork-mcp | MCP server | 2026-06-22 | 120 |
| openrewrite | framework | 2026-06-22 | 120 |
| opensquilla | platform | 2026-06-22 | 120 |
| openviking | platform | 2026-06-22 | 120 |
| osaurus | harness | 2026-06-22 | 120 |
| pare | MCP server | 2026-06-22 | 120 |
| pentest-ai | MCP server | 2026-06-22 | 120 |
| pezzo | platform | 2026-06-22 | 120 |
| pg-aiguide | MCP server | 2026-06-22 | 120 |
| phantom | platform | 2026-06-22 | 120 |
| phoenix | platform | 2026-06-22 | 120 |
| plandex | platform | 2026-06-22 | 120 |
| playwright-mcp | MCP server | 2026-06-22 | 120 |
| plumb-mcp | MCP server | 2026-06-22 | 120 |
| prisma-mcp | MCP server | 2026-06-22 | 120 |
| pydantic-ai | framework | 2026-06-22 | 120 |
| pydantic-deepagents | framework | 2026-06-22 | 120 |
| qwen-code | platform | 2026-06-22 | 120 |
| ragflow | platform | 2026-06-22 | 120 |
| ref-tools-mcp | MCP server | 2026-06-22 | 120 |
| refly | platform | 2026-06-22 | 120 |
| reversa | framework | 2026-06-22 | 120 |
| ruflo | harness | 2026-06-22 | 120 |
| scenario | framework | 2026-06-22 | 120 |
| sentry-mcp | MCP server | 2026-06-22 | 120 |
| sequential-thinking | MCP server | 2026-06-22 | 120 |
| serena | MCP server | 2026-06-22 | 120 |
| server-filesystem | MCP server | 2026-06-22 | 120 |
| server-github | MCP server | 2026-06-22 | 120 |
| server-memory | MCP server | 2026-06-22 | 120 |
| sim | platform | 2026-06-22 | 120 |
| skillopt | framework | 2026-06-22 | 120 |
| sourcebot | platform | 2026-06-22 | 120 |
| squish-memory | MCP server | 2026-06-22 | 120 |
| strands-agents | framework | 2026-06-22 | 120 |
| supabase-mcp | MCP server | 2026-06-22 | 120 |
| tabby | platform | 2026-06-22 | 120 |
| textgrad | framework | 2026-06-22 | 120 |
| trace-mcp | MCP server | 2026-06-22 | 120 |
| trigger-dev | platform | 2026-06-22 | 120 |
| txtai | framework | 2026-06-22 | 120 |
| ui-tars-desktop | harness | 2026-06-22 | 120 |
| vercel-ai | framework | 2026-06-22 | 120 |
| vercel-sandbox | platform | 2026-06-22 | 120 |
| vibecode-pro-max-kit | harness | 2026-06-22 | 120 |
| voltagent | framework | 2026-06-22 | 120 |
| zeroshot | harness | 2026-06-22 | 120 |

_0 eval(s) carry no `**Last verified:**` date (field presence is gated separately by `backfill-lastverified.py`)._
<!-- WATCHLIST:STALE:END -->

## 4. Unverified claims & measurement backlog (18)

**Unverified token-savings claims (16).** CATALOG rows with a numeric token-savings headline whose eval is not run-backed (`MEASURED`/`RUN`). Run the token-savings protocol to verify, or add an in-row disclaimer.

| Tool | Evidence | Disclaimer in row? |
|------|----------|--------------------|
| ACE (agentic-context-engine) | SOURCE-ONLY | no |
| buried-injections | SOURCE-ONLY | no |
| claude-code-memory-setup | REVIEW | yes |
| claw-compactor | REVIEW | no |
| cocoindex-code | REVIEW | no |
| code-context-engine | REVIEW | no |
| context-mode | REVIEW | no |
| GenericAgent | REVIEW | no |
| gortex | REVIEW | no |
| h5i | SOURCE-ONLY | no |
| LeanKG | SOURCE-ONLY | yes |
| OmniRoute | SOURCE-ONLY | yes |
| rtk | REVIEW | no |
| semble | REVIEW | no |
| SocratiCode | REVIEW | no |
| token-optimizer-mcp | REVIEW | no |

**ADOPT skills lacking measured backing (2).** ADOPT-verdict skill evals not yet graduated to a measured run (#38): agent-skills-addyosmani, cc-skills-golang.

<!-- WATCHLIST:END -->
