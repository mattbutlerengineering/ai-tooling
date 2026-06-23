# Evaluation: andrej-karpathy-skills

**Repo:** [multica-ai/andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills)
**Stars:** 178,312 | **Last updated:** 2026-06-18 | **License:** MIT
**Dev loop stage:** Implement
**Layer:** Process

---

## What it does

A single CLAUDE.md file (also packaged as a skill) encoding four behavioral principles derived from Andrej Karpathy's public observations on LLM coding pitfalls: Think Before Coding, Simplicity First, Surgical Changes, and Goal-Driven Execution. The mechanism is pure context injection — loading the file primes the agent to surface assumptions, avoid overengineering, restrict diffs to the requested change, and define verifiable success criteria before implementation.

The repo also ships EXAMPLES.md with concrete before/after code samples for each principle, a Cursor rule file, and a skills.sh-installable SKILL.md. The four principles directly address specific LLM failure modes Karpathy identified: silent assumption-picking, code bloat, orthogonal side-effect edits, and underspecified goals.

## How we tested it

**Evidence:** REVIEW

Read the CLAUDE.md, SKILL.md, and EXAMPLES.md from the repo via GitHub API. Cross-referenced against the user's own `~/.claude/rules/common/implementation-discipline.md`, which is explicitly documented as "Adapted from the karpathy-skills behavioral framework" — confirming that this skill has already been adopted, internalized, and refined with project-specific amendments (e.g., reconciled error handling guidance, explicit refactoring-is-a-separate-mode rule).

```bash
gh api repos/multica-ai/andrej-karpathy-skills/contents/CLAUDE.md --jq '.content' | base64 -d
gh api repos/multica-ai/andrej-karpathy-skills/contents/skills/karpathy-guidelines/SKILL.md --jq '.content' | base64 -d
gh api repos/multica-ai/andrej-karpathy-skills/contents/EXAMPLES.md --jq '.content' | base64 -d
```

## What worked

- **Directly addresses real LLM failure modes** — not generic advice but targeted fixes for specific Karpathy-observed pitfalls (silent assumptions, bloat, orthogonal edits, weak goals)
- **Concise and non-conflicting** — the full CLAUDE.md is ~60 lines with no framework dependencies, no tools to install, no configuration
- **EXAMPLES.md is genuinely useful** — concrete before/after code samples showing what goes wrong and how the principle prevents it, in Python, TypeScript, and SQL
- **Cross-editor** — ships as CLAUDE.md, SKILL.md (skills.sh), and Cursor rule, so it works everywhere
- **Already proven in practice** — the user's own implementation-discipline.md is adapted from this framework, confirming real-world effectiveness

## What didn't work or surprised us

- **Thin content for 178K stars** — the core is ~60 lines of fairly obvious advice ("don't overcomplicate", "ask before assuming"); the star count reflects Karpathy's brand, not the repo's depth
- **No enforcement mechanism** — pure prompt-based guidance with no hooks, no automated checks, no CI integration; the agent can and does ignore these guidelines under pressure
- **No structured skill orchestration** — unlike mattpocock/skills which has progressive disclosure and loads references on demand, this is a monolithic context dump
- **Redundant if you've already internalized the principles** — the user already has a refined version in their rules; installing the skill on top would be pure duplication
- **EXAMPLES.md not included in the skill** — only the SKILL.md is loaded by the skills system; the most useful file (examples) requires manual reading

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | "Think Before Coding" reduces silent assumption errors; "Goal-Driven Execution" produces verifiable implementations |
| Speed | neutral/- | Guidelines explicitly bias toward caution over speed; may slow down trivial tasks |
| Maintainability | + | "Simplicity First" and "Surgical Changes" directly reduce code bloat and unnecessary diffs |
| Safety | neutral | No security-specific guidance |
| Cost Efficiency | neutral | No token optimization; if anything, asking clarifying questions adds round-trips |

## Verdict

**CONDITIONAL**

Use as a starting point when you have no CLAUDE.md behavioral guidelines yet — it's the most popular and most concise behavioral framework available. However, once you've internalized the four principles into your own project-specific rules (as this user already has), the skill becomes redundant. The EXAMPLES.md is worth reading once as a teaching tool even if you don't install the skill. Compare with mattpocock/skills (ADOPT) which provides deeper, more structured guidance across more dimensions, and agents-best-practices (CONDITIONAL) which covers agent design patterns the Karpathy skill doesn't touch.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [andrej-karpathy-skills](https://github.com/multica-ai/andrej-karpathy-skills) | skill | CLAUDE.md based on Karpathy's LLM coding pitfall observations | Want coding guidelines derived from known LLM failure modes | mattpocock/skills, agent-skills |
