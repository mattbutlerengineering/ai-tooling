# Evaluation: usagetrim

**Repo:** [00200200/usagetrim](https://github.com/00200200/usagetrim)
**Stars:** 33 | **Last updated:** 2026-09-27 (pushed) | **License:** MIT
**Last verified:** 2026-09-27
**Last triaged:** 2026-09-27  <!-- triaged: bulk -->
**Dev loop stage:** Implement
**Layer:** Tooling

---

## What it does

A local CLI + MCP tool that folds verbose output from dev tools (Docker, cargo,
pytest, kubectl, etc.) before it reaches Claude Code, Codex, Cursor, or Claude
Desktop — keeping the failure signal while compressing the noise, with the omitted
content recoverable through local references rather than dropped entirely.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only:
repo metadata plus the README's description of the compression approach. That is
sufficient for a discovery-log entry, not for an ADOPT — this eval offers none. The
README's own reduction figures (88–99%) are the authors' self-reported numbers, not
independently measured here.

## Triage note

Left at `discovery-log`. It cites `caveman` in Overlaps with (inherited from the
same overlap set as its closest catalogued peer, `tokenflux`), but the two compress
different things: caveman compresses the *agent's own outbound register* (terser
prompting/output), while usagetrim compresses *third-party tool output* being fed
back into the agent (Docker/cargo/pytest/kubectl noise). Same broad token-efficiency
problem, different target and mechanism — not clearly redundant, so left rather than
SKIPped.

_Triaged 2026-09-27 by the P2 challenger band (daily discovery pass)._

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [usagetrim](https://github.com/00200200/usagetrim) | tool | Local CLI + MCP (MIT) folding verbose dev-tool output (Docker, cargo, pytest, kubectl) for Claude Code/Codex/Cursor/Desktop while preserving failure signals, with omitted content recoverable via local references | Verbose CLI output from dev tools burns agent context/tokens even though only the failure signal matters | tokenflux, deadeye-cc, caveman |
