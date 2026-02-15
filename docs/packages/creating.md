# Creating Packages

## Manual Package Creation

A package requires two things: an `ai-config-kit-package.yaml` manifest and the component files it references.

### Manifest Format

The manifest declares package metadata and lists all components.

#### Required Fields

```yaml
name: my-package           # Lowercase alphanumeric with hyphens
version: 1.0.0             # Semantic versioning (X.Y.Z)
description: What this package does
author: Your Name
license: MIT
namespace: org/repo        # Unique namespace identifier
```

| Field | Rules |
|-------|-------|
| `name` | Lowercase letters, numbers, hyphens, underscores only |
| `version` | Must follow semver: `MAJOR.MINOR.PATCH` with optional pre-release suffix |
| `description` | Free text |
| `author` | Free text |
| `license` | License identifier (MIT, Apache-2.0, etc.) |
| `namespace` | Typically `owner/repo` format |

#### Optional Fields

These fields are not currently parsed by the manifest parser but are useful for documentation:

```yaml
author_email: team@example.com
homepage: https://example.com
repository: https://github.com/org/repo
keywords: [python, testing, security]
```

#### Components Section

The `components` section contains named lists for each component type:

```yaml
components:
  instructions:
    - name: code-style
      file: instructions/code-style.md
      description: Code style guidelines
      tags: [style, quality]

  mcp_servers:
    - name: filesystem
      file: mcp/filesystem.json
      description: Filesystem access server
      credentials:
        - name: ALLOWED_DIRECTORIES
          description: Directories the server can access
          required: false
          default: "."

  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Run checks before commits
      hook_type: pre-commit

  commands:
    - name: test
      file: commands/test.sh
      description: Run test suite
      command_type: shell

  skills:
    - name: deploy
      file: skills/deploy
      description: Deployment automation skill

  workflows:
    - name: review
      file: workflows/review.md
      description: Code review workflow

  memory_files:
    - name: project-context
      file: memory_files/CLAUDE.md
      description: Project context and conventions

  resources:
    - name: gitignore
      file: resources/.gitignore
      description: Standard gitignore
      install_path: .gitignore
      checksum: sha256:e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855
      size: 250
```

### Complete Example Manifest

This manifest demonstrates all component types in a single package:

```yaml
name: python-dev-setup
version: 2.0.0
description: Python development environment with linting, testing, and MCP tools
author: Engineering Team
license: MIT
namespace: acme/python-packages

components:
  instructions:
    - name: python-style
      file: instructions/python-style.md
      description: PEP 8 guidelines with project-specific conventions
      tags: [python, style, pep8]

    - name: testing-strategy
      file: instructions/testing-strategy.md
      description: pytest patterns and coverage requirements
      tags: [python, testing, pytest]

  mcp_servers:
    - name: filesystem
      file: mcp/filesystem.json
      description: Filesystem access for project files
      credentials:
        - name: ALLOWED_DIRECTORIES
          description: Comma-separated directories to allow access
          required: false
          default: "."

  hooks:
    - name: pre-commit
      file: hooks/pre-commit.sh
      description: Run black, ruff, and mypy before commits
      hook_type: pre-commit

  commands:
    - name: test
      file: commands/test.sh
      description: Run pytest with coverage reporting
      command_type: shell

    - name: lint
      file: commands/lint.sh
      description: Run ruff with auto-fix
      command_type: shell

  resources:
    - name: gitignore
      file: resources/.gitignore
      description: Python-specific gitignore
      install_path: .gitignore
      checksum: sha256:abc123...
      size: 450
```

### Directory Structure

After creating the manifest, create directories and files to match:

```
python-dev-setup/
├── ai-config-kit-package.yaml
├── README.md
├── instructions/
│   ├── python-style.md
│   └── testing-strategy.md
├── mcp/
│   └── filesystem.json
├── hooks/
│   └── pre-commit.sh
├── commands/
│   ├── test.sh
│   └── lint.sh
└── resources/
    └── .gitignore
```

### Validation

The manifest parser validates:

- All required fields are present
- Version follows semantic versioning
- Every `file` reference points to an existing file in the package directory
- Component names are unique within each type

If validation fails, `devsync package install` reports the specific errors:

```
Error: Manifest validation failed: Instruction file not found: instructions/missing.md
```

## Creating Packages from Existing Projects

The `devsync package create` command scans a project for existing AI configurations and generates a package automatically.

### Basic Usage

```bash
devsync package create --name my-package
```

This scans the current project for:

- Instructions in `.claude/rules/`, `.cursor/rules/`, `.windsurf/rules/`, etc.
- MCP server configs in `.claude/settings.local.json`
- Hooks in `.claude/hooks/`
- Commands in `.claude/commands/`
- Skills in `.claude/skills/`
- Workflows in `.windsurf/workflows/`
- Memory files (CLAUDE.md)
- Resources in `.devsync/resources/`

### Command Options

```bash
devsync package create \
  --name my-package \           # Package name (required in non-interactive mode)
  --version 1.0.0 \             # Version (default: 1.0.0)
  --description "Description" \ # Package description
  --author "Your Name" \        # Author (default: git user.name)
  --license MIT \               # License (default: MIT)
  --output ./packages \         # Output directory (default: current dir)
  --project ~/my-project \      # Project to scan (default: current dir)
  --no-interactive \            # Skip prompts
  --scrub-secrets \             # Template secrets in MCP configs (default)
  --keep-secrets \              # Preserve secrets as-is
  --force \                     # Overwrite existing package directory
  --json                        # Output results as JSON
```

### Interactive Mode

By default, `package create` runs interactively:

```bash
$ devsync package create

Scanning project: /home/user/my-project

Detected components:
┏━━━━━━━━━━━━━┳━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃ Type        ┃ Count┃ Details                          ┃
┡━━━━━━━━━━━━━╇━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩
│ Instructions│     3│ code-style, testing, security    │
│ MCP Servers │     1│ filesystem                       │
│ Hooks       │     2│ pre-commit, post-checkout        │
│ Commands    │     1│ test                             │
└─────────────┴──────┴──────────────────────────────────┘

Total: 7 component(s)

Package name [my-project]: my-team-config
Package description [Configuration package for my-project]: Team dev standards
Creating package with 7 components
Proceed? [Y/n]: y

Package created successfully!
  Location: /home/user/my-project/package-my-team-config
  Components: 7
  Secrets templated: 2
```

### Non-Interactive Mode

For CI/CD or scripting:

```bash
devsync package create \
  --name ci-package \
  --description "Auto-generated package" \
  --no-interactive \
  --json
```

## Secret Detection and Templating

When creating packages from existing projects, MCP server configurations often contain API keys, tokens, or other credentials. The `--scrub-secrets` flag (enabled by default) automatically detects and templates these values.

### How Detection Works

The secret detector uses three confidence levels:

| Confidence | Action | Triggers |
|-----------|--------|----------|
| **HIGH** | Auto-template | Key names containing TOKEN, KEY, SECRET, PASSWORD, AUTH, API; JWT patterns; API key patterns (20+ alphanumeric chars) |
| **MEDIUM** | Auto-template | High-entropy values (>4.5 bits/char); ambiguous keys like `*_URL` with credentials |
| **SAFE** | Preserve | Booleans, version strings, short values (<8 chars), URLs without credentials, keys containing PATH, DIR, HOST, PORT |

### Example

Given this MCP configuration in a project:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "ghp_abc123def456ghi789jkl012mno345pqr678",
        "GITHUB_HOST": "github.com"
      }
    }
  }
}
```

After `devsync package create --scrub-secrets`, the packaged config becomes:

```json
{
  "mcpServers": {
    "github": {
      "command": "npx",
      "args": ["-y", "@modelcontextprotocol/server-github"],
      "env": {
        "GITHUB_TOKEN": "${GITHUB_TOKEN}",
        "GITHUB_HOST": "github.com"
      }
    }
  }
}
```

The manifest also generates credential descriptors for templated values:

```yaml
mcp_servers:
  - name: github
    file: mcp/github.json
    description: GitHub MCP server
    credentials:
      - name: GITHUB_TOKEN
        description: Environment variable for github
        required: true
```

### Disabling Secret Scrubbing

If you need to preserve values (for example, non-sensitive defaults):

```bash
devsync package create --name my-package --keep-secrets
```

!!! warning "Security"
    Only use `--keep-secrets` when you are certain no sensitive values exist in MCP configurations. The package directory will contain the original values verbatim.

## Testing a Package

After creating a package, verify it works:

```bash
# Create a temporary test project
mkdir /tmp/test-project && cd /tmp/test-project
git init

# Install the package
devsync package install /path/to/my-package --ide claude

# Check what was installed
devsync package list

# Verify files exist
ls -la .claude/rules/
ls -la .claude/hooks/
ls -la .claude/commands/

# Clean up
devsync package uninstall my-package --yes
```

Test across multiple IDEs to verify filtering works correctly:

```bash
# Claude Code gets everything
devsync package install ./my-package --ide claude

# Cursor gets only instructions, MCP, and resources
devsync package install ./my-package --ide cursor --project /tmp/test-cursor

# Windsurf gets instructions, MCP, workflows, and resources
devsync package install ./my-package --ide windsurf --project /tmp/test-windsurf
```

## Best Practices

**Keep packages focused.** A package for "Python development" is better than a package for "everything." Users can install multiple packages.

**Use semantic versioning.** Bump the patch version for typo fixes, minor for new components, major for breaking changes (renamed or removed files).

**Write a README.** Include what the package does, what tools it requires, and how to customize it after installation. The `package create` command generates one automatically.

**Tag components consistently.** Tags like `[python, testing, pytest]` are more useful than `[misc, important]`.

**Make scripts portable.** Use `#!/usr/bin/env bash`, check for required commands before using them, and avoid platform-specific flags.

**Version control your packages.** A package directory works well as a Git repository. Tag releases to match the manifest version.
