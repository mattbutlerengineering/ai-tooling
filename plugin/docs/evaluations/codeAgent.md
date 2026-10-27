# Evaluation: codeAgent

**Repo:** [Harvil1/codeAgent](https://github.com/Harvil1/codeAgent)
**Stars:** ~1,000 (approx., GitHub page display — gh API access to this repo was not available this session) | **Last updated:** 2026-10-14 (pushed) | **License:** MIT
**Last verified:** 2026-10-27
**Last triaged:** 2026-10-27  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A terminal coding agent CLI (Python 3.11+, primarily Chinese-language README/comments,
Windows-first) that reads repositories, plans multi-step changes, edits files, runs
commands/tests, and iterates until a task is done. Adds long-term memory and
self-learning skills distilled from conversation history, sub-agents, a team mode, a
workflow engine, MCP external-tool support, approval prompts for dangerous commands
with optional `bwrap` sandboxing on Linux, context compression, hooks, scheduled
tasks, session checkpoints (`/rewind`), and plan mode. Defaults to DeepSeek but works
with any OpenAI-compatible or Anthropic-protocol endpoint.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata (via the public GitHub web page and a shallow git clone — this
session's GitHub API access does not cover unattached repositories) plus the
README/feature list. That is sufficient to place the lead, not to support an ADOPT,
and none is offered here.

## Triage note

Left at `discovery-log`. Cites `Baize`, `aider`, `command-code`, `pi` in "Overlaps
with" — none of which is a STACK pick, so this doesn't band P2 challenger. It sits in
an already-crowded "multi-provider terminal coding agent CLI" niche (`Baize` is the
closest peer: same DeepSeek-default/OpenAI-compatible-endpoint shape, sub-agents,
context compression, sandboxing), but it adds a workflow engine, scheduled tasks, and
session checkpoints that `Baize`'s one-liner doesn't claim, and no eval of either tool
has exercised them head-to-head. Not vendored (Type `harness`, not `skill`/`plugin`),
so the MIT license imposes nothing even if it were a stricter one. Deserves a real
hands-on look — ideally alongside `Baize` — rather than a mechanical SKIP on name
resemblance to tools that are themselves still unevaluated leads.

_Triaged 2026-10-27 by the P3 backlog band (newly catalogued same day)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [codeAgent](https://github.com/Harvil1/codeAgent) | harness | Terminal coding agent CLI (MIT, ★1K, Python) — reads repos, plans multi-step changes, edits files, runs commands/tests, with sub-agents, team mode, a workflow engine, hooks, scheduled tasks, session checkpoints, and optional sandboxing; DeepSeek default, works with any OpenAI-compatible or Anthropic-protocol endpoint | Want a hackable, multi-provider terminal coding agent with built-in long-term memory and workflow automation, not locked to one vendor | Baize, aider, command-code, pi |
