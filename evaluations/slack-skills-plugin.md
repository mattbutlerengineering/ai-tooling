# Evaluation: slack-skills-plugin

**Repo:** [slackapi/slack-skills-plugin](https://github.com/slackapi/slack-skills-plugin)
**Stars:** 132 | **Last updated:** 2026-09-10 (pushed) | **License:** MIT
**Last verified:** 2026-09-21
**Last triaged:** 2026-09-21  <!-- triaged: bulk -->
**Dev loop stage:** MCP Servers
**Layer:** Infrastructure

---

## What it does

Official Slack Technologies plugin (MIT) bringing Slack into Claude Code, Cursor, and Codex via a
bundled Slack MCP server plus a set of Slack skills for both users and developers. Published on the
official Claude Code marketplace as `slack@claude-plugins-official`; independently installable from
its own repo, not vendored inside `anthropics/claude-plugins-official`.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow clone
of the repo (README, LICENSE, package manifests) confirming it is real, MIT-licensed, published by
Slack, and matches its stated description.

## Verdict

**discovery-log — tentative read**

## Triage note

P2 challenger by citation only: its Overlaps cell names `github-mcp-server` (STACK `ADOPT`) as a
conceptual peer — both are official-vendor MCP integrations — but the two serve entirely different
external services (Slack vs. GitHub) and are not competing for the same job. This is not a
redundancy case, so not SKIPped. Left at `discovery-log`; a dedicated Slack MCP server row was
previously missing from the catalog despite Slack being referenced as an integration target from
several existing rows (`nanoclaw`, `phantom`, `letta-code`, `Composio`, `mirage`), so this fills a
real gap rather than duplicating one.

_Triaged 2026-09-21 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [slack-skills-plugin](https://github.com/slackapi/slack-skills-plugin) | plugin | Official Slack plugin (MIT) — a Slack MCP server plus developer/user skills for Claude Code, Cursor, and Codex | Agents have no first-party way to read, post, or search Slack without a hand-rolled integration | mcp-atlassian, sentry, github-mcp-server |  |
