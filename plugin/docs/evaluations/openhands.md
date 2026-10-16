# Evaluation: OpenHands

**Repo:** [OpenHands/OpenHands](https://github.com/OpenHands/OpenHands)  <!-- was All-Hands-AI/OpenHands at eval time; the org renamed itself, re-checked 2026-08-04 -->
**Stars:** 83,137 (re-checked 2026-08-04) | **Last updated:** 2026-06-19 | **License:** MIT (enterprise/ directory separate)
**Last verified:** 2026-10-16
**Last triaged:** 2026-10-16  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Infrastructure

---

## What it does

Self-hosted developer control center for coding agents and automations. OpenHands Agent Canvas is a web UI that connects to one or more "agent backends" — local, Docker, VM, or cloud — and runs the OpenHands agent, Claude Code, Codex, Gemini, or any ACP-compatible agent. The platform includes an automation server for scheduled/webhook-triggered tasks (GitHub issue decomposition, Slack reports, dependency updates) and a multi-backend architecture that lets you switch between personal and shared agent servers from one frontend.

Originally "OpenDevin" (a Devin clone), it has evolved into an agent orchestration platform. The codebase is splitting: `OpenHands/software-agent-sdk` (agent + agent server) and `OpenHands/agent-canvas` (frontend + automation). The main repo now serves as the migration hub.

## How we tested it

**Evidence:** RUN

**Hands-on** — installed the agent SDK (`OpenHands/software-agent-sdk`, the part of the platform that holds the agent loop and tools) via `python3.12 -m venv v && v/bin/pip install openhands-sdk openhands-tools` (v1.55.1, 2m50s install, pulls litellm 1.105.1) under `/tmp/eval-openhands/`, then drove its default tool set directly on a planted-defect fixture and ran one real agent conversation against the live LLM endpoint.

```
# t3.py: Agent(...).tools_map executed directly, fixture = calc.py (sum_to_n off-by-one) + test_calc.py
tools: ['file_editor', 'finish', 'task_tracker', 'terminal', 'think']
create 0.002s File created successfully at: /tmp/eval-openhands/fx/calc.py
pytest-before 1.763s   FAILED test_calc.py::test_it - assert 6 == 10   (1 failed)
str_replace 0.006s
pytest-after 0.667s    1 passed in 0.01s
bad replace: No replacement was performed, old_str `nonexistent` did not appear verbatim in .../calc.py.
persist: bar          # `export FOO=bar` then `echo $FOO` in a later terminal call

# t1.py: Conversation.run() with a placeholder key
RUN ERR: ConversationRunError ... litellm.AuthenticationError: AnthropicException - invalid x-api-key
status: ConversationExecutionStatus.ERROR elapsed 2.5s   files: []
```

## Test design

- **Task/corpus:** one fixture, `calc.py` with `sum(range(n))` where `range(n + 1)` is required, plus a one-assert pytest; exercises create, run-tests, edit, re-run-tests, a failing edit and shell-state persistence.
- **Baseline:** none. Only the tool layer ran, so there is no with/without-tool arm and nothing here measures agent quality.
- **Metric:** pass/fail of the fixture test before and after the edit (1 failed to 1 passed), per-call wall-clock, error-message content.
- **Reproduce:** venv as above with Python 3.12 (the SDK requires >=3.12), `pip install pytest`, then build `Agent(llm=LLM(model=..., api_key=...), tools=get_default_tools(enable_browser=False))`, `Conversation(agent, workspace=...)`, call `agent._initialize(conv.state)` and invoke `agent.tools_map[name](Action(...), conv)`.

## What worked

- **Multi-backend architecture** is genuinely novel: one UI connects to local, Docker, VM, or cloud agent servers. You can run personal agents on your laptop and shared review agents on a team server, switching between them from the same frontend.
- **ACP (Agent-Client Protocol)** support means it's not locked to one agent — Claude Code, Codex, Gemini, and custom agents all work through the same interface.
- **Automation server** with scheduled/webhook triggers fills a gap that pure CLI agents like Claude Code don't cover — e.g., daily dependency update agents, GitHub issue decomposition on creation.
- **Active development**: monthly major releases, 77.7K stars, MIT license, Linux Foundation backing through the OpenHands org.

## What didn't work or surprised us

- **The agent loop was not exercised.** No model credentials exist in the test sandbox, so `Conversation.run()` stopped at the provider's `invalid x-api-key` error after 2.5s; whether OpenHands solves tasks better or worse than Claude Code is unmeasured here.
- **The platform layer was not exercised.** Docker is installed but its daemon is absent, so the Docker sandbox, the agent server, Agent Canvas and the automation server (the features the verdict leans on) were not started.
- **Python >=3.12 required**: the sandbox default 3.11 gets `No matching distribution found for openhands-sdk`; a heavy dependency tree (litellm et al.) took 2m50s to install.
- **Tool use needs private API**: calling tools without an LLM meant invoking `agent._initialize(...)` and `tools_map`, which are internals; the supported path is through the conversation loop.
- **Codebase in transition**: splitting across 3 repos (main, software-agent-sdk, agent-canvas) means the developer experience is fragmented. `agent-canvas` has only 86 stars — community hasn't followed the migration yet.
- **Full platform replacement**: this replaces your agent environment, not augments it. You can't use OpenHands features from within a Claude Code session. It's an either/or platform choice.
- **No built-in methodology**: unlike Claude Code + superpowers (TDD enforcement, verification gates, systematic debugging), OpenHands provides the runtime but not the engineering process. You'd need to build that yourself through skills or AGENTS.md.
- **Heavy infrastructure**: Docker sandbox mode requires Docker Desktop, project path mounting, and port management. The no-sandbox mode gives agents full filesystem access with a warning banner.
- **Enterprise license split**: the `enterprise/` directory has a separate non-MIT license, which means some features are commercially restricted despite the MIT branding.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral | Agent quality depends on the underlying model, not the platform |
| Speed | + | Multi-backend lets you run agents on faster hardware; automations run unattended |
| Maintainability | neutral | No methodology built in; you bring your own engineering process |
| Safety | +/- | Docker sandbox adds isolation; no-sandbox mode is dangerously permissive; no built-in guardrails like agentlint |
| Cost Efficiency | + | Self-hosted means no per-seat SaaS fees; but infrastructure costs replace them |
| Verifiability | neutral | The file editor returns explicit errors (`old_str ... did not appear verbatim`) and terminal output is returned verbatim, so tool steps are checkable; whole-agent output was not run |

## Verdict

**discovery-log — tentative read** — the SDK installs and its terminal and file-editor tools behave correctly on a planted-defect fixture (1 failed to 1 passed), but the agent loop and the platform features this entry is about need a model key and a Docker daemon, so there is no real read yet.

Use OpenHands when you need a self-hosted agent orchestration platform with multi-backend support, automation triggers (scheduled/webhook), or ACP-compatible multi-agent management — especially for team environments where agents need to run on shared infrastructure. Choose Claude Code directly when you want the deepest ecosystem (skills, plugins, marketplace, hooks), structured methodology (superpowers, agent-skills), and the simplest setup (single CLI, no Docker required). Like goose and opencode, this is a platform choice, not a complement. Skills (SKILL.md format) are portable between platforms.

## Triage note

Cites claude-squad (STACK ADOPT) in Overlaps with, but the eval's own verdict already draws the line: this is a platform choice (self-hosted, multi-backend agent control center) versus claude-squad's parallel-session TUI, not a redundant re-implementation. ★83.1K, MIT, actively pushed. Left for a real hands-on eval rather than a mechanical SKIP.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenHands](https://github.com/OpenHands/OpenHands) | platform | Self-hosted agent control center — multi-backend, multi-agent, automations (77.7K stars) | Want a full AI dev platform with scheduled automations and team agent servers | claude-squad, goose, opencode |
