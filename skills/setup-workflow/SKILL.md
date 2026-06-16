---
name: setup-workflow
description: Bootstrap the recommended AI workflow in any repo — checks what's installed, creates CLAUDE.md with quality rules, and identifies gaps
---

# Setup Workflow

Bootstrap the recommended AI workflow in the current repo. Creates a project CLAUDE.md with quality-producing rules, checks which global tools are installed, and identifies what's missing for your ACMM level.

## Trigger

`/setup-workflow` or `/setup-workflow L3` (to target a specific ACMM level)

## Workflow

### 1. Detect project context

```bash
# Language/framework detection
ls package.json pyproject.toml Cargo.toml go.mod pom.xml Gemfile composer.json 2>/dev/null
# Existing instruction files
ls CLAUDE.md .claude.local.md AGENTS.md GEMINI.md .github/copilot-instructions.md 2>/dev/null
# Test framework detection
ls jest.config* vitest.config* pytest.ini .pytest_cache tsconfig.json 2>/dev/null
# CI detection
ls .github/workflows/*.yml .gitlab-ci.yml Jenkinsfile 2>/dev/null
```

### 2. Check global tool installation

Verify which recommended tools are already installed globally:

```bash
# Plugins
ls ~/.claude/plugins/cache/ 2>/dev/null

# Skills
ls ~/.claude/skills/ 2>/dev/null

# MCP servers
grep -c "mcpServers" ~/.claude/settings.json 2>/dev/null
```

Map against the recommended stack from WORKFLOW.md for the target ACMM level.

### 3. Create or update CLAUDE.md

If no CLAUDE.md exists, create one. If one exists, propose additions for gaps.

The CLAUDE.md should include these sections based on what's detected:

**Always include:**
- Project overview (what this repo is, one line)
- Build/test/dev commands (detected from package.json, Makefile, etc.)
- Code style rules (immutability, small files, small functions)
- Testing requirements (TDD workflow, minimum coverage)
- Security checklist (no hardcoded secrets, input validation)
- Git workflow (conventional commits, PR format)

**Include if relevant framework detected:**
- Framework-specific patterns and conventions
- Key file locations (entry points, config, routes)
- Environment setup (required env vars)

**Include for L3+:**
- PR acceptance criteria
- Coverage gating thresholds
- Error handling policy

**Include for L4+:**
- Feedback loop configuration
- Automation boundaries (what agents can/cannot do autonomously)

### 4. Create .claude.local.md for personal preferences

If it doesn't exist, create with:
- User-specific tool preferences
- Local development quirks
- Add to .gitignore if not already there

### 5. Report

```
## Workflow Setup Report

**Repo:** {name}
**Detected:** {language/framework}
**Target ACMM Level:** L{n}

### Global Tools
| Tool | Required for L{n} | Installed |
|------|-------------------|-----------|
| mattpocock/skills | ✅ | ✅ / ❌ |
| graphify | ✅ | ✅ / ❌ |
| ... | ... | ... |

### Files Created/Updated
- {list of files created or modified}

### Missing Tools
{list of tools to install globally with install commands}

### Next Steps
1. {most important thing to do next}
2. {second}
```

## CLAUDE.md Template

The generated CLAUDE.md follows this structure (sections included only when relevant):

```markdown
# {Project Name}

{One-line description}

## Commands

{Detected build/test/dev/lint commands}

## Architecture

{Key directories and their purpose — only if non-obvious}

## Code Style

- Immutability: create new objects, never mutate existing ones
- Small files (200-400 lines typical, 800 max)
- Small functions (<50 lines)
- No deep nesting (>4 levels)

## Testing

- TDD: write test first (RED), implement (GREEN), refactor
- Minimum coverage: 80%
- Fix implementation, not tests (unless tests are wrong)

## Security

- No hardcoded secrets — use environment variables
- Validate all user input at system boundaries
- Parameterized queries for database operations
- Sanitize HTML output

## Git

- Conventional commits: feat, fix, refactor, docs, test, chore
- PR descriptions: summary + test plan
```
