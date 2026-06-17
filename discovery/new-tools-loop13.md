# Loop 13 — Tool Evaluations (2026-06-17)

Discovery channels: GitHub search (claude code, ai coding agent), skills.sh registry, web search (AI dev tools 2026, flaky test detection, code quality).

## New Entries Added (19 total)

### Agent Orchestration (4 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| cc-switch | 103K | ADD | Desktop GUI wrapping 6+ CLI agents — unique niche vs terminal-only tools |
| qwen-code | 25K | ADD | Alibaba-backed open-source terminal agent; represents Qwen ecosystem |
| DeepSeek-Reasonix | 23K | ADD | Prefix-cache-optimized agent; unique long-session approach |
| oh-my-pi | 13K | ADD | Feature-complete agent with LSP/DAP, hash-anchored edits, 40+ providers |

### Code Understanding (1 entry)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| opensrc | 2.5K | ADD | Fetches npm source for agent context; complements context7 (docs vs source) |

### Memory & Context (1 entry)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| engram | 4.4K | ADD | Agent-agnostic Go binary; portable single-binary memory for any editor |

### Skills & Plugins (3 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| scientific-agent-skills | 28K | ADD | 140 scientific skills + 100 DB connectors; deep domain depth |
| openskills | 10K | ADD | Universal SKILL.md installer across all AI editors |
| agents (wshobson) | 37K | ADD | 84 plugins, 192 agents across 6 editors; largest marketplace |

### Code Review & Quality (1 entry)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| PR-Agent | 12K | ADD | Open-source AI PR reviewer (ex-Qodo); now Apache-2.0 community-maintained |

### Dev Workflow (2 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| claude-code-router | 35K | ADD | Claude Code as infrastructure layer with custom routing |
| aidlc-workflows | 3K | ADD | AWS adaptive lifecycle rules; cross-editor, methodology-first |

### Observability (2 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| Infracost | 12K | ADD | Cloud infra cost estimates; fills gap in Cost Efficiency signal |
| abtop | 3K | ADD | htop-style multi-session agent monitor; unique cross-session visibility |

### MCP Servers (5 entries)
| Tool | Stars | Verdict | Rationale |
|------|-------|---------|-----------|
| fastmcp | 26K | ADD | Framework for building MCP servers quickly; no overlap |
| git-mcp | 8K | ADD | Anti-hallucination MCP; live repo context vs context7's library docs |
| awslabs/mcp | 9K | ADD | Official AWS MCP servers for S3, Lambda, DynamoDB, CDK |
| Figma-Context-MCP | 15K | ADD | Bridge Figma designs to code via MCP |
| mcp-toolbox | 16K | ADD | Google's database MCP server; complements prisma/supabase |

## Ecosystem Observations

- **Multi-editor convergence**: cc-switch (103K), openskills (10K), aidlc-workflows (3K) all target 6+ editors. The market is moving toward editor-agnostic tooling.
- **Open-source coding agents proliferating**: qwen-code, DeepSeek-Reasonix, oh-my-pi join opencode, goose, OpenHands. Every major AI lab now has a terminal agent.
- **MCP ecosystem maturing rapidly**: fastmcp (26K stars), awslabs/mcp, googleapis/mcp-toolbox show infrastructure providers investing heavily in MCP.
- **PR-Agent going community**: Qodo transferred PR-Agent back to Apache-2.0 with community governance — significant for open-source AI code review.
- **Cost visibility gap**: Infracost fills the "what does AI-generated infra cost?" gap, complementing tokencost's "what does the AI itself cost?" coverage.

## Catalog count: 183 -> ~202 entries (19 added)
