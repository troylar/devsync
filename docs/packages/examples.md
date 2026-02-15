# Package Examples

Four complete package examples covering common use cases. Each includes the full manifest, directory structure, and representative component files.

---

## 1. Python Development Setup

A package for Python projects that enforces coding standards with instructions, automates quality checks with hooks, and provides convenience commands.

### Directory Structure

```
python-dev-setup/
├── ai-config-kit-package.yaml
├── instructions/
│   ├── python-style.md
│   ├── testing-strategy.md
│   └── error-handling.md
├── hooks/
│   └── pre-commit.sh
├── commands/
│   ├── test.sh
│   └── lint.sh
└── resources/
    └── .gitignore
```

### Manifest

```yaml
name: python-dev-setup
version: 1.0.0
description: Python development standards with linting, testing, and code quality
author: Platform Team
license: MIT
namespace: platform/python

components:
  instructions:
    - name: python-style
      file: instructions/python-style.md
      description: PEP 8 conventions with project-specific rules
      tags: [python, style, formatting]

    - name: testing-strategy
      file: instructions/testing-strategy.md
      description: pytest patterns, fixtures, and coverage requirements
      tags: [python, testing, pytest]

    - name: error-handling
      file: instructions/error-handling.md
      description: Exception handling and error reporting patterns
      tags: [python, errors, logging]

  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Run black, ruff, and mypy before every commit
      hook_type: pre-commit

  commands:
    - name: test
      file: commands/test.sh
      description: Run pytest with coverage and HTML report
      command_type: shell

    - name: lint
      file: commands/lint.sh
      description: Run ruff with auto-fix enabled
      command_type: shell

  resources:
    - name: gitignore
      file: resources/.gitignore
      description: Python-specific gitignore
      install_path: .gitignore
      checksum: sha256:a1b2c3d4e5f6...
      size: 320
```

### Key Files

**`instructions/python-style.md`**

```markdown
# Python Style Guide

## Formatting

- Line length: 120 characters maximum
- Indentation: 4 spaces, no tabs
- Formatter: black (run automatically via pre-commit hook)
- Linter: ruff with rule sets E, F, I, N, W

## Type Hints

All functions must include type hints:

    def process_items(items: list[dict[str, str]], limit: int = 10) -> list[str]:
        """Extract names from item dictionaries."""
        return [item["name"] for item in items[:limit]]

Use modern syntax (Python 3.10+): `list[str]` not `List[str]`,
`str | None` not `Optional[str]`.

## Import Order

1. Standard library
2. Third-party packages
3. Local application modules

Each group separated by a blank line. Use `ruff` to enforce ordering.

## Naming

| Element    | Convention       | Example            |
|------------|------------------|--------------------|
| Variables  | snake_case       | user_count         |
| Functions  | snake_case       | get_active_users   |
| Classes    | PascalCase       | UserAccount        |
| Constants  | UPPER_SNAKE_CASE | MAX_RETRY_COUNT    |
| Private    | _leading_under   | _validate_input    |
```

**`hooks/pre-commit.sh`**

```bash
#!/usr/bin/env bash
set -e

echo "Running pre-commit checks..."

if command -v black &> /dev/null; then
    echo "-> black (formatting)"
    black --check . || { echo "Run 'black .' to fix."; exit 1; }
fi

if command -v ruff &> /dev/null; then
    echo "-> ruff (linting)"
    ruff check . || { echo "Run 'ruff check --fix .' to fix."; exit 1; }
fi

if command -v mypy &> /dev/null; then
    echo "-> mypy (type checking)"
    mypy . || { echo "Fix type errors before committing."; exit 1; }
fi

echo "All checks passed."
```

### Installation

```bash
devsync package install ./python-dev-setup --ide claude
```

---

## 2. Security Compliance Package

A package focused on secure coding practices. Contains instructions covering OWASP guidelines and resource files for security tooling configuration.

### Directory Structure

```
security-compliance/
├── ai-config-kit-package.yaml
├── instructions/
│   ├── secure-coding.md
│   ├── authentication.md
│   ├── input-validation.md
│   └── dependency-management.md
└── resources/
    ├── .snyk
    └── security-checklist.md
```

### Manifest

```yaml
name: security-compliance
version: 1.1.0
description: OWASP-aligned secure coding guidelines and security tooling
author: Security Team
license: Apache-2.0
namespace: security/compliance

components:
  instructions:
    - name: secure-coding
      file: instructions/secure-coding.md
      description: Core secure coding principles (OWASP Top 10)
      tags: [security, owasp, coding]

    - name: authentication
      file: instructions/authentication.md
      description: Authentication and session management standards
      tags: [security, auth, sessions]

    - name: input-validation
      file: instructions/input-validation.md
      description: Input validation, sanitization, and encoding rules
      tags: [security, validation, injection]

    - name: dependency-management
      file: instructions/dependency-management.md
      description: Dependency scanning and supply chain security
      tags: [security, dependencies, sca]

  resources:
    - name: snyk-config
      file: resources/.snyk
      description: Snyk vulnerability scanning configuration
      install_path: .snyk
      checksum: sha256:b2c3d4e5f6a7...
      size: 180

    - name: security-checklist
      file: resources/security-checklist.md
      description: Pre-deployment security review checklist
      install_path: docs/security-checklist.md
      checksum: sha256:c3d4e5f6a7b8...
      size: 2400
```

### Key Files

**`instructions/secure-coding.md`**

```markdown
# Secure Coding Standards

## Principles

1. Never trust user input. Validate on the server side.
2. Use parameterized queries for all database operations. Never concatenate
   user input into SQL strings.
3. Encode output for its context (HTML, JavaScript, URL, SQL).
4. Use established authentication libraries. Do not implement custom auth.
5. Apply the principle of least privilege to all access control decisions.

## Forbidden Patterns

The following patterns must never appear in code:

- `eval()`, `exec()`, `Function()` with user-controlled input
- SQL string concatenation: `f"SELECT * FROM users WHERE id = {user_id}"`
- `innerHTML` assignment with unsanitized data
- Hardcoded secrets, API keys, or credentials
- Disabled CSRF protection
- `verify=False` or `rejectUnauthorized: false` in production code
- Wildcard CORS: `Access-Control-Allow-Origin: *`

## Error Handling

- Return generic error messages to users
- Log detailed errors server-side with timestamps, user IDs, and source IPs
- Never expose stack traces, SQL errors, or internal paths in responses
- Never log passwords, tokens, or PII

## Cryptography

- Passwords: Argon2id, bcrypt (cost >= 12), or scrypt
- Symmetric encryption: AES-256-GCM or ChaCha20-Poly1305
- TLS 1.2+ for all data in transit
- Generate keys and IVs from the platform CSPRNG
- Store secrets in environment variables or a secrets manager
```

**`instructions/input-validation.md`**

```markdown
# Input Validation Rules

## Server-Side Validation

All input must be validated on the server. Client-side validation is for UX
only and provides no security benefit.

## Validation Strategy

Use allowlists (whitelists) over denylists:

    # Good: allowlist
    ALLOWED_STATUSES = {"active", "inactive", "pending"}
    if status not in ALLOWED_STATUSES:
        raise ValidationError(f"Invalid status: {status}")

    # Bad: denylist
    BLOCKED = {"admin", "root"}
    if role in BLOCKED:
        raise ValidationError("Blocked role")

## Database Queries

Always use parameterized queries:

    # Good: parameterized
    cursor.execute("SELECT * FROM users WHERE id = %s", (user_id,))

    # Bad: string concatenation
    cursor.execute(f"SELECT * FROM users WHERE id = {user_id}")

## File Uploads

- Validate MIME type and extension against an allowlist
- Enforce maximum file size
- Store uploaded files outside the web root
- Generate random filenames; never use the original filename in the path
```

### Installation

```bash
# Works with any IDE since it only contains instructions and resources
devsync package install ./security-compliance --ide claude
devsync package install ./security-compliance --ide cursor
devsync package install ./security-compliance --ide windsurf
```

---

## 3. Full-Stack Team Package

A comprehensive package for a team working on a full-stack application. Includes instructions for frontend and backend, MCP servers for tooling, hooks for quality gates, commands for common workflows, and resource files.

### Directory Structure

```
fullstack-team/
├── ai-config-kit-package.yaml
├── instructions/
│   ├── api-design.md
│   ├── react-components.md
│   ├── database-patterns.md
│   └── code-review.md
├── mcp/
│   ├── filesystem.json
│   └── github.json
├── hooks/
│   └── pre-commit.sh
├── commands/
│   ├── test-all.sh
│   └── dev.sh
└── resources/
    ├── .editorconfig
    └── .prettierrc
```

### Manifest

```yaml
name: fullstack-team
version: 2.0.0
description: Full-stack development environment with API, React, and database patterns
author: Engineering
license: MIT
namespace: acme/fullstack

components:
  instructions:
    - name: api-design
      file: instructions/api-design.md
      description: RESTful API design patterns and conventions
      tags: [api, rest, backend]

    - name: react-components
      file: instructions/react-components.md
      description: React component patterns with TypeScript
      tags: [react, typescript, frontend]

    - name: database-patterns
      file: instructions/database-patterns.md
      description: Database schema design and query optimization
      tags: [database, sql, backend]

    - name: code-review
      file: instructions/code-review.md
      description: Code review checklist and standards
      tags: [review, quality, process]

  mcp_servers:
    - name: filesystem
      file: mcp/filesystem.json
      description: Project filesystem access
      credentials:
        - name: ALLOWED_DIRECTORIES
          description: Directories to expose to the AI
          required: false
          default: "."

    - name: github
      file: mcp/github.json
      description: GitHub API access for PRs and issues
      credentials:
        - name: GITHUB_TOKEN
          description: GitHub personal access token with repo scope
          required: true
          example: "ghp_xxxxxxxxxxxxxxxxxxxx"

  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Run ESLint, Prettier, and backend linting
      hook_type: pre-commit

  commands:
    - name: test-all
      file: commands/test-all.sh
      description: Run frontend and backend test suites
      command_type: shell

    - name: dev
      file: commands/dev.sh
      description: Start development servers (frontend + backend)
      command_type: shell

  resources:
    - name: editorconfig
      file: resources/.editorconfig
      description: Editor configuration for consistent formatting
      install_path: .editorconfig
      checksum: sha256:d4e5f6a7b8c9...
      size: 280

    - name: prettierrc
      file: resources/.prettierrc
      description: Prettier configuration for frontend code
      install_path: .prettierrc
      checksum: sha256:e5f6a7b8c9d0...
      size: 120
```

### Key Files

**`mcp/github.json`**

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}"
      }
    }
  }
}
```

**`commands/test-all.sh`**

```bash
#!/usr/bin/env bash
set -e

echo "=== Backend Tests ==="
cd backend
if command -v pytest &> /dev/null; then
    pytest --cov=. --cov-report=term -q
else
    echo "pytest not found, skipping backend tests"
fi
cd ..

echo ""
echo "=== Frontend Tests ==="
cd frontend
if [ -f package.json ]; then
    npm test -- --coverage --watchAll=false
else
    echo "No package.json found, skipping frontend tests"
fi
cd ..

echo ""
echo "All test suites complete."
```

### Installation

```bash
# Claude Code: gets all 11 components
devsync package install ./fullstack-team --ide claude

# Cursor: gets 4 instructions + 2 MCP servers + 2 resources = 8 components
devsync package install ./fullstack-team --ide cursor

# Copilot: gets 4 instructions + 2 MCP servers = 6 components
devsync package install ./fullstack-team --ide copilot
```

---

## 4. Claude Code Power User

A Claude-specific package that uses skills, memory files, commands, and hooks to build a highly customized Claude Code environment.

### Directory Structure

```
claude-power-user/
├── ai-config-kit-package.yaml
├── skills/
│   ├── review-pr/
│   │   └── SKILL.md
│   └── create-test/
│       └── SKILL.md
├── memory_files/
│   ├── CLAUDE.md
│   └── src/
│       └── api/
│           └── CLAUDE.md
├── commands/
│   ├── deploy.sh
│   └── db-migrate.sh
└── hooks/
    ├── pre-commit.sh
    └── notification.sh
```

### Manifest

```yaml
name: claude-power-user
version: 1.0.0
description: Advanced Claude Code setup with skills, memory files, and automation
author: Senior Dev
license: MIT
namespace: personal/claude-config

components:
  skills:
    - name: review-pr
      file: skills/review-pr
      description: Automated PR review with security and performance checks

    - name: create-test
      file: skills/create-test
      description: Generate unit tests for a given function or module

  memory_files:
    - name: project-context
      file: memory_files/CLAUDE.md
      description: Project architecture, conventions, and active decisions

    - name: api-context
      file: memory_files/src/api/CLAUDE.md
      description: API layer patterns and endpoint conventions

  commands:
    - name: deploy
      file: commands/deploy.sh
      description: Deploy to staging or production
      command_type: shell

    - name: db-migrate
      file: commands/db-migrate.sh
      description: Run database migrations with safety checks
      command_type: shell

  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Comprehensive pre-commit checks
      hook_type: pre-commit

    - name: notification
      file: hooks/notification.sh
      description: Send Slack notification on task completion
      hook_type: post-task
```

### Key Files

**`skills/review-pr/SKILL.md`**

```markdown
---
name: review-pr
description: Review a pull request for correctness, security, and performance
---

# PR Review Skill

Review the specified pull request thoroughly.

## Process

1. Fetch the PR diff using the GitHub CLI
2. Check each changed file for:
   - Correctness: logic errors, edge cases, null handling
   - Security: injection risks, auth bypasses, hardcoded secrets
   - Performance: N+1 queries, unnecessary allocations, missing indexes
   - Style: naming conventions, code organization, documentation
3. Identify any missing test coverage for changed code
4. Generate a structured review comment with findings organized by severity

## Output Format

Produce a review with sections:
- **Critical** -- must fix before merge
- **Suggestions** -- improvements to consider
- **Positive** -- things done well
```

**`skills/create-test/SKILL.md`**

```markdown
---
name: create-test
description: Generate comprehensive unit tests for a function or module
---

# Create Test Skill

Generate unit tests for the specified function, class, or module.

## Process

1. Read the source file and understand the function signature and behavior
2. Identify edge cases: empty inputs, boundary values, error conditions
3. Generate tests using the project's test framework (pytest by default)
4. Follow the Arrange-Act-Assert pattern
5. Use fixtures and parametrize for related test cases
6. Include both success and failure scenarios

## Requirements

- Tests must be independent and not rely on execution order
- Mock external dependencies (database, network, filesystem)
- Assert specific values, not just truthiness
- Name tests descriptively: test_<function>_<scenario>_<expected>
```

**`memory_files/CLAUDE.md`**

```markdown
# Project Context

## Architecture

Monorepo with three services:
- `src/api/` -- FastAPI HTTP service (port 8000)
- `src/worker/` -- Celery task workers
- `src/shared/` -- Shared models and utilities

## Key Decisions

- SQLAlchemy 2.0 with async sessions
- Pydantic v2 for validation
- pytest with factory_boy for test data
- Alembic for migrations (always review generated SQL)

## Development Flow

1. Create feature branch from main
2. Write tests first (TDD)
3. Implement the feature
4. Run `invoke quality` before committing
5. Open PR and request review
```

**`memory_files/src/api/CLAUDE.md`**

```markdown
# API Layer Context

## Route Organization

Routes are organized by resource in `src/api/routes/`:
- `users.py` -- user CRUD and authentication
- `projects.py` -- project management
- `tasks.py` -- task operations

## Patterns

- All endpoints use dependency injection for database sessions
- Authentication via `get_current_user` dependency
- Response models are separate from database models
- Use `status_code` parameter on route decorators, not manual responses
```

### Installation

```bash
# Only Claude Code supports all these component types
devsync package install ./claude-power-user --ide claude
```

For other IDEs, only the supported components are installed. Since this package has no instructions or resources, installing to Cursor or Windsurf results in no components installed.

!!! tip "Mixed packages"
    If you want a package that works across IDEs, include instructions alongside Claude-specific components. Other IDEs will install the instructions and skip the rest.
