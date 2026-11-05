# Evaluation: claude-resocket-plugin

**Repo:** [UponNuclearastro/claude-resocket-plugin](https://github.com/UponNuclearastro/claude-resocket-plugin)
**Stars:** 40 | **Last updated:** 2026-11-05 (pushed) | **License:** none (no LICENSE file)
**Last verified:** 2026-11-05
**Last triaged:** 2026-11-05  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A Claude Code plugin ("Uiprobe") running a check against a Figma design — it compares
the built page to the Figma frame value-by-value and has Claude fix the differences.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo
metadata (no `LICENSE` file; GitHub API reports `license: null`) plus the CATALOG
one-liner. That is sufficient for the verdict below, because the verdict turns on
licensing, not on the tool's behaviour — a question metadata answers directly. It would
not be sufficient to support an ADOPT, and this eval offers none.

## Verdict

**SKIP** — no declared license. A plugin is *vendored* — its text is copied into the
consuming repo — and text carrying no license grant cannot be copied in.

_Triaged 2026-11-05 by the P4 mechanical-skip band. Zero judgement: the missing license
on a vendored artifact is the reason, not a quality assessment._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [claude-resocket-plugin](https://github.com/UponNuclearastro/claude-resocket-plugin) | plugin | Uiprobe plugin for Claude Code (⚠️ no declared license) checking a built page against its Figma frame value-by-value, then fixing the gaps | Confirming a built page actually matches its Figma frame means eyeballing it rather than a mechanical value-by-value diff | figma-maxxing, ai-design-check, ilse |
