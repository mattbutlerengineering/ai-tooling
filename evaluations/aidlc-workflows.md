# Evaluation: aidlc-workflows (AI-DLC)

**Repo:** [awslabs/aidlc-workflows](https://github.com/awslabs/aidlc-workflows)
**Stars:** 2,984 | **Last updated:** 2026-06-18 | **License:** MIT-0
**Dev loop stage:** Implement (cross-cutting: all stages)
**Layer:** Process

---

## What it does

AI-DLC (AI-Driven Development Life Cycle) is AWS's adaptive three-phase workflow for AI coding agents. It ships as a set of markdown rule files that replace or augment your CLAUDE.md (or equivalent instruction file for 6 other editors: Kiro, Amazon Q, Cursor, Cline, GitHub Copilot). The three phases are Inception (what + why: requirements, user stories, application design, risk assessment), Construction (how: functional design, code generation, testing), and Operations (deploy + monitor: placeholder, not yet implemented).

The mechanism is progressive rule loading. A 539-line `core-workflow.md` file acts as the orchestrator, telling the agent to conditionally load ~20 detailed rule files from `aws-aidlc-rule-details/` (organized under `common/`, `inception/`, `construction/`, `extensions/`, `operations/`). The agent reads only the rules needed for the current stage, keeping context cost bounded. An extension system adds opt-in security, testing, and resiliency rules as blocking constraints — once enabled, the agent must verify compliance at each stage before proceeding.

Distinctive features:
- **Overconfidence prevention** — explicit rules telling the agent to ask more questions, not fewer, with a documented root-cause analysis of why "skip if not needed" directives fail
- **Depth-level adaptation** — the agent decides artifact detail level based on problem complexity (simple bug fix → concise requirements; system migration → multi-round questions)
- **Audit trail** — mandatory logging of every user input and AI response in `aidlc-docs/audit.md` with ISO timestamps
- **Question-driven interaction** — requirements gathered via structured multiple-choice questions written to files, not chat, so they persist across sessions
- **v2.0 Preview** — announced with a full specification PDF, aiming to make "autonomous software development practical" via self-correcting engineering workflows

## How we tested it

Architecture review of the full rule file set. Read the core-workflow.md (539 lines), depth-levels.md, overconfidence-prevention.md, and the extension system structure. Assessed the Claude Code setup path (copies core-workflow.md to CLAUDE.md, rule details to `.aidlc-rule-details/`). Compared the three-phase model against GSD (superpowers), which uses a Discover → Architect → Decompose → [inner loop per task] → Integrate → Retrospect outer loop with Plan → Implement → Verify → Review → Ship inner loop.

```bash
gh api repos/awslabs/aidlc-workflows --jq '.description, .stargazers_count, .updated_at'
gh api repos/awslabs/aidlc-workflows/contents/aidlc-rules/aws-aidlc-rules/core-workflow.md --jq '.content' | base64 -d
gh api repos/awslabs/aidlc-workflows/contents/aidlc-rules/aws-aidlc-rule-details/common/overconfidence-prevention.md --jq '.content' | base64 -d
gh api repos/awslabs/aidlc-workflows/contents/aidlc-rules/aws-aidlc-rule-details/common/depth-levels.md --jq '.content' | base64 -d
```

## What worked

- **Overconfidence prevention is a genuine insight.** The documented root-cause analysis ("skip entire categories if not applicable" → agent silently skips everything) matches real LLM failure modes. The fix (default to asking, not skipping) is simple and correct.
- **Progressive rule loading is context-efficient.** Instead of dumping all rules into CLAUDE.md, the agent loads only what's needed per stage. The extension opt-in system adds blocking constraints without paying context cost until the user enables them.
- **Cross-editor portability is real.** The same rule files work across 6 editors with only the destination directory changing. This is the only framework in the catalog with official setup instructions for Kiro, Amazon Q, Cursor, Cline, Claude Code, and GitHub Copilot.
- **Supporting tools ecosystem is growing.** The evaluator framework (golden test cases, semantic evaluation, NFR testing) and the experimental design reviewer (multi-agent: Critique, Alternatives, Gap Analysis) show investment in quality assurance.
- **Audit trail provides compliance value.** Mandatory timestamped logging of every interaction in `audit.md` is useful for regulated environments — no other framework in the catalog has this.

## What didn't work or surprised us

- **Replaces CLAUDE.md entirely.** The Claude Code setup copies core-workflow.md *to* CLAUDE.md, overwriting any existing project-specific instructions. This is a lifestyle commitment — you can't incrementally adopt individual rules alongside an existing CLAUDE.md.
- **Operations phase is a placeholder.** The third phase (deploy/monitor) has no implemented rules — just a directory structure and a TODO note. The actual workflow is two-phase today.
- **No inner-loop awareness.** AI-DLC treats development as Inception → Construction linearly, without the iterative inner loop (Plan → Implement → Verify → Review → Ship → Reflect) that GSD and superpowers provide. There's no built-in TDD enforcement, review gates, or reflection arcs.
- **Heavyweight artifact generation.** The framework creates an `aidlc-docs/` directory with inception plans, requirements, user stories, application designs, functional designs, NFR designs, infrastructure designs, build-and-test plans, state tracking, and audit logs. For a single-session bug fix, this is extreme overhead.
- **Amazon/Kiro-first design.** While cross-editor, the README leads with Kiro and Amazon Q setup — Claude Code is third. The v2 preview leans into Kiro's spec mode and Amazon Bedrock for the design reviewer.
- **v2 is on a separate branch and not GA.** The "2.0 Preview" is announced but on the `v2` branch, while main is still v0.1.8 (released April 2026).

## Quality signals affected

| Signal | Impact | Evidence |
|--------|--------|----------|
| Correctness | + | Overconfidence prevention and structured requirements gathering reduce assumption-driven bugs |
| Speed | - | Heavy artifact generation and multi-phase ceremonies slow down simple tasks |
| Maintainability | + | Documented decisions and audit trails help future developers understand past choices |
| Safety | + | Extension system with blocking compliance checks; audit trail for regulated environments |
| Cost Efficiency | neutral | Progressive rule loading is token-efficient, but the framework generates many intermediate files |

## Verdict

**CONDITIONAL**

Use when you need a formal, auditable development methodology across a mixed-editor team (especially if the team includes Kiro/Amazon Q/Cursor users alongside Claude Code). The overconfidence prevention and compliance extension system provide real value for enterprise contexts. For Claude Code-only users, superpowers (ADOPT) provides a tighter inner loop with TDD, debugging, and review workflows that AI-DLC lacks. AI-DLC is complementary to superpowers at the project/epic level (Inception for requirements) but redundant at the task level (Construction vs. superpowers' inner loop).

## Catalog entry

| Name | Type | One-liner | Problem it solves | Overlaps with |
|------|------|-----------|-------------------|---------------|
| [aidlc-workflows](https://github.com/awslabs/aidlc-workflows) | framework | AWS adaptive three-phase dev lifecycle rules for AI coding agents across 6 editors | Unstructured AI-assisted development lacks phased gates, risk assessment, and cross-editor consistency | GSD, superpowers |
