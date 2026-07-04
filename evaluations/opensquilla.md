# Evaluation: OpenSquilla

**Repo:** [opensquilla/opensquilla](https://github.com/opensquilla/opensquilla)
**Stars:** 4,398 | **Last updated:** 2026-06-18 | **License:** Apache-2.0
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Dev loop stage:** Plan + Implement + Verify (a full standalone agent runtime — it *is* the inner loop, not a stage within Claude Code's)
**Layer:** Tooling (an alternative agent harness/platform, not a Claude Code add-on)

---

## What it does

Catalog one-liner: "Token-efficient AI agent — same budget, higher intelligence density." Ground truth: **OpenSquilla is a complete, standalone, self-hostable AI agent platform written in Python (3.12+) — not a Claude Code plugin, skill, or token-efficiency layer you bolt onto an existing harness.** It is a "microkernel AI agent for your CLI, Web UI, and chat channels": you install it (`uv tool install opensquilla[recommended]`), run `opensquilla onboard` then `opensquilla gateway run`, and it stands up its own gateway/control console on `127.0.0.1:18791` with a Web UI, a CLI, and connectors for Slack, Discord, Telegram, Feishu, DingTalk, QQ, WeCom, and Matrix. Every entry point runs through one shared turn loop, so tool dispatch, retries, and decision logging behave identically across surfaces.

Its pluggable provider layer speaks to OpenRouter, OpenAI, Anthropic, Ollama, DeepSeek, Gemini, Qwen/DashScope, and 20+ other LLM providers. Anthropic is *one provider among many*; the project is provider-agnostic and explicitly anti-lock-in. The "token-efficient" claim rests on two documented mechanisms: **SquillaRouter** — an on-device model router (bundled ONNX runtime + LightGBM classifier) that sends each turn to the cheapest model tier that can handle it, reserving strong models for hard reasoning/recovery; and **tool compression** — model-visible tool outputs are shortened to a compact preview with a `tool_result_handle` for out-of-band retrieval of the full result, while the raw result is preserved. It also ships persistent memory, a layered sandbox, built-in web search, on-device embeddings, "meta-skills," and scheduling.

Relevant to this catalog: OpenSquilla can run as a **stdio MCP server bridge** (`opensquilla mcp-server run`, with the `mcp` extra) so another MCP-capable client could call into OpenSquilla session workflows. This is the only Claude-Code-adjacent surface — and it is OpenSquilla acting as a *backend MCP server you delegate to*, not a tool that improves a Claude Code session. The docs describe it as a separate integration surface bound to the gateway WebSocket.

## How we tested it

**Evidence:** REVIEW

**Method: inspected the repo, README, license, docs tree, and key feature docs via the GitHub API. Did NOT install or run it.** This is a deliberate non-install evaluation, for the same reason as the oh-my-openagent SKIP: OpenSquilla is a *replacement* front-end, not a Claude Code enhancement. Installing it means standing up a separate Python agent platform with its own gateway, Web UI, model router (bundled ONNX/LightGBM/Git-LFS model assets), and provider keys — it would not run inside, or extend, the Claude Code dev loop this catalog standardizes on. The verdict therefore rests on the repo, license, documented mechanics, and maturity signals. No metrics are invented; star/fork/release/contributor counts are from live API calls, and the cost/score figures in the README leaderboard are quoted as the project's own claims.

```bash
gh api repos/opensquilla/opensquilla --jq '{stars:.stargazers_count,license:.license.spdx_id,description,created_at,pushed_at,language,forks:.forks_count,open_issues:.open_issues_count}'
# 4,398 stars; Apache-2.0; Python; created 2026-05-06; pushed 2026-06-18; 339 forks; 107 open issues
gh api repos/opensquilla/opensquilla/readme --jq '.content' | base64 -d              # full README
gh api "repos/opensquilla/opensquilla/git/trees/HEAD?recursive=1" --jq '.tree[].path' # src/, docs/, channels, gateway, squilla_router
gh api repos/opensquilla/opensquilla/contents/docs/mcp-server.md --jq '.content' | base64 -d        # MCP *server* bridge
gh api repos/opensquilla/opensquilla/contents/docs/features/squilla-router.md --jq '.content' | base64 -d
gh api repos/opensquilla/opensquilla/contents/docs/features/tool-compression.md --jq '.content' | base64 -d
gh api repos/opensquilla/opensquilla/releases --paginate --jq '.[].tag_name' | wc -l    # 6
gh api repos/opensquilla/opensquilla/contributors --paginate --jq '.[].login' | wc -l   # 6
```

Reviewed: README (install paths, provider list, leaderboard), the docs index and feature docs (squilla-router, tool-compression, mcp-server, memory, skills, meta-skills, channels, gateway), the recursive file tree, and the maturity signals above.

## What worked

- **It is a genuinely complete, multi-surface agent platform.** One shared turn loop across CLI / Web UI / chat channels, a control console, persistent memory, layered sandbox, scheduling, on-device embeddings, and 20+ provider integrations. As a *self-hosted agent product* (e.g. a Slack/Discord bot backed by routed models) it is coherent and well-documented.
- **The token-efficiency mechanisms are real and specific.** SquillaRouter does on-device tier classification so routine turns avoid premium models, and tool compression shortens model-visible tool output while preserving the raw result behind a `tool_result_handle`. These are concrete cost/context mechanisms, not just a slogan — directionally the same ideas as headroom (reversible tool-output compression) and rtk (command-output rewriting), but implemented inside OpenSquilla's own runtime.
- **Provider-agnostic, anti-lock-in, Apache-2.0.** Unlike oh-my-openagent's non-commercial SUL-1.0 license, OpenSquilla is permissively licensed and explicitly avoids single-provider lock-in. Good for commercial self-hosting.
- **Honest, thorough docs.** A real docs tree (configuration, providers, sandbox, approvals/permissions, diagnostics-and-replay, usage-and-cost, troubleshooting), explicit install profiles (`core` vs `recommended`), SECURITY.md, and clear safety notes (keep the gateway bound to `127.0.0.1`).

## What didn't work or surprised us

- **It is NOT a Claude Code tool — this is the central caveat.** OpenSquilla is its own agent harness with its own UI, CLI, and gateway. Adopting it means *running a different agent platform*, not extending the Claude Code dev loop. There is no Claude Code plugin/skill/hook to install. Anthropic is merely one of 20+ providers OpenSquilla can call.
- **Its only Claude-Code-adjacent surface points the wrong way.** The MCP integration is OpenSquilla running *as an MCP server* that another client delegates *to* — i.e. Claude Code would hand work off to a second full agent platform. That is a heavyweight, redundant arrangement (agent-calling-agent), not a context/quality enhancement for the Claude Code session, and it requires standing up and securing the whole OpenSquilla gateway.
- **Young and thin on maturity signals.** Created 2026-05-06 (~6 weeks old at evaluation), 4.4k stars, only 6 releases, ~6 contributors, 107 open issues, current release 0.3.1 with unsigned Windows preview builds. Far less battle-tested than oh-my-openagent (62.8k stars) or headroom (37.3k). Real concentration/abandonment risk for something on the agent's critical path.
- **Heavy install for the token-efficiency win.** The `recommended` profile pulls ONNX Runtime, LightGBM, NumPy, tokenizers, and Git-LFS-tracked router model assets; Windows needs the VC++ runtime for the bundled ONNX. That is a lot of footprint to obtain routing/compression you would only get *inside OpenSquilla*, not in your existing harness.
- **The headline cost/score numbers are self-reported.** The README leaderboard (e.g. an "OpenClaw / Claude Opus 4.7" row with score/cost figures) is the project's own benchmark, not independently reproduced here.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | neutral (and not for *this* loop) | Tier routing + tool compression target cost/context, not correctness; any benefit accrues inside OpenSquilla's runtime, not a Claude Code session, and leaderboard scores are self-reported |
| Speed | +/- | Routing cheap turns to small models and compressing tool output can speed OpenSquilla's own loop; irrelevant to a Claude Code workflow, and standing up a second agent platform adds latency/overhead |
| Maintainability | - (for this loop) | Adopting it means running a separate Python gateway/Web-UI platform rather than integrating into the Claude Code dev loop; young project, 6 releases, ~6 contributors |
| Safety | +/- | Layered sandbox, approvals/permissions, local-bound gateway, on-device routing (no external classifier) are positives; offset by an unsigned-preview, internet-facing-capable gateway and immature codebase on the critical path |
| Cost Efficiency | + (within OpenSquilla) | The core pitch: on-device tier routing to cheap models + reversible tool-output compression cut token spend — but only for workloads run *through OpenSquilla*, not Claude Code |

## Verdict

**SKIP** (for *this* catalog's Claude Code dev loop) — but note the ideas, and re-evaluate if your stack is OpenSquilla itself.

OpenSquilla is a legitimate, permissively licensed (Apache-2.0), provider-agnostic standalone agent platform with real token-efficiency engineering (SquillaRouter on-device tier routing, reversible tool-output compression). But for a catalog standardized on Claude Code it is a SKIP as an installable artifact, for exactly the oh-my-openagent reason: **it is an alternative agent harness you switch *to*, not a tool you add to Claude Code.** Its sole Claude-Code-adjacent surface — an MCP *server bridge* — points the wrong way (Claude Code delegating to a second full agent platform), which is redundant rather than additive. Maturity is also thin (~6 weeks old, 6 releases, ~6 contributors, 4.4k stars) for something that would sit on the critical path.

**Differentiation:** vs. `oh-my-openagent` (SKIP) — both are alternative harnesses you switch to rather than add; OpenSquilla is its *own* Python platform (CLI/Web/channels/gateway) whereas oh-my-openagent wraps OpenCode/Codex, but the SKIP logic is identical, and OpenSquilla's Apache-2.0 license is friendlier than oh-my-openagent's SUL-1.0. vs. `headroom` (CONDITIONAL) — headroom is the right shape for this catalog: a provider-agnostic compression *layer* (proxy / `headroom wrap claude` / MCP) that wraps your existing Claude Code agent and cuts tokens without replacing the harness; OpenSquilla's tool compression is the same idea trapped inside its own runtime. vs. `caveman` / `rtk` — lightweight, fail-open context-reduction tools that live inside the Claude Code loop; OpenSquilla replaces the loop entirely.

Re-evaluate to CONDITIONAL only if (a) the user's stack is OpenSquilla itself (self-hosted multi-channel agent) rather than Claude Code — in which case it stands on its own terms — or (b) a real Claude Code integration ships that *adds* OpenSquilla's routing/compression into a Claude Code session rather than delegating to a separate agent.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [OpenSquilla](https://github.com/opensquilla/opensquilla) | platform | Standalone token-efficient agent platform (CLI/Web/chat) with on-device model routing; not a Claude Code plugin | Want a self-hosted, provider-agnostic agent with cheap-tier model routing across many channels | oh-my-openagent, headroom, caveman, rtk |
