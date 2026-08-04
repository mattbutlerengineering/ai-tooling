# Evaluation: Nimbalyst (formerly Crystal)

**Repo:** [Nimbalyst/nimbalyst](https://github.com/Nimbalyst/nimbalyst)
**Stars:** 876 (successor) | **Last updated:** 2026-06-19 (pushed; created 2025-10-30) | **License:** MIT
**Last verified:** 2026-06-22  <!-- backfilled from last git edit; not a hands-on re-check -->
**Last triaged:** 2026-08-04  <!-- triaged: bulk -->
**Dev loop stage:** Implement (a visual session-manager/workspace wrapping coding agents; touches Plan via tasks and Review via WYSIWYG diff approval)
**Layer:** Tooling (cross-platform Electron desktop app + mobile companion)

---

## What it does

Nimbalyst is a **free, local visual workspace and parallel-session manager for coding agents** — Codex and Claude Code (Opencode and Copilot in alpha). It is the active successor to **Crystal** ([stravu/crystal](https://github.com/stravu/crystal)), which was deprecated in February 2026 and now just redirects here. Instead of driving agents in a bare terminal, you collaborate visually: agents stream edits into open editors and you approve their changes as **red/green WYSIWYG diffs**, then edit or annotate. It bundles editors for Markdown, code (Monaco), CSV (RevoGrid), Mermaid, Excalidraw, mockups, and data models.

For developers the session layer is the core: run **multiple agent sessions in parallel**, organize them on a **Kanban board**, link sessions↔files, search/resume sessions, and use built-in **git worktrees**, AI commits, workstreams, and a terminal — plus task tracking the agent can read and edit, and a **mobile app** to manage sessions on the go. It's extension-first (build your own editors) and local-first (Markdown/JSON/CSV).

## How we tested it

**Evidence:** REVIEW

**Source-grounded inspection — not installed, not run.** No desktop app installed, no session run. Claims come from the repository (GitHub metadata, README, release count) for both the successor (Nimbalyst/nimbalyst) and the deprecated original (stravu/crystal), not observed behavior. The feature list is the project's own README.

```bash
gh api repos/stravu/crystal --jq '.archived, .pushed_at'          # deprecated Feb 2026 -> Nimbalyst
gh api repos/Nimbalyst/nimbalyst --jq '{stars:.stargazers_count,created:.created_at,license:.license.spdx_id}'
gh api repos/Nimbalyst/nimbalyst/readme --jq '.content' | base64 -d
gh api repos/Nimbalyst/nimbalyst/releases --jq 'length'           # 30
```

## What worked

- **Visual diff-approval is a real Review aid.** Red/green WYSIWYG approval of an agent's changes (with inline edit/annotate) is a more legible review surface than reading raw terminal diffs — a genuine human-in-the-loop checkpoint.
- **Parallel-session management with git worktrees.** Kanban + worktree isolation + session↔file linking is exactly the coordination layer multi-session agent work needs; directly comparable to claude-squad but GUI-rich.
- **Multi-agent, cross-platform, local-first.** Works across Codex/Claude Code (+ alpha Opencode/Copilot), macOS/Windows/Linux, with open local file formats — not locked to one vendor or cloud.
- **Active and iterating.** 30 releases, public roadmap, issue templates, discussions; the Crystal→Nimbalyst migration shows continuity rather than abandonment.
- **Mobile companion** for starting/responding to sessions away from the desk is a genuinely uncommon capability.

## What didn't work or surprised us

- **Young under the new name.** 876★ on the successor (vs. ~3k on the deprecated Crystal) and created late 2025 — the rename resets social proof, and stability/longevity are less proven than CLI incumbents.
- **Heavy surface.** A full Electron workspace with seven editor types is a lot of app to adopt for what many users get from a TUI (claude-squad) or their existing IDE — discovery and resource cost are real.
- **GUI desktop, not scriptable infra.** Unlike the CLI session managers, it's a desktop application; not something you wire into CI or headless automation.
- **Overlaps your editor.** If you already run an in-editor agent (kilocode/Cursor) or an IDE you like, a separate visual workspace competes with that habit rather than slotting in.

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | WYSIWYG red/green approval + annotate makes it easier to catch bad agent edits before they land. |
| Speed | + / neutral | Parallel sessions, kanban, and worktrees speed multi-track agent work; offset by the overhead of adopting a full desktop workspace. |
| Maintainability | neutral | Affects workflow/review surface, not codebase structure. |
| Safety | neutral | Local-first; standard agent file/edit trust model with human approval gates. |
| Cost Efficiency | neutral | Free and local; spends your own provider tokens. |

## Verdict

**SKIP** — redundant with [`claude-squad`](https://github.com/smtg-ai/claude-squad) (STACK, `RUN`). The evaluation says so in its own hold-off clause: *"Hold off if
you're happy in a TUI (claude-squad) — the full Electron workspace is a heavy switch."* Alternatives
you pick between are the definition of the redundancy this band eliminates.

The job is identical — run several Codex/Claude Code sessions in parallel over git worktrees and
approve the diffs — and the difference is the surface: an Electron desktop workspace instead of a
TUI. The WYSIWYG red/green approval and kanban are genuinely nicer, and they are also the cost: a
standalone Electron app is a heavier dependency than a terminal program, and the evaluation notes
the successor (formerly Crystal) is still young.

★1.1K against the incumbent's ★8.1K is the tiebreak. A GUI variant with an eighth of the adoption
is not a replacement candidate.

Re-open if visual diff approval turns out to be the thing that makes parallel sessions reviewable —
that is a measurable claim (review throughput with and without), and it would be P0 work.

_Triaged 2026-08-04 by the P2 challenger band ([#262](https://github.com/mattbutlerengineering/ai-tooling/issues/262))._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [Nimbalyst](https://github.com/Nimbalyst/nimbalyst) | platform | Local visual workspace + parallel-session manager for Codex/Claude Code — WYSIWYG red/green diff approval, kanban, git worktrees, task tracking, mobile app (formerly Crystal) | Running several coding-agent sessions and reviewing their edits is hard in a bare terminal; want a visual command center with human approval gates | claude-squad (lean TUI session manager), kilocode (in-editor agent), opencode |
