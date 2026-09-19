# Evaluation: jev-browser

**Repo:** [Ying-Kai-Liao/jev-browser](https://github.com/Ying-Kai-Liao/jev-browser)
**Stars:** 13 | **Last updated:** 2026-09-19 (pushed) | **License:** MIT
**Last verified:** 2026-09-19
**Last triaged:** 2026-09-19  <!-- triaged: bulk -->
**Dev loop stage:** Verify
**Layer:** Tooling

---

## What it does

Browser automation where an LLM plans and TypeSafe.ai's Jev decision model executes the plan,
shipped as a library, CLI, and MCP server — aimed at cutting the per-step cost of LLM-driven
browser automation by delegating execution to a cheaper decision model.

## How we tested it

**Evidence:** SOURCE-ONLY

We did **not** install or run this tool. This evaluation is source-grounded only: repo metadata
plus the CATALOG "Overlaps with" cell (playwright, browser-use, agent-browser). That is sufficient
for the verdict below, because the verdict turns on *redundancy with an already-installed STACK
incumbent doing the same job*, not on the tool's behavior — a question the overlap answers
directly. It would not be sufficient to support an ADOPT, and this eval does not offer one.

## Verdict

**SKIP** — redundant with `playwright` (STACK, ADOPT, `claude mcp add playwright -- npx
@playwright/mcp@latest`). Both are MCP servers that give an agent browser automation/testing;
playwright is already installed, validated (RUN evidence), and vendor-maintained (Microsoft).
jev-browser's differentiator — routing execution through TypeSafe's proprietary Jev model instead
of the LLM driving Playwright's own accessibility-tree actions directly — adds a paid third-party
dependency to a job the STACK incumbent already does for free, with no stated correctness or
capability advantage. A second, unvalidated, 13-star entrant earns nothing over the incumbent.

_Triaged 2026-09-19 by the daily discovery routine (today's new lead)._
