# New Tools Evaluation (Loop 1)

Tools surfaced by the automated catalog scan on 2026-06-15. Each assessed for whether it earns a slot in the recommended WORKFLOW.md stack.

## caveman

**Stars:** 73,065 | **Last updated:** 2026-06-12 | **Forks:** 4,126
**What it does:** Claude Code skill that changes agent communication style to drop filler, articles, and pleasantries. Cuts ~75% of output tokens while preserving full technical accuracy. Works across 30+ editors (Claude Code, Codex, Gemini, Cursor, etc.).
**Current workflow alternative:** headroom (L4) compresses tool *outputs* before they reach the LLM. token-optimizer-mcp does similar server-side.
**Key difference:** caveman reduces *agent output* tokens (what the agent says back to you). headroom reduces *input* tokens (tool output before the agent reads it). They solve opposite directions of the token problem and are complementary, not competing.

**Verdict:** ADD to L2 (alongside headroom at L4)
**Justification:** At 73K stars it's the most-adopted skill in the ecosystem. Unlike headroom (which compresses inputs), caveman compresses outputs - making every session cheaper and faster. It's zero-config (just invoke `/caveman`) and has no dependencies. The token savings compound across an entire session. Adding at L2 because it requires no measurement infrastructure - it's a communication style, not a feedback loop.

## trailofbits/skills

**Stars:** 5,715 | **Last updated:** 2026-06-15 (today) | **Forks:** 498
**What it does:** Full Claude Code plugin marketplace from Trail of Bits with 10+ security plugins covering smart contract security, C/C++ security review, GitHub Actions auditing, differential review, Burp Suite integration, and dimensional analysis for formula bugs. Installable as a marketplace (`/plugin marketplace add trailofbits/skills`).
**Current workflow alternative:** SkillSpector (L5) scans skills for vulnerabilities. security-guidance plugin provides general security review. ghostsecurity/skills provides AppSec skills.
**Key difference:** Trail of Bits is one of the most respected security audit firms in the industry. Their skills encode actual audit methodology, not just generic security checks. SkillSpector scans *skills* for malicious patterns; trailofbits/skills performs *code* security audits - they solve different problems.

**Verdict:** ADD to L3 (alongside security-guidance)
**Justification:** Security review should happen as early as measurement begins, not deferred to L5. Trail of Bits's reputation gives these skills unique credibility - they're encoding real audit methodology from a firm that has found vulnerabilities in major projects. The differential-review and c-review plugins are particularly valuable for CI-integrated security feedback. Complementary to SkillSpector (which vets skills) and security-guidance (which is more general).

## book-to-skill

**Stars:** 5,765 | **Last updated:** 2026-06-15 (today) | **Forks:** 730
**What it does:** Converts any technical book PDF (plus EPUB, DOCX, MD, HTML, RTF, MOBI) into a structured Claude Code skill with chapter-by-chapter on-demand loading, a glossary, and a patterns index. The book becomes queryable context during coding sessions. Works across Claude Code, Copilot CLI, and Amp.
**Current workflow alternative:** Nothing in the workflow does this. context7 provides live library docs, but not book-length domain knowledge.
**Key difference:** Completely unique capability. No other tool converts arbitrary technical books into agent-consumable skills.

**Verdict:** SKIP (useful but doesn't improve code quality or feedback loops)
**Justification:** While unique and well-built, book-to-skill is a knowledge-ingestion convenience, not a code quality or workflow improvement tool. It doesn't produce feedback loops, enforce methodology, or measure anything. It's genuinely useful for individual learning, but adding it to the recommended stack would dilute the ACMM-focused "fewer tools, more feedback loops" principle. Keep in catalog for users who need it, but don't add to WORKFLOW.md.

## humanizer

**Stars:** 24,373 | **Last updated:** 2026-06-07 | **Forks:** 2,311
**What it does:** Removes signs of AI-generated writing from text. Makes AI output sound more natural and human. Simple invocation: `/humanizer [paste text]`.
**Current workflow alternative:** taste-skill (prevents generic output) and stop-slop (removes AI tells from prose) are in the catalog but not in the recommended workflow.
**Key difference:** humanizer is specifically about making *written output* pass as human-written. taste-skill is about aesthetic quality. stop-slop is about removing filler words.

**Verdict:** SKIP (writing quality tool, not a code quality tool)
**Justification:** The recommended workflow is about producing high-quality *code*, not high-quality prose. humanizer, taste-skill, and stop-slop are all legitimate tools for content creation, but they don't improve code quality, testing, or feedback loops. Adding a prose-polishing tool to a code-focused workflow would be scope creep. Keep in catalog for users who write documentation or marketing content alongside code.
