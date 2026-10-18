# Evaluation: claude-show-your-work

**Repo:** [iamumeransari/claude-show-your-work](https://github.com/iamumeransari/claude-show-your-work)
**Stars:** 236 | **Last updated:** 2026-10-18 (pushed) | **License:** MIT
**Last verified:** 2026-10-18
**Last triaged:** 2026-10-18  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

A Claude Code plugin rendering screenshots and playing Playwright recordings inline in the
terminal (Ghostty/kitty graphics protocol), with synced before/after visual QA comparisons —
avoiding a context switch out of the terminal to view visual test output.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: the CATALOG
one-liner and GitHub repo metadata (stars, license, activity). No hands-on run was performed.

## Verdict

**discovery-log — tentative read** — not previously examined.

## Triage note

P3 backlog, oldest-untriaged (no prior eval file). Not a P2 challenger: its cited peers
(`claude-skill-playwright-browser`, `dev3000`, `agent-vision-toolkit`) are themselves
`discovery-log` leads, not a STACK pick it's redundant with — the inline-terminal-rendering
angle (vs. a separate browser/viewer) is a real differentiator. Left at `discovery-log`;
stamped.

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with | Ships inside |
|------|------|-----------|-------------------|---------------|--------------|
| [claude-show-your-work](https://github.com/iamumeransari/claude-show-your-work) | plugin | Claude Code plugin (MIT) rendering screenshots and playing Playwright recordings inline in the terminal, with synced before/after QA comparisons (Ghostty/kitty) | Visual QA output (screenshots, test recordings) is invisible inside a terminal session, forcing a context switch to view it | claude-skill-playwright-browser, dev3000, agent-vision-toolkit |  |
