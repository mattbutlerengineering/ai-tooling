# Evaluation: Claude-Red (SnailSploit)

**Repo:** [SnailSploit/Claude-Red](https://github.com/SnailSploit/Claude-Red)
**Stars:** 9,300 | **Last updated:** n/a (not checked via API; this session's GitHub access is repo-scoped) | **License:** MIT
**Last verified:** 2026-10-26
**Last triaged:** 2026-10-26  <!-- triaged: bulk -->
**Dev loop stage:** Review
**Layer:** Tooling

---

## What it does

A curated library of ~78 `SKILL.md` offensive-security skills across 23 categories for
the Claude skills system — SQL injection, Active Directory attacks, wireless testing,
EDR evasion, and more. Claude loads the matching skill when a conversation names that
topic. The README states the intended uses as authorized red-team engagements, bug
bounty triage, security research, CTF preparation, and operator training.

**Not to be confused with** the unrelated, now-defunct `0xwilliamortiz/claude-red`
(already catalogued as `claude-red`, SKIPped as gone — repo and author account 404 as
of 2026-08-15). Same display name, different owner, different repo, different
codebase. The catalog row and this file are disambiguated as "Claude-Red (SnailSploit)"
to avoid the two colliding under the same case-insensitive name.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the
repo's own README (fetched over the web, since this session's GitHub API access is
scoped to this repository and does not extend to arbitrary repos) plus the CATALOG
"Overlaps with" cell. That is sufficient to place the lead against its closest catalog
peers, not to support any verdict, and none is offered here.

## Triage note

No STACK pick appears in its "Overlaps with" cell (`Claude-BugHunter`, `pentest-ai-agents`,
`ctf-skills` are all themselves unevaluated leads), so this lands in P3 backlog —
nothing to call redundant against. The catalog already holds a deep roster of
offensive-security skill packs with overlapping scope; left at `discovery-log` rather
than SKIPped, since differentiating this pack from its closest peers (coverage depth,
curation quality, maintenance) needs an actual hands-on read, not a mechanical call.

_Triaged 2026-10-26 by the daily discovery-and-triage routine (bulk, eliminate-only).
Left, not SKIPped._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Claude-Red (SnailSploit)](https://github.com/SnailSploit/Claude-Red) | skill | Curated offensive-security skill library (MIT, ★9.3K, ~78 skills/23 categories) for authorized red-team engagements, bug-bounty triage, and CTF prep — unrelated to the now-defunct `0xwilliamortiz/claude-red` | Need per-technique offensive-security methodology (AD attacks, SQLi, wireless, EDR evasion) loaded on demand by topic | Claude-BugHunter, pentest-ai-agents, ctf-skills |
