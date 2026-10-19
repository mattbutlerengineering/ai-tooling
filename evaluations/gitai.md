# Evaluation: gitai

**Repo:** [feder-cr/git-ai](https://github.com/feder-cr/git-ai)
**Stars:** 1,197 | **Last updated:** 2026-10-17 (pushed) | **License:** MIT
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Ship
**Layer:** Infrastructure

---

## What it does

An open-source, server-centric reimplementation of Git aimed at coding agents rather than
humans, modeled on Anthropic's internally-described (but not public) "Scion" design. Clients
stay online and fetch only what they need; history questions are answered and cached
server-side; changes land through a compare-and-swap instead of a client-side merge queue;
every update is an entry in a changeset log; and repository state lives in a database plus
object storage so the server scales out. Built on GitLab's Gitaly codebase (MIT), vendor-neutral
— the server never calls an LLM itself.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: a shallow
clone's README, LICENSE, and repo layout. That confirms the license (plain MIT; no `ee/`
directory present in this checkout) and the shape of the claim, not whether compare-and-swap
landing actually holds up under real concurrent-agent load.

## Verdict

**discovery-log — tentative read** — newly catalogued this pass; not previously examined.

## Triage note

New lead, added today. Not a P2 challenger: `worktrunk` and `rune` solve *client-side* git
isolation (worktrees, terminal workspace) for one or a few agents per machine, while gitai's
claim is a *server-side* redesign for hundreds of agents landing on one branch concurrently —
a different problem at a different scale, with no existing STACK pick covering it. Left at
`discovery-log`; a real eval would need a concurrent-write benchmark against plain Git to check
whether the compare-and-swap claim holds.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [gitai](https://github.com/feder-cr/git-ai) | tool | Open-source, server-centric Git reimplementation (MIT) letting hundreds of AI agents land changes on one branch concurrently via compare-and-swap | Client-side Git (full clones, merge queues, history walks) bottlenecks when many short-lived agent tasks all want to land on the same branch in seconds | worktrunk, rune, GSD |  |
