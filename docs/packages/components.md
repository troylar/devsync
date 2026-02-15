# Component Types

This page documents each component type that a package can contain: the manifest entry format, the file format, and how the component is installed.

## Instructions

Instructions are Markdown files that guide AI coding assistant behavior. They are the most widely supported component type -- every IDE that DevSync supports can use instructions.

### Manifest Entry

```yaml
components:
  instructions:
    - name: code-quality
      file: instructions/code-quality.md
      description: Code quality and review guidelines
      tags: [quality, review, best-practices]
      ide_support: null  # null or omitted = all IDEs
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Unique identifier within the package |
| `file` | Yes | Relative path to the .md file |
| `description` | Yes | What this instruction covers |
| `tags` | No | Searchable categorization tags |
| `ide_support` | No | Restrict to specific IDEs (omit for all) |

### File Format

Plain Markdown. Write clear, actionable guidelines:

```markdown
# Code Quality Guidelines

## Naming Conventions

- Variables and functions: `snake_case`
- Classes: `PascalCase`
- Constants: `UPPER_CASE`
- Use descriptive names that reveal intent

## Error Handling

- Handle errors explicitly at the call site
- Use custom exceptions for domain errors
- Never swallow exceptions silently
- Log errors with sufficient context for debugging

## Code Organization

- One responsibility per function
- Maximum 3-4 parameters per function
- Use early returns to reduce nesting
- Group related functions in the same module
```

### Installation Paths

| IDE | Installed To | Extension |
|-----|-------------|-----------|
| Claude Code | `.claude/rules/<name>.md` | `.md` |
| Cursor | `.cursor/rules/<name>.mdc` | `.mdc` |
| Windsurf | `.windsurf/rules/<name>.md` | `.md` |
| GitHub Copilot | `.github/instructions/<name>.instructions.md` | `.instructions.md` |
| Kiro | `.kiro/steering/<name>.md` | `.md` |
| Cline | `.clinerules/<name>.md` | `.md` |
| Roo Code | `.roo/rules/<name>.md` | `.md` |
| Codex CLI | Section in `AGENTS.md` | `.md` |

---

## MCP Servers

MCP (Model Context Protocol) server configurations define external tool integrations. Each MCP component is a JSON file that tells the IDE how to launch and connect to an MCP server.

### Manifest Entry

```yaml
components:
  mcp_servers:
    - name: filesystem
      file: mcp/filesystem.json
      description: Local filesystem access via MCP
      credentials:
        - name: ALLOWED_DIRECTORIES
          description: Comma-separated list of directories to expose
          required: false
          default: "."
        - name: GITHUB_TOKEN
          description: GitHub personal access token
          required: true
          example: "ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
      ide_support: [claude, windsurf]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Server identifier |
| `file` | Yes | Relative path to .json config |
| `description` | Yes | What the server provides |
| `credentials` | No | Environment variables needed |
| `ide_support` | No | IDEs that support this server |

### Credential Descriptors

Each credential entry describes an environment variable:

```yaml
credentials:
  - name: API_KEY            # UPPER_SNAKE_CASE, required
    description: Service API key
    required: true            # true = must be provided (default)
    default: null             # Cannot have default if required
    example: "sk-abc123..."   # Example value for documentation
  - name: LOG_LEVEL
    description: Server log verbosity
    required: false
    default: "info"           # Default used when not provided
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Env var name (UPPER_SNAKE_CASE) |
| `description` | Yes | What this credential is for |
| `required` | No | Whether user must provide it (default: true) |
| `default` | No | Default value (only valid when required=false) |
| `example` | No | Example value for user reference |

!!! note "Validation"
    A credential cannot be both `required: true` and have a `default` value. The manifest parser enforces this.

### File Format

Standard MCP server configuration JSON:

```json
{
  "mcpServers": {
    "filesystem": {
      "command": "npx",
      "args": [
        "-y",
        "@modelcontextprotocol/server-filesystem",
        "${ALLOWED_DIRECTORIES:-.}"
      ],
      "env": {}
    }
  }
}
```

Use `${VAR_NAME}` placeholders for values that should be configured per-installation. The `${VAR:default}` syntax provides a fallback.

### Supported IDEs

Claude Code, Cursor, Windsurf, Roo Code, GitHub Copilot, Antigravity, Amazon Q, JetBrains AI, Zed, Continue.dev, Trae, Augment, Tabnine, and OpenHands.

---

## Hooks

Hooks are shell scripts triggered by IDE lifecycle events. Currently, only Claude Code supports hooks.

### Manifest Entry

```yaml
components:
  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Run linting and formatting before commits
      hook_type: pre-commit
      ide_support: [claude]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Hook identifier |
| `file` | Yes | Relative path to shell script |
| `description` | Yes | What the hook does |
| `hook_type` | Yes | Trigger type (e.g., `pre-commit`, `post-install`) |
| `ide_support` | No | IDEs that support hooks (default: `[claude]`) |

### File Format

Executable shell script:

```bash
#!/usr/bin/env bash
# Pre-commit hook: run linting and formatting checks

set -e

echo "Running pre-commit checks..."

# Check formatting
if command -v black &> /dev/null; then
    echo "-> Checking formatting (black)..."
    black --check . || {
        echo "Formatting issues found. Run 'black .' to fix."
        exit 1
    }
fi

# Check linting
if command -v ruff &> /dev/null; then
    echo "-> Checking linting (ruff)..."
    ruff check . || {
        echo "Linting issues found. Run 'ruff check --fix .' to fix."
        exit 1
    }
fi

echo "All pre-commit checks passed."
```

!!! tip "Script requirements"
    - Include `#!/usr/bin/env bash` shebang
    - Use `set -e` to fail on errors
    - Check for required tools before using them
    - DevSync sets the executable bit (0o755) automatically during installation

### Installation Path

| IDE | Installed To |
|-----|-------------|
| Claude Code | `.claude/hooks/<name>.sh` |

---

## Commands

Commands are shell scripts that users can invoke on demand, typically via slash commands in the IDE.

### Manifest Entry

```yaml
components:
  commands:
    - name: test
      file: commands/test.sh
      description: Run test suite with coverage
      command_type: shell
      ide_support: [claude, roo]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Command identifier |
| `file` | Yes | Relative path to script |
| `description` | Yes | What the command does |
| `command_type` | Yes | Type: `shell` or `slash` |
| `ide_support` | No | IDEs that support commands |

### File Format

```bash
#!/usr/bin/env bash
# Run pytest with coverage reporting

set -e

if ! command -v pytest &> /dev/null; then
    echo "pytest not found. Install with: pip install pytest pytest-cov"
    exit 1
fi

pytest \
    --cov=. \
    --cov-report=term \
    --cov-report=html \
    -v \
    "$@"

echo ""
echo "Coverage report: htmlcov/index.html"
```

### Installation Paths

| IDE | Installed To |
|-----|-------------|
| Claude Code | `.claude/commands/<name>.sh` |
| Roo Code | `.roo/commands/<name>.md` |

---

## Skills

Skills are Claude Code-specific directories that contain a `SKILL.md` file and optional supporting files. Skills can be invoked via slash commands and are shared across Claude products.

### Manifest Entry

```yaml
components:
  skills:
    - name: deploy
      file: skills/deploy
      description: Automated deployment to staging and production
      ide_support: [claude]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Skill identifier (becomes directory name) |
| `file` | Yes | Relative path to skill directory |
| `description` | Yes | What the skill does |
| `ide_support` | No | IDEs that support skills (default: `[claude]`) |

### File Format

A skill is a directory containing at minimum a `SKILL.md` file:

```
skills/deploy/
├── SKILL.md          # Required: skill definition
├── deploy.sh         # Optional: supporting script
└── config.yaml       # Optional: supporting config
```

The `SKILL.md` file uses frontmatter to declare the skill metadata:

```markdown
---
name: deploy
description: Deploy the application to staging or production
---

# Deploy Skill

Deploy the current project to the specified environment.

## Usage

Invoke with `/deploy staging` or `/deploy production`.

## Steps

1. Run the test suite
2. Build the application
3. Push to the target environment
4. Verify the deployment health check
```

### Installation Path

| IDE | Installed To |
|-----|-------------|
| Claude Code | `.claude/skills/<name>/` (entire directory copied) |

---

## Workflows

Workflows are Windsurf-specific files that define multi-step automated processes.

### Manifest Entry

```yaml
components:
  workflows:
    - name: code-review
      file: workflows/code-review.md
      description: Automated code review workflow
      ide_support: [windsurf]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Workflow identifier |
| `file` | Yes | Relative path to workflow file |
| `description` | Yes | What the workflow does |
| `ide_support` | No | IDEs that support workflows (default: `[windsurf]`) |

### File Format

Markdown file defining the workflow steps:

```markdown
# Code Review Workflow

## Trigger
Run on pull request creation or update.

## Steps

1. Check for test coverage on changed files
2. Review code style compliance
3. Identify potential security issues
4. Suggest performance improvements
5. Generate review summary
```

### Installation Path

| IDE | Installed To |
|-----|-------------|
| Windsurf | `.windsurf/workflows/<name>.md` |

---

## Memory Files

Memory files are `CLAUDE.md` files that persist context across Claude Code sessions. They can exist at the project root or in subdirectories to scope context to specific areas of the codebase.

### Manifest Entry

```yaml
components:
  memory_files:
    - name: project-context
      file: memory_files/CLAUDE.md
      description: Project architecture and conventions
      ide_support: [claude]
    - name: api-context
      file: memory_files/src/api/CLAUDE.md
      description: API layer conventions and patterns
      ide_support: [claude]
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Memory file identifier |
| `file` | Yes | Relative path within package |
| `description` | Yes | What context this file provides |
| `ide_support` | No | IDEs that support memory files (default: `[claude]`) |

### File Format

Standard Markdown. The content should provide persistent context:

```markdown
# Project Context

## Architecture

This project uses a layered architecture:
- `src/api/` -- HTTP handlers and route definitions
- `src/core/` -- Business logic, independent of transport
- `src/storage/` -- Database access and persistence
- `src/utils/` -- Shared utilities

## Conventions

- All functions must have type hints
- Use dataclasses for data models
- Prefer composition over inheritance
- Tests go in `tests/` mirroring the `src/` structure

## Active Decisions

- Using SQLAlchemy 2.0 with async sessions
- Pydantic v2 for request/response validation
- pytest with fixtures for all database tests
```

### Installation Path

| IDE | Installed To |
|-----|-------------|
| Claude Code | `CLAUDE.md` at project root (for root memory files) or subdirectory paths preserved |

---

## Resources

Resources are arbitrary files -- configuration templates, .gitignore files, editor configs, or any other file that should be part of the project setup.

### Manifest Entry

```yaml
components:
  resources:
    - name: gitignore
      file: resources/.gitignore
      description: Python-specific gitignore
      install_path: .gitignore
      checksum: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
      size: 450
```

| Field | Required | Description |
|-------|----------|-------------|
| `name` | Yes | Resource identifier |
| `file` | Yes | Relative path in package |
| `description` | Yes | What the resource is |
| `install_path` | Yes | Where to install in the project (relative to project root) |
| `checksum` | Yes | SHA-256 checksum for integrity (`sha256:...`) |
| `size` | Yes | File size in bytes |

### File Format

Any file type. Resources are copied verbatim (both text and binary files are supported):

```gitignore
# Python
__pycache__/
*.py[cod]
*.so
.Python
env/
venv/
*.egg-info/
dist/
build/

# Testing
.coverage
htmlcov/
.pytest_cache/

# IDEs
.vscode/
.idea/
*.swp
```

### Installation Path

Resources are installed to the path specified by `install_path`, relative to the project root. If `install_path` is not specified, it defaults to the `file` path.

| IDE | Supported |
|-----|-----------|
| Claude Code | Yes |
| Cursor | Yes |
| Windsurf | Yes |
| Kiro | Yes |
| Cline | Yes |
| Roo Code | Yes |
| Codex CLI | Yes |
| GitHub Copilot | No |
